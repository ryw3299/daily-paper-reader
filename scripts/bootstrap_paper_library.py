"""按依赖顺序合并现有 SQL，供新 Supabase 项目的 SQL Editor 执行。"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFERENCES = (
    "neurips_openreview", "icml_openreview", "iclr_openreview", "aaai",
    "acl", "emnlp", "cvpr", "eccv", "ijcai", "osdi", "sosp", "ieee_sp", "ndss",
)


def build_sql(*, arxiv_only: bool = False) -> str:
    names = ["create_arxiv_papers_schema.sql", "match_arxiv_papers.sql"]
    if not arxiv_only:
        names += [f"create_{key}_papers_schema.sql" for key in CONFERENCES]
        names += [f"match_{key}_papers.sql" for key in CONFERENCES]
        names += [
            "create_conference_papers_unified.sql",
            "enable_conference_anon_read_policies.sql",
            "create_conference_year_stats_schema.sql",
        ]
    parts = [
        "-- Personal paper library: existing tables and retrieval RPCs.\n"
        "-- Run as the project owner in Supabase SQL Editor.\n"
        "set search_path = public, extensions;\n"
    ]
    for name in names:
        parts.append(f"-- BEGIN {name}\n" + (ROOT / "sql" / name).read_text(encoding="utf-8"))
    parts.append(
        "grant execute on function public.match_arxiv_papers_exact(vector, int, timestamptz, timestamptz) to anon, authenticated;\n"
        "grant execute on function public.match_arxiv_papers_bm25(text, int, timestamptz, timestamptz) to anon, authenticated;\n"
    )
    # 新项目可关闭自动 API 授权，因此显式授予维护程序所需的写权限。
    # anon/authenticated 的只读权限仍由各表原有 RLS 策略控制。
    for table in ["arxiv_papers"] + (
        [f"{key}_papers" for key in CONFERENCES] + ["conference_year_stats"]
        if not arxiv_only else []
    ):
        parts.append(f"grant all on public.{table} to service_role;\n")
    parts.append("notify pgrst, 'reload schema';\n")
    return "\n\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-only", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / ".local-runs/paper-library/bootstrap.sql")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_sql(arxiv_only=args.arxiv_only), encoding="utf-8")
    print(f"SQL written: {args.output.resolve()}")
    print("Only SQL generation completed; no database was modified.")


if __name__ == "__main__":
    main()
