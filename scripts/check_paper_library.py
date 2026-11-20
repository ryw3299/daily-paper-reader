"""实测日常与90/365天窗口的原有数据库检索接口，不调用付费评审模型。"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from local_env import load_local_env
from source_config import get_source_backend, load_config_with_source_migration
from supabase_source import count_papers_by_date_range, match_papers_by_bm25, match_papers_by_embedding


def main() -> None:
    load_local_env()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.yaml")
    parser.add_argument("--days", type=int, nargs="+", default=[9, 90, 365])
    parser.add_argument("--allow-empty", action="store_true", help="仅建表阶段使用，允许空库。")
    args = parser.parse_args()
    if any(not 1 <= days <= 400 for days in args.days):
        parser.error("检查窗口必须在1–400天之间")
    config = load_config_with_source_migration(str(args.config), write_back=False)
    backend = get_source_backend(config, "arxiv")
    if not backend.get("enabled") or not backend.get("url") or not backend.get("anon_key"):
        raise RuntimeError("arxiv 缺少可用 Supabase 后端")
    from model_loader import load_sentence_transformer

    model = load_sentence_transformer("BAAI/bge-small-en-v1.5", device="cpu")
    query = "knowledge graph"
    vector = model.encode(["query: " + query], batch_size=1, normalize_embeddings=True)[0].tolist()
    if len(vector) != 384:
        raise RuntimeError("论文库需要384维向量")
    # 专题研究的截止日期为UTC排他边界，与 research_plan 保持一致。
    end = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    common = {
        "url": backend["url"], "api_key": backend["anon_key"],
        "schema": backend.get("schema") or "public",
    }
    checks = []
    for days in args.days:
        window = {"start_dt": end - timedelta(days=days), "end_dt": end}
        count, message = count_papers_by_date_range(
            **common, **window, papers_table=backend["papers_table"],
        )
        if count is None:
            raise RuntimeError(message)
        keyword_rows, keyword_message = match_papers_by_bm25(
            **common, **window, rpc_name=backend["bm25_rpc"], query_text=query, match_count=3,
        )
        vector_rows, vector_message = match_papers_by_embedding(
            **common, **window, rpc_name=backend["vector_rpc_exact"], query_embedding=vector, match_count=3,
        )
        for status in (keyword_message, vector_message):
            if not status.startswith("rpc 查询成功"):
                raise RuntimeError(status)
        if count and not vector_rows:
            raise RuntimeError(f"{days}天窗口有论文但向量检索为空，请完成 embedding 同步。")
        checks.append({"days": days, "papers": count, "bm25_hits": len(keyword_rows), "vector_hits": len(vector_rows)})
    print(json.dumps({"database": backend["url"], "checks": checks}, ensure_ascii=False, indent=2))
    if not args.allow_empty and not any(item["papers"] for item in checks):
        raise RuntimeError("论文库接口可用但尚未导入论文；不能把空库视为恢复成功。")


if __name__ == "__main__":
    main()
