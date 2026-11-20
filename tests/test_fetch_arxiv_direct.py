from datetime import datetime, timezone
from pathlib import Path
import sys
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fetch_arxiv_direct import ArxivClient, fetch, keyword_queries, parse_feed, resolve_window
from main import resolve_arxiv_fetch_script


NOW = datetime(2026, 11, 20, tzinfo=timezone.utc)
CONFIG = {"subscriptions": {"intent_profiles": [{
    "tag": "graph", "enabled": True, "paper_sources": ["arxiv"],
    "keywords": [{"keyword": "knowledge graph", "query": "A long semantic rewrite"}],
    "intent_queries": [{"query": "How do agents reason with knowledge?"}],
}]}}


def feed(published="2026-11-15T00:00:00Z", updated="2026-11-19T00:00:00Z"):
    return f'''<feed xmlns="http://www.w3.org/2005/Atom"
        xmlns:arxiv="http://arxiv.org/schemas/atom">
      <entry><id>http://arxiv.org/abs/2611.12345v2</id>
        <title>Knowledge Graph\n Agents</title><summary>A real abstract.</summary>
        <published>{published}</published><updated>{updated}</updated>
        <author><name>Researcher</name></author><category term="cs.AI"/>
        <arxiv:primary_category term="cs.AI"/>
        <link title="pdf" href="https://arxiv.org/pdf/2611.12345v2"/>
      </entry></feed>'''.encode()


def test_original_keywords_selected_by_enabled_arxiv_profile(monkeypatch):
    import copy
    config = copy.deepcopy(CONFIG)
    config["subscriptions"]["intent_profiles"].extend([
        {"tag": "off", "enabled": False, "paper_sources": ["arxiv"], "keywords": ["ignored"]},
        {"tag": "conference", "paper_sources": ["icml"], "keywords": ["ignored"]},
        {"tag": "other", "paper_sources": ["arxiv"], "keywords": ["other"]},
    ])
    config["subscriptions"]["intent_profiles"][0]["keywords"].extend([
        {"keyword": "disabled", "enabled": False}, {"keyword": "Knowledge Graph"},
    ])
    monkeypatch.setenv("DPR_FILTER_PROFILE_TAG", "graph")
    assert keyword_queries(config) == ['all:"knowledge graph"']


@pytest.mark.parametrize("status", [429, 503])
def test_http_failure_cannot_be_reported_as_empty_success(tmp_path, status):
    response = Mock(status_code=status, headers={})
    session = Mock()
    session.get.return_value = response
    client = ArxivClient(session, sleep=lambda _: None)
    output = tmp_path / "raw.json"
    output.write_text('[{"id": "previous-result"}]')
    with pytest.raises(RuntimeError, match=f"HTTP {status}"):
        fetch(CONFIG, days=30, token="20261022-20261120", output=output, client=client, now=NOW)
    assert session.get.call_count == 3
    assert "previous-result" in output.read_text()


def test_api_error_entry_is_failure():
    with pytest.raises(ValueError, match="arXiv API error"):
        parse_feed(b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
            <id>http://arxiv.org/api/errors#incorrect_id_format</id>
            <summary>Invalid query</summary></entry></feed>''')


def test_empty_success_is_valid(tmp_path):
    session = Mock()
    session.get.return_value = Mock(status_code=200, content=b'<feed xmlns="http://www.w3.org/2005/Atom"/>')
    output = tmp_path / "raw.json"
    assert fetch(CONFIG, days=30, token="20261022-20261120", output=output,
                 client=ArxivClient(session), now=NOW) == []
    assert output.read_text() == "[]"


def test_window_uses_first_submission_and_deduplicates(tmp_path):
    import copy
    config = copy.deepcopy(CONFIG)
    config["subscriptions"]["intent_profiles"][0]["keywords"].append("agent security")
    client = Mock()
    recent = parse_feed(feed())
    old = parse_feed(feed(published="2025-11-01T00:00:00Z"))
    old[0]["id"] = "2511.12345v2"
    client.search.return_value = recent + old
    output = tmp_path / "raw.json"
    result = fetch(config, days=30, token="20261022-20261120", output=output, client=client, now=NOW)
    assert len(result) == 1
    assert result[0]["id"] == "2611.12345v2"
    assert result[0]["published"] == "2026-11-15T00:00:00Z"
    assert result[0]["primary_category"] == "cs.AI"
    assert result[0]["title"] == "Knowledge Graph Agents"
    assert client.search.call_count == 2


def test_all_requests_must_succeed_before_writing(tmp_path):
    import copy
    config = copy.deepcopy(CONFIG)
    config["subscriptions"]["intent_profiles"][0]["keywords"].append("agent security")
    client = Mock()
    client.search.side_effect = [parse_feed(feed()), RuntimeError("offline")]
    output = tmp_path / "raw.json"
    with pytest.raises(RuntimeError, match="offline"):
        fetch(config, days=30, token="20261022-20261120", output=output, client=client, now=NOW)
    assert not output.exists()


def test_request_spacing_and_retry_after():
    response = Mock(status_code=429, headers={"Retry-After": "12"})
    success = Mock(status_code=200, content=b'<feed xmlns="http://www.w3.org/2005/Atom"/>')
    session = Mock()
    session.get.side_effect = [response, success, success]
    sleeps = []
    client = ArxivClient(session, sleep=sleeps.append, clock=lambda: 100)
    assert client.search("all:test") == []
    assert client.search("all:other") == []
    assert 12 in sleeps
    assert sleeps.count(3.1) == 2
    params = session.get.call_args.kwargs["params"]
    assert params["sortBy"] == "submittedDate"
    assert "submittedDate:" not in params["search_query"]


def test_window_and_main_routing():
    start, end = resolve_window(9, "20261120", NOW)
    assert start.day == 11 and end == NOW
    start, end = resolve_window(30, "20261022-20261120", NOW)
    assert start.month == 10 and start.day == 22 and end == NOW
    assert Path(resolve_arxiv_fetch_script({"source_backends": {"arxiv": {"enabled": False}}})).name == "fetch_arxiv_direct.py"
    assert Path(resolve_arxiv_fetch_script({"source_backends": {"arxiv": {"enabled": True}}})).name == "fetch_arxiv.py"
