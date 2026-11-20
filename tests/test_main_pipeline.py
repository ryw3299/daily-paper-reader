import importlib.util
import json
import os
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch


def _load_module():
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    src_path = root / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("main_pipeline_mod", src_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class MainPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def _write_rrf_input(self, root: Path, token: str) -> Path:
        filtered_dir = root / "archive" / token / "filtered"
        filtered_dir.mkdir(parents=True, exist_ok=True)
        path = filtered_dir / f"arxiv_papers_{token}.json"
        payload = {
            "generated_at": "2026-03-10T00:00:00+00:00",
            "papers": [
                {"id": "p1", "title": "Paper 1", "abstract": "A"},
                {"id": "p2", "title": "Paper 2", "abstract": "B"},
                {"id": "p3", "title": "Paper 3", "abstract": "C"},
            ],
            "queries": [
                {
                    "type": "intent_query",
                    "tag": "query:test",
                    "paper_tag": "query:test",
                    "query_text": "test query",
                    "sim_scores": {
                        "p1": {"score": 0.9, "rank": 1},
                        "p2": {"score": 0.6, "rank": 2},
                        "p3": {"score": 0.2, "rank": 3},
                    },
                }
            ],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def _stage_writer(self, root, token, calls, payload, fail_at=None):
        stages = {
            "Step 2.1 - BM25": ("filtered", ".bm25.json"),
            "Step 2.2 - Embedding": ("filtered", ".embedding.json"),
            "Step 2.3 - RRF": ("filtered", ".json"),
            "Step 3 - Rerank": ("rank", ".json"),
            "Step 4 - LLM refine": ("rank", ".llm.json"),
        }

        def run(label, args, env=None):
            calls.append((label, args, env))
            if label == fail_at:
                raise RuntimeError("retrieval failed")
            if label in stages:
                directory, suffix = stages[label]
                path = root / "archive" / token / directory / f"arxiv_papers_{token}{suffix}"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(payload), encoding="utf-8")

        return run

    def test_resolve_summary_step_env_uses_summary_overrides(self):
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "base-key",
                "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
                "SUMMARY_API_KEY": "summary-key",
                "SUMMARY_BASE_URL": "https://summary.example.com/v1",
                "SUMMARY_MODEL": "deepseek-v4-flash",
            },
            clear=True,
        ):
            env = self.mod.resolve_summary_step_env()

        self.assertEqual(env["DEEPSEEK_API_KEY"], "summary-key")
        self.assertEqual(env["SUMMARY_API_KEY"], "summary-key")
        self.assertEqual(env["DEEPSEEK_BASE_URL"], "https://summary.example.com/v1")
        self.assertEqual(env["LLM_PRIMARY_BASE_URL"], "https://summary.example.com/v1")
        self.assertEqual(env["DEEPSEEK_MODEL"], "deepseek-v4-flash")

    def test_main_runs_local_rerank_without_remote_rerank_base(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            token = "20260310"
            payload = json.loads(self._write_rrf_input(root, token).read_text(encoding="utf-8"))
            calls = []
            fake_run_step = self._stage_writer(root, token, calls, payload)

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "resolve_run_date_token", return_value=token
            ), patch.object(
                self.mod, "resolve_sidebar_date_label", return_value=None
            ), patch.object(
                self.mod, "parse_trace_ids", return_value=[]
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.object(
                sys, "argv", ["main.py"]
            ), patch.dict(
                os.environ,
                {"LLM_PRIMARY_BASE_URL": "https://api.openai.com/v1"},
                clear=True,
            ):
                self.mod.main()

            labels = [item[0] for item in calls]
            self.assertIn("Step 3 - Rerank", labels)
            self.assertIn("Step 4 - LLM refine", labels)

    def test_main_keeps_local_rerank_in_deepseek_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            token = "20260310"
            payload = json.loads(self._write_rrf_input(root, token).read_text(encoding="utf-8"))
            calls = []
            fake_run_step = self._stage_writer(root, token, calls, payload)

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "resolve_run_date_token", return_value=token
            ), patch.object(
                self.mod, "resolve_sidebar_date_label", return_value=None
            ), patch.object(
                self.mod, "parse_trace_ids", return_value=[]
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.object(
                sys, "argv", ["main.py"]
            ), patch.dict(
                os.environ,
                {"LLM_PRIMARY_BASE_URL": "https://api.deepseek.com"},
                clear=True,
            ):
                self.mod.main()

            labels = [item[0] for item in calls]
            self.assertIn("Step 3 - Rerank", labels)

    def _pipeline_context(self, stack, root, token, run_step):
        for name, value in [("ROOT_DIR", str(root)), ("SRC_DIR", str(root / "src"))]:
            stack.enter_context(patch.object(self.mod, name, value))
        stack.enter_context(patch.object(self.mod, "resolve_run_date_token", return_value=token))
        stack.enter_context(patch.object(self.mod, "resolve_sidebar_date_label", return_value=None))
        stack.enter_context(patch.object(self.mod, "parse_trace_ids", return_value=[]))
        stack.enter_context(patch.object(self.mod, "should_skip_fetch", return_value=True))
        stack.enter_context(patch.object(self.mod, "run_step", side_effect=run_step))
        stack.enter_context(patch.object(sys, "argv", ["main.py"]))
        stack.enter_context(patch.dict(os.environ, {}, clear=True))

    def test_failed_retrieval_stops_before_selection_and_preserves_published_state(self):
        for failed_stage in ["Step 2.1 - BM25", "Step 2.2 - Embedding", "Step 2.3 - RRF"]:
            with self.subTest(stage=failed_stage), tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
                root, token = Path(tmp), "20260310"
                payload = json.loads(self._write_rrf_input(root, token).read_text(encoding="utf-8"))
                protected = [root / "docs" / "README.md", root / "archive" / "carryover.json",
                             root / "archive" / token / "recommend" / f"arxiv_papers_{token}.standard.json"]
                for path in protected:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("existing user state", encoding="utf-8")
                calls = []
                self._pipeline_context(stack, root, token, self._stage_writer(root, token, calls, payload, failed_stage))
                with self.assertRaisesRegex(RuntimeError, "retrieval failed"):
                    self.mod.main()
                labels = [label for label, *_ in calls]
                self.assertNotIn("Step 3 - Rerank", labels)
                self.assertNotIn("Step 5 - Select", labels)
                self.assertNotIn("Step 6 - Generate Docs", labels)
                for path in protected:
                    self.assertEqual(path.read_text(encoding="utf-8"), "existing user state")

    def test_zero_hits_replace_old_scores_and_skip_models_before_selection(self):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            root, token = Path(tmp), "20260310"
            self._write_rrf_input(root, token)
            rank = root / "archive" / token / "rank"
            rank.mkdir()
            for suffix in [".json", ".llm.json"]:
                (rank / f"arxiv_papers_{token}{suffix}").write_text('{"papers": [{"id": "stale"}]}', encoding="utf-8")
            calls = []
            payload = {"papers": [], "queries": [{"query_text": "TSP", "sim_scores": {}}]}
            self._pipeline_context(stack, root, token, self._stage_writer(root, token, calls, payload))
            self.mod.main()
            labels = [label for label, *_ in calls]
            self.assertNotIn("Step 3 - Rerank", labels)
            self.assertNotIn("Step 4 - LLM refine", labels)
            self.assertIn("Step 5 - Select", labels)
            self.assertIn("Step 6 - Generate Docs", labels)
            for suffix in [".json", ".llm.json"]:
                actual = json.loads((rank / f"arxiv_papers_{token}{suffix}").read_text(encoding="utf-8"))
                self.assertEqual(actual["papers"], [])
                self.assertEqual(actual["queries"], payload["queries"])
            self.assertEqual(actual["llm_ranked"], [])


if __name__ == "__main__":
    unittest.main()
