"""自建研究库必须完整分页；任何失败窗口都不能变成成功的空论文池。"""

from datetime import datetime, timezone
from unittest.mock import Mock, patch

import pytest

from src.maintain.fetchers import fetch_arxiv as fetcher


WINDOW = (datetime(2026, 11, 1, tzinfo=timezone.utc), datetime(2026, 11, 8, tzinfo=timezone.utc))


def test_research_ingest_uses_full_pagination_and_preserves_date_window():
    client = Mock()
    client.results.return_value = []
    fetcher.fetch_category_in_windows(client, "research-scope", [WINDOW], set(), {}, query_filter='all:"knowledge graph"')
    search = client.results.call_args.args[0]
    assert search.max_results is None
    assert search.query == '(all:"knowledge graph") AND submittedDate:[202611010000 TO 202611080000]'


def test_default_ingest_keeps_existing_category_query():
    client = Mock()
    client.results.return_value = []
    fetcher.fetch_category_in_windows(client, "cs", [WINDOW], set(), {})
    assert client.results.call_args.args[0].query.startswith("cat:cs* AND submittedDate:")


def test_split_retry_keeps_the_research_scope():
    client = Mock()
    client.results.side_effect = [RuntimeError("large window"), [], []]
    fetcher.fetch_category_in_windows(client, "research-scope", [WINDOW], set(), {}, query_filter='all:"GraphRAG"')
    assert client.results.call_count == 3
    assert all(call.args[0].query.startswith('(all:"GraphRAG") AND ') for call in client.results.call_args_list)


def test_exhausted_window_failure_does_not_publish_or_advance_state(tmp_path):
    output = tmp_path / "raw.json"
    output.write_text('[{"id":"previous"}]', encoding="utf-8")
    client = Mock()
    client.results.side_effect = RuntimeError("offline")
    config = {"arxiv_paper_setting": {"ingest_query": 'all:"GraphRAG"'}}
    with (
        patch.object(fetcher, "load_config", return_value=config),
        patch.object(fetcher, "get_supabase_read_config", return_value={"enabled": False}),
        patch.object(fetcher.arxiv, "Client", return_value=client),
        patch.object(fetcher, "save_seen_state") as seen,
        patch.object(fetcher, "save_last_crawl_at") as watermark,
    ):
        with pytest.raises(RuntimeError, match="抓取窗口失败"):
            fetcher.fetch_all_domains_metadata_robust(days=1, output_file=str(output), ignore_seen=True)
    assert output.read_text(encoding="utf-8") == '[{"id":"previous"}]'
    seen.assert_not_called()
    watermark.assert_not_called()
