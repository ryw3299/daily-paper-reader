"""Regression coverage for failed retrieval being mistaken for an empty result."""

from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def backend():
    return {
        "enabled": True, "url": "https://example.invalid", "anon_key": "test-key",
        "use_bm25_rpc": True, "bm25_rpc": "match_arxiv_papers_bm25",
        "use_vector_rpc": True, "vector_rpc_exact": "match_arxiv_papers_exact",
        "vector_rpc": "match_arxiv_papers_exact", "papers_table": "arxiv_papers",
    }


def query():
    return {
        "type": "intent_query", "query_text": "asymmetric TSP", "tag": "ATSP",
        "paper_tag": "query:ATSP", "paper_sources": ["arxiv"],
        "query_embedding": [1.0, 0.0, 0.0],
    }


class DailyRetrievalFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bm25 = load_module("strict_bm25", "2.1.retrieval_papers_bm25.py")
        cls.vector = load_module("strict_vector", "2.2.retrieval_papers_embedding.py")

    def lanes(self):
        return [(self.bm25, "match_papers_by_bm25", "bm25"),
                (self.vector, "match_papers_by_embedding", "embedding")]

    def run_stage(self, module, rpc_name, lane, root, response, count=1, raw=False, multi=False):
        raw_dir, filtered_dir = root / "raw", root / "filtered"
        if raw:
            raw_dir.mkdir(exist_ok=True)
            (raw_dir / "arxiv_papers_test.json").write_text("[]", encoding="utf-8")
        cfg = {"arxiv_paper_setting": {"prefer_supabase_read": True},
               "source_backends": {"arxiv": backend()}}
        queries = [query()]
        if multi:
            cfg["source_backends"]["biorxiv"] = backend()
            queries[0]["paper_sources"] = ["arxiv", "biorxiv"]
        output = filtered_dir / f"arxiv_papers_test.{lane}.json"
        with ExitStack() as stack:
            stack.enter_context(patch.dict(os.environ, {"DPR_ENABLE_MULTI_SOURCE_RPC": "1" if multi else "0"}, clear=True))
            stack.enter_context(patch.object(sys, "argv", ["retrieval.py"]))
            for name, value in [("RAW_DIR", str(raw_dir)), ("FILTERED_DIR", str(filtered_dir)),
                                ("TODAY_STR", "test")]:
                stack.enter_context(patch.object(module, name, value))
            stack.enter_context(patch.object(module, "load_config", return_value=cfg))
            stack.enter_context(patch.object(module, "build_pipeline_inputs", return_value={
                "bm25_queries": queries, "embedding_queries": queries}))
            stack.enter_context(patch.object(module, "count_papers_by_date_range",
                                            return_value=(count, "count 查询失败" if count is None else "count 查询成功")))
            rpc = stack.enter_context(patch.object(module, rpc_name, return_value=response))
            stack.enter_context(patch.object(module, "load_paper_pool", side_effect=AssertionError("unexpected local fallback")))
            if lane == "embedding":
                stack.enter_context(patch.object(module, "hydrate_query_embeddings_from_config", return_value={}))
            module.main()
        return output, rpc

    def test_database_failures_raise_even_when_local_input_exists(self):
        for module, rpc_name, lane in self.lanes():
            for message in ["rpc 查询异常：DNS lookup failed", "rpc 查询失败：HTTP 401",
                            'rpc 查询失败：HTTP 500 {"code":"57014"}', "rpc 查询结果格式异常"]:
                with self.subTest(lane=lane, message=message), tempfile.TemporaryDirectory() as tmp:
                    with self.assertRaises(RuntimeError):
                        self.run_stage(module, rpc_name, lane, Path(tmp), ([], message), raw=True)
                    self.assertFalse((Path(tmp) / "filtered" / f"arxiv_papers_test.{lane}.json").exists())

    def test_successful_zero_hits_write_empty_results_without_local_fallback(self):
        for module, rpc_name, lane in self.lanes():
            for raw in [False, True]:
                with self.subTest(lane=lane, raw=raw), tempfile.TemporaryDirectory() as tmp:
                    path, rpc = self.run_stage(module, rpc_name, lane, Path(tmp), ([], "rpc 查询成功：0 条"), raw=raw)
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    self.assertEqual(payload["papers"], [])
                    self.assertEqual(len(payload["queries"]), 1)
                    self.assertEqual(payload["queries"][0]["sim_scores"], {})
                    self.assertTrue(rpc.called)

    def test_count_failure_stops_before_rpc(self):
        for module, rpc_name, lane in self.lanes():
            with self.subTest(lane=lane), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(RuntimeError):
                    self.run_stage(module, rpc_name, lane, Path(tmp), ([], "rpc 查询成功"), count=None)

    def test_multi_source_zero_hits_are_complete_but_errors_stop_the_stage(self):
        for module, rpc_name, lane in self.lanes():
            with self.subTest(lane=lane), tempfile.TemporaryDirectory() as tmp:
                path, rpc = self.run_stage(module, rpc_name, lane, Path(tmp), ([], "rpc 查询成功：0 条"), multi=True)
                self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["papers"], [])
                self.assertTrue(all(call.kwargs["rpc_name"].startswith("match_multi_source") for call in rpc.call_args_list))
            with self.subTest(lane=lane), tempfile.TemporaryDirectory() as tmp, self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                self.run_stage(module, rpc_name, lane, Path(tmp), ([], "rpc 查询失败：HTTP 403"), multi=True)

    def test_successful_hits_still_produce_papers(self):
        for module, rpc_name, lane in self.lanes():
            with self.subTest(lane=lane), tempfile.TemporaryDirectory() as tmp:
                path, _ = self.run_stage(module, rpc_name, lane, Path(tmp),
                    ([{"id": "p1", "title": "TSP paper", "score": 1, "similarity": 0.9}], "rpc 查询成功：1 条"))
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual([paper["id"] for paper in payload["papers"]], ["p1"])
                self.assertIn("p1", payload["queries"][0]["sim_scores"])

    def test_partial_shards_are_not_success(self):
        start = datetime(2026, 3, 1, tzinfo=timezone.utc)
        for module, rpc_name, lane in self.lanes():
            response = [([{"id": "p1", "score": 1, "similarity": 1}], "rpc 查询成功：1 条"),
                        ([], "rpc 查询失败：HTTP 403")]
            kwargs = dict(url="https://example.invalid", api_key="test-key", rpc_name="test",
                          match_count=10, schema="public", start_dt=start,
                          end_dt=start + timedelta(days=2), time_fields=("published",), shard_days=1)
            if lane == "bm25":
                kwargs.update(query_text="TSP")
            else:
                kwargs.update(query_embedding=[1.0])
            call = module.query_supabase_bm25_with_shards if lane == "bm25" else module.query_supabase_vector_with_shards
            with self.subTest(lane=lane), patch.object(module, rpc_name, side_effect=response):
                rows, message = call(**kwargs)
                self.assertEqual(rows, [])
                self.assertIn("分片查询失败", message)
                self.assertIn("HTTP 403", message)

    def test_rank_rejects_partial_result_before_returning_any_hits(self):
        for module, _, lane in self.lanes():
            helper = "query_supabase_bm25_with_shards" if lane == "bm25" else "query_supabase_vector_with_shards"
            kwargs = dict(queries=[query()], top_k=10, supabase_conf=backend())
            if lane == "embedding":
                kwargs.update(model=None, rpc_mode="exact")
            with self.subTest(lane=lane), patch.object(module, helper, return_value=([], "rpc 分片查询失败：HTTP 403")):
                with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                    module.rank_papers_for_queries_via_supabase(**kwargs)


class ResponseFormatTests(unittest.TestCase):
    def test_null_objects_and_invalid_rows_are_errors_not_zero_hits(self):
        import supabase_source as source
        calls = [(source.match_papers_by_bm25, {"rpc_name": "bm25", "query_text": "TSP", "match_count": 10}),
                 (source.match_papers_by_embedding, {"rpc_name": "vector", "query_embedding": [1.0], "match_count": 10}),
                 (source.fetch_papers_by_date_range, {"papers_table": "arxiv_papers",
                    "start_dt": datetime(2026, 3, 1, tzinfo=timezone.utc),
                    "end_dt": datetime(2026, 3, 2, tzinfo=timezone.utc)})]
        for call, kwargs in calls:
            for body in [None, {}, "", [None], [{}], []]:
                with self.subTest(call=call.__name__, body=body):
                    response = Mock(status_code=200)
                    response.json.return_value = body
                    with patch.object(source, "_request_with_retries", return_value=response):
                        rows, message = call(url="https://example.invalid", api_key="test", **{
                            "start_dt": datetime(2026, 3, 1, tzinfo=timezone.utc),
                            "end_dt": datetime(2026, 3, 2, tzinfo=timezone.utc), **kwargs})
                    self.assertEqual(rows, [])
                    self.assertIn("查询成功" if body == [] else "格式异常", message)


class RequiredArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = load_module("strict_main", "main.py")
        cls.rrf = load_module("strict_rrf", "2.3.retrieval_papers_rrf.py")

    def test_a_success_exit_without_new_output_cannot_reuse_old_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "old.json"
            output.write_text('{"papers": [], "queries": []}', encoding="utf-8")
            with patch.object(self.main, "run_step"), self.assertRaises(FileNotFoundError):
                self.main.run_data_step("BM25", [], str(output))

    def test_malformed_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bad.json"
            def write_bad(*args, **kwargs):
                output.write_text('{"papers": {}}', encoding="utf-8")
            with patch.object(self.main, "run_step", side_effect=write_bad), self.assertRaises(ValueError):
                self.main.run_data_step("BM25", [], str(output))

    def test_rrf_missing_either_lane_is_an_error_even_if_old_output_exists(self):
        for present in [None, "bm25", "embedding"]:
            with self.subTest(present=present), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for lane in ["bm25", "embedding"]:
                    if lane == present:
                        (root / f"{lane}.json").write_text('{"papers": [], "queries": []}', encoding="utf-8")
                output = root / "out.json"
                output.write_text("old", encoding="utf-8")
                args = ["rrf.py", "--bm25-input", str(root / "bm25.json"),
                        "--embedding-input", str(root / "embedding.json"), "--output", str(output)]
                with patch.object(sys, "argv", args), self.assertRaises(FileNotFoundError):
                    self.rrf.main()

    def test_rrf_accepts_two_valid_empty_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for lane in ["bm25", "embedding"]:
                (root / f"{lane}.json").write_text('{"papers": [], "queries": []}', encoding="utf-8")
            output = root / "out.json"
            args = ["rrf.py", "--bm25-input", str(root / "bm25.json"),
                    "--embedding-input", str(root / "embedding.json"), "--output", str(output)]
            with patch.object(sys, "argv", args):
                self.rrf.main()
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["papers"], [])


class ForcedFetchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Other maintenance tests put src/maintain/arxiv.py on sys.path; isolate the crawler dependency.
        with patch.dict(sys.modules, {"arxiv": Mock()}):
            cls.fetch = load_module("strict_fetch_arxiv", "maintain/fetchers/fetch_arxiv.py")

    def test_forced_database_fetch_does_not_fall_back_or_advance_state_on_failure(self):
        for message in ["papers 查询异常：DNS failure", "papers 查询失败：HTTP 401", "papers 查询结果格式异常"]:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
                output = Path(tmp) / "raw.json"
                output.write_text('[{"id": "old"}]', encoding="utf-8")
                stack.enter_context(patch.object(self.fetch, "load_config", return_value={}))
                stack.enter_context(patch.object(self.fetch, "get_supabase_read_config", return_value=backend()))
                stack.enter_context(patch.object(self.fetch, "fetch_papers_by_date_range", return_value=([], message)))
                stack.enter_context(patch.object(self.fetch, "fetch_recent_papers", return_value=([], message)))
                state = stack.enter_context(patch.object(self.fetch, "save_last_crawl_at"))
                stack.enter_context(patch.object(self.fetch, "load_seen_state", side_effect=AssertionError("local fallback")))
                with self.assertRaises(RuntimeError):
                    self.fetch.fetch_all_domains_metadata_robust(days=1, output_file=str(output))
                state.assert_not_called()
                self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [{"id": "old"}])

    def test_forced_database_zero_hits_replace_old_raw_without_local_fetch(self):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            output = Path(tmp) / "raw.json"
            output.write_text('[{"id": "old"}]', encoding="utf-8")
            stack.enter_context(patch.object(self.fetch, "load_config", return_value={}))
            stack.enter_context(patch.object(self.fetch, "get_supabase_read_config", return_value=backend()))
            stack.enter_context(patch.object(self.fetch, "fetch_papers_by_date_range", return_value=([], "papers 查询成功：0 条")))
            stack.enter_context(patch.object(self.fetch, "fetch_recent_papers", return_value=([], "papers 查询成功：0 条")))
            state = stack.enter_context(patch.object(self.fetch, "save_last_crawl_at"))
            stack.enter_context(patch.object(self.fetch, "load_seen_state", side_effect=AssertionError("local fallback")))
            self.fetch.fetch_all_domains_metadata_robust(days=1, output_file=str(output))
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), [])
            state.assert_called_once()

    def test_explicit_ingestion_disable_still_uses_local_fetch(self):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            stack.enter_context(patch.object(self.fetch, "load_config", return_value={}))
            stack.enter_context(patch.object(self.fetch, "get_supabase_read_config", return_value=backend()))
            fetch_db = stack.enter_context(patch.object(self.fetch, "fetch_papers_by_date_range"))
            stack.enter_context(patch.object(self.fetch, "load_seen_state", return_value=(set(), None)))
            stack.enter_context(patch.object(self.fetch, "load_last_crawl_at", return_value=None))
            stack.enter_context(patch.object(self.fetch, "save_last_crawl_at"))
            stack.enter_context(patch.object(self.fetch, "save_seen_state"))
            stack.enter_context(patch.object(self.fetch, "arxiv"))
            category = stack.enter_context(patch.object(self.fetch, "fetch_category_in_windows", return_value=None))
            self.fetch.fetch_all_domains_metadata_robust(days=1, output_file=str(Path(tmp) / "raw.json"), disable_supabase_read=True)
            fetch_db.assert_not_called()
            self.assertEqual(category.call_count, len(self.fetch.CATEGORIES_TO_FETCH))


class TopicFailureTests(unittest.TestCase):
    def test_all_topic_modes_fail_without_publishing_or_changing_daily_state(self):
        import topic_research as research
        import starter_pack_retrieval as retrieval
        cfg = {"source_backends": {"arxiv": backend()}, "subscriptions": {"intent_profiles": [{
            "tag": "ATSP", "enabled": True, "keywords": ["ATSP"], "intent_queries": [], "paper_sources": ["arxiv"]}]}}
        for mode in ["90", "365", "starter"]:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
                root = Path(tmp)
                docs = root / "docs"
                docs.mkdir()
                (docs / "README.md").write_text("existing report", encoding="utf-8")
                carryover = root / "archive" / "carryover.json"
                carryover.parent.mkdir()
                carryover.write_text("existing state", encoding="utf-8")
                stack.enter_context(patch.dict(os.environ, {"DPR_STARTER_RETRIEVAL_WORKERS": "1"}))
                stack.enter_context(patch.object(retrieval, "_vector", return_value=[1.0] * 384))
                stack.enter_context(patch("conference_retrieval.resolve_unified_conference_backend", return_value=backend()))
                def match(**kwargs):
                    # Starter must propagate a conference error after successful arXiv tasks.
                    if mode == "starter" and "extra_payload" not in kwargs:
                        return [], "rpc 查询成功：0 条"
                    return [], "rpc 查询失败：HTTP 403"
                stack.enter_context(patch.object(retrieval, "match_papers_by_bm25", side_effect=match))
                stack.enter_context(patch.object(retrieval, "match_papers_by_embedding", side_effect=match))
                with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
                    research.run_research(cfg, "ATSP", mode, "2026-09-11", root, conferences=["icml"])
                self.assertEqual((docs / "README.md").read_text(encoding="utf-8"), "existing report")
                self.assertEqual(carryover.read_text(encoding="utf-8"), "existing state")
                self.assertFalse(list((docs / "starter-pack").glob("*/index.json")))
                manifests = list((root / ".local-runs").glob("**/manifest.json"))
                self.assertTrue(manifests)
                self.assertTrue(all(json.loads(p.read_text(encoding="utf-8"))["status"] == "failed" for p in manifests))


if __name__ == "__main__":
    unittest.main()
