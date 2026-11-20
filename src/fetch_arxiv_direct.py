"""Fetch bounded, subscription-specific arXiv candidates without a shared database.

The API sorts by first submission; the requested date window is applied locally.
Only a completely successful fetch is published for the downstream pipeline.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import time
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

import requests

from source_config import load_config_with_source_migration
from subscription_plan import build_pipeline_inputs


ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
MAX_RESULTS_PER_KEYWORD = 200


def keyword_queries(config: dict) -> list[str]:
    """Use original recall keywords, not long semantic intent rewrites."""
    queries = []
    seen = set()
    for query in build_pipeline_inputs(config)["bm25_queries"]:
        if query["type"] != "keyword" or "arxiv" not in query["paper_sources"]:
            continue
        keyword = " ".join(str(query["query_text"]).split())
        if not keyword or keyword.casefold() in seen:
            continue
        # Quote the phrase so API operators/punctuation in a keyword cannot
        # accidentally change the scope of the search.
        queries.append('all:"' + keyword.replace('"', " ") + '"')
        seen.add(keyword.casefold())
    if not queries:
        raise ValueError("No enabled arXiv keywords in the selected subscription; add a keyword first.")
    return queries


def resolve_window(days: int, token: str, now: datetime) -> tuple[datetime, datetime]:
    if not 1 <= days <= 365:
        raise ValueError("days must be between 1 and 365")
    if re.fullmatch(r"\d{8}-\d{8}", token):
        start, end = [datetime.strptime(x, "%Y%m%d").replace(tzinfo=timezone.utc)
                      for x in token.split("-")]
        if start > end:
            raise ValueError("Invalid run date range")
        return start, min(end + timedelta(days=1), now)
    return now - timedelta(days=days), now


def parse_feed(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    if root.tag != f"{{{NS['a']}}}feed":
        raise ValueError("arXiv returned an invalid Atom feed")
    papers = []
    for entry in root.findall("a:entry", NS):
        entry_id = entry.findtext("a:id", "", NS).strip()
        if "/api/errors" in entry_id:
            raise ValueError("arXiv API error: " + entry.findtext("a:summary", "unknown error", NS))
        pid = entry_id.split("/abs/", 1)[-1]
        if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-zA-Z.-]+/\d{7})(?:v\d+)?", pid):
            raise ValueError("arXiv returned an invalid paper ID")
        published = entry.findtext("a:published", "", NS)
        # Fail on malformed dates instead of silently losing candidates.
        datetime.fromisoformat(published.replace("Z", "+00:00"))
        title = " ".join(entry.findtext("a:title", "", NS).split())
        abstract = " ".join(entry.findtext("a:summary", "", NS).split())
        if not title or not abstract:
            raise ValueError(f"arXiv returned incomplete metadata for {pid}")
        primary = entry.find("arxiv:primary_category", NS)
        pdf = next((link.get("href") for link in entry.findall("a:link", NS)
                    if link.get("title") == "pdf"), None)
        papers.append({
            "id": pid,
            "source": "arxiv",
            "title": title,
            "abstract": abstract,
            "authors": [a.findtext("a:name", "", NS) for a in entry.findall("a:author", NS)],
            "primary_category": primary.get("term", "") if primary is not None else "",
            "categories": [c.get("term", "") for c in entry.findall("a:category", NS)],
            "published": published,
            "link": pdf or f"https://arxiv.org/pdf/{pid}",
        })
    return papers


class ArxivClient:
    def __init__(self, session=None, *, sleep=time.sleep, clock=time.monotonic):
        self.session = session or requests.Session()
        self.sleep = sleep
        self.clock = clock
        self.last_request: float | None = None

    def search(self, query: str) -> list[dict]:
        for attempt in range(3):
            if self.last_request is not None:
                self.sleep(max(0, 3.1 - (self.clock() - self.last_request)))
            self.last_request = self.clock()
            try:
                response = self.session.get(
                    API_URL,
                    params={"search_query": query, "start": 0,
                            "max_results": MAX_RESULTS_PER_KEYWORD,
                            "sortBy": "submittedDate", "sortOrder": "descending"},
                    headers={"User-Agent": "daily-paper-reader/1.0 (subscription metadata reader)"},
                    timeout=(10, 60),
                )
            except requests.RequestException as exc:
                if attempt == 2:
                    raise RuntimeError(f"arXiv request failed for {query}: {type(exc).__name__}") from exc
                self.sleep(10 * (attempt + 1))
                continue
            if response.status_code == 429 or 500 <= response.status_code < 600:
                if attempt == 2:
                    raise RuntimeError(f"arXiv request failed for {query}: HTTP {response.status_code}")
                try:
                    delay = float(response.headers.get("Retry-After", ""))
                except ValueError:
                    delay = 10 * (attempt + 1)
                if delay > 60:
                    raise RuntimeError(f"arXiv requested a long retry delay for {query}; try again later")
                print(f"[arXiv] HTTP {response.status_code}; retry {attempt + 1}/2", flush=True)
                self.sleep(max(3.1, delay))
                continue
            response.raise_for_status()
            return parse_feed(response.content)
        raise AssertionError("unreachable")


def fetch(config: dict, *, days: int, token: str, output: Path,
          client=None, now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    start, end = resolve_window(days, token, now)
    queries = keyword_queries(config)
    client = client or ArxivClient()
    papers = {}
    print(f"[arXiv] Direct fetch: {len(queries)} keywords; first submitted in [{start}, {end})", flush=True)
    print(f"[arXiv] Bounded recall: latest {MAX_RESULTS_PER_KEYWORD} candidates per keyword", flush=True)
    for query in queries:
        candidates = client.search(query)
        count = 0
        for paper in candidates:
            published = datetime.fromisoformat(paper["published"].replace("Z", "+00:00"))
            if start <= published < end:
                papers[paper["id"]] = paper
                count += 1
        print(f"[arXiv] {query}: {len(candidates)} candidates, {count} in window", flush=True)
        if len(candidates) >= MAX_RESULTS_PER_KEYWORD:
            print(f"[arXiv] Candidate cap reached for {query}; this is not an exhaustive search", flush=True)
    result = sorted(papers.values(), key=lambda p: p["published"], reverse=True)
    # Publish only after every request succeeds. Do not update global crawl/seen
    # state: downstream recommendation selection owns the reading history.
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(output)
    print(f"[arXiv] Saved {len(result)} unique papers to {output}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ignore-seen", action="store_true", help="Accepted for pipeline compatibility; fetch always uses the full requested window")
    args = parser.parse_args()
    config = load_config_with_source_migration(os.getenv("DPR_CONFIG_FILE") or str(ROOT / "config.yaml"), write_back=False)
    days = args.days if args.days is not None else int((config.get("arxiv_paper_setting") or {}).get("days_window") or 9)
    now = datetime.now(timezone.utc)
    token = os.getenv("DPR_RUN_DATE") or now.strftime("%Y%m%d")
    if not re.fullmatch(r"\d{8}(?:-\d{8})?", token):
        raise ValueError("Invalid DPR_RUN_DATE")
    output = args.output or ROOT / "archive" / token / "raw" / f"arxiv_papers_{token}.json"
    fetch(config, days=days, token=token, output=output, now=now)


if __name__ == "__main__":
    main()
