#!/usr/bin/env python
"""Dispatch conference maintenance sequentially; preview payloads by default.

Set GH_TOKEN (or GITHUB_TOKEN) to a token with repository Actions write access.
Example: python scripts/trigger_conference_maintenance.py --repo OWNER/REPO --ref main --execute

The workflow uses GitHub Secrets, not the local .env. Forks also need the
DPR_MAINTAIN_OWN_SUPABASE repository variable set to true. Push the year fixes
to the selected ref before executing. The workflow must exist on the default branch.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


WORKFLOW = "maintain-supabase.yml"
API_VERSION = "2026-03-10"
TARGETS = (
    ("neurips", "2023,2024,2025"),
    ("iclr", "2023,2024,2025"),
    ("icml", "2023,2024,2025"),
    ("aaai", "2023,2024,2025"),
    ("cvpr", "2023,2024,2025"),
    ("eccv", "2022,2024,2026"),
    ("ijcai", "2023,2024,2025"),
    ("acl", "2023,2024,2025"),
    ("emnlp", "2023,2024,2025"),
)


def github_request(token: str, method: str, resource: str, payload: dict | None = None) -> dict:
    request = Request(
        "https://api.github.com" + resource,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "daily-paper-reader-maintenance",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            body = response.read()
    except HTTPError as exc:
        raise RuntimeError(f"GitHub {method} {resource}: HTTP {exc.code} {exc.reason}") from None
    except URLError as exc:
        raise RuntimeError(f"GitHub {method} {resource}: {exc.reason}") from None
    return json.loads(body) if body else {}


def build_payload(ref: str, conference: str, years: str) -> dict:
    return {
        "ref": ref,
        "inputs": {"maintain_target": "conference", "conference": conference, "years": years},
    }


def wait_for_success(token: str, repo: str, run_id: int, poll_seconds: int, timeout_minutes: int) -> None:
    resource = f"/repos/{repo}/actions/runs/{run_id}"
    deadline = time.monotonic() + timeout_minutes * 60
    while True:
        run = github_request(token, "GET", resource)
        if run.get("status") == "completed":
            if run.get("conclusion") != "success":
                raise RuntimeError(f"Run {run_id} ended with {run.get('conclusion')}; batch stopped")
            jobs = github_request(token, "GET", resource + "/jobs?per_page=100").get("jobs", [])
            if not jobs or any(job.get("conclusion") != "success" for job in jobs):
                raise RuntimeError(
                    f"Run {run_id} did not execute all jobs successfully; check "
                    "DPR_MAINTAIN_OWN_SUPABASE and workflow job conditions"
                )
            print(f"Completed run {run_id}", flush=True)
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise RuntimeError(f"Timed out waiting for run {run_id}; batch stopped")
        time.sleep(min(poll_seconds, remaining))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub repository as OWNER/REPO")
    parser.add_argument("--ref", default="main", help="Branch or tag containing the fixes")
    parser.add_argument("--conference", nargs="+", choices=[name for name, _ in TARGETS])
    parser.add_argument("--execute", action="store_true", help="Submit runs and wait for each to succeed")
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--timeout-minutes", type=int, default=180, help="Wait limit per conference")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        parser.error("--repo must be OWNER/REPO")
    if args.poll_seconds <= 0 or args.timeout_minutes <= 0:
        parser.error("Polling interval and timeout must be positive")

    targets = [(name, years) for name, years in TARGETS if not args.conference or name in args.conference]
    token = (os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()
    if args.execute and not token:
        parser.error("Set GH_TOKEN or GITHUB_TOKEN before using --execute")

    workflow_resource = f"/repos/{args.repo}/actions/workflows/{quote(WORKFLOW, safe='')}"
    if args.execute:
        workflow = github_request(token, "GET", workflow_resource)
        if workflow.get("state") != "active":
            raise RuntimeError("Maintenance workflow is not active")

    for conference, years in targets:
        payload = build_payload(args.ref, conference, years)
        if not args.execute:
            print(json.dumps(payload))
            continue
        # The shared concurrency group allows only one pending run. Wait before
        # dispatching another conference so this batch cannot replace its own runs.
        result = github_request(token, "POST", workflow_resource + "/dispatches", payload)
        run_id = result.get("workflow_run_id")
        if not isinstance(run_id, int) or run_id <= 0:
            raise RuntimeError("Dispatch returned no run ID; check Actions before retrying")
        print(f"Dispatched {conference} {years}: {result.get('html_url', run_id)}", flush=True)
        wait_for_success(token, args.repo, run_id, args.poll_seconds, args.timeout_minutes)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
