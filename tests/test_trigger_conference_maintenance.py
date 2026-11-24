import contextlib
import importlib.util
import io
import json
import pathlib
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "trigger_conference_maintenance", ROOT / "scripts/trigger_conference_maintenance.py"
)
batch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(batch)


class BatchConferenceMaintenanceTest(unittest.TestCase):
    def test_preview_covers_exact_requested_conferences_and_years_without_network(self):
        output = io.StringIO()
        with mock.patch.dict(batch.os.environ, {}, clear=True):
            with mock.patch.object(batch, "github_request") as request:
                with contextlib.redirect_stdout(output):
                    self.assertEqual(batch.main(["--repo", "owner/repo"]), 0)
        request.assert_not_called()
        payloads = [json.loads(line) for line in output.getvalue().splitlines()]
        expected = {
            name: "2023,2024,2025"
            for name in ("neurips", "iclr", "icml", "aaai", "cvpr", "ijcai", "acl", "emnlp")
        }
        expected["eccv"] = "2022,2024,2026"
        self.assertEqual(len(payloads), 9)
        self.assertEqual({p["inputs"]["conference"]: p["inputs"]["years"] for p in payloads}, expected)
        self.assertTrue(all(p["ref"] == "main" and p["inputs"]["maintain_target"] == "conference" for p in payloads))

    def test_batch_waits_for_each_run_before_dispatching_next(self):
        active = None
        dispatched = []

        def request(token, method, resource, payload=None):
            nonlocal active
            self.assertEqual(token, "test-token")
            if method == "POST":
                self.assertIsNone(active, "Previous run must complete before another dispatch")
                dispatched.append(payload["inputs"]["conference"])
                active = len(dispatched)
                return {"workflow_run_id": active}
            if resource.endswith(".yml"):
                return {"state": "active"}
            if "/jobs?" in resource:
                self.assertIn(f"/runs/{active}/jobs?", resource)
                active = None
                return {"jobs": [{"conclusion": "success"}]}
            self.assertTrue(resource.endswith(f"/runs/{active}"))
            return {"status": "completed", "conclusion": "success"}

        with mock.patch.dict(batch.os.environ, {"GH_TOKEN": "test-token"}, clear=True):
            with mock.patch.object(batch, "github_request", side_effect=request):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(batch.main(["--repo", "owner/repo", "--execute"]), 0)
        self.assertEqual(len(dispatched), 9)
        self.assertIsNone(active)

    def test_failed_or_skipped_job_stops_batch(self):
        for conclusion, jobs in (("failure", []), ("success", [{"conclusion": "skipped"}])):
            with self.subTest(conclusion=conclusion):
                responses = [
                    {"state": "active"}, {"workflow_run_id": 42},
                    {"status": "completed", "conclusion": conclusion},
                    {"jobs": jobs},
                ]
                with mock.patch.dict(batch.os.environ, {"GH_TOKEN": "test-token"}, clear=True):
                    with mock.patch.object(batch, "github_request", side_effect=responses) as request:
                        with contextlib.redirect_stdout(io.StringIO()):
                            with self.assertRaises(RuntimeError):
                                batch.main(["--repo", "owner/repo", "--execute"])
                self.assertEqual(sum(call.args[1] == "POST" for call in request.call_args_list), 1)

    def test_queued_run_is_polled_until_success(self):
        responses = [
            {"status": "queued"},
            {"status": "completed", "conclusion": "success"},
            {"jobs": [{"conclusion": "success"}]},
        ]
        with mock.patch.object(batch, "github_request", side_effect=responses):
            with mock.patch.object(batch.time, "sleep") as sleep:
                with contextlib.redirect_stdout(io.StringIO()):
                    batch.wait_for_success("token", "owner/repo", 42, 30, 180)
        sleep.assert_called_once_with(30)

    def test_wait_has_a_timeout(self):
        with mock.patch.object(batch, "github_request", return_value={"status": "queued"}):
            with mock.patch.object(batch.time, "monotonic", side_effect=[0, 60]):
                with self.assertRaisesRegex(RuntimeError, "Timed out"):
                    batch.wait_for_success("token", "owner/repo", 42, 30, 1)

    def test_execute_requires_token_without_sending_a_request(self):
        with mock.patch.dict(batch.os.environ, {}, clear=True):
            with mock.patch.object(batch, "github_request") as request:
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        batch.main(["--repo", "owner/repo", "--execute"])
        request.assert_not_called()

    def test_dispatch_sends_current_api_headers_and_json(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"workflow_run_id": 42}'
        payload = batch.build_payload("fix-years", "eccv", "2022,2024,2026")
        with mock.patch.object(batch, "urlopen", return_value=response) as open_url:
            result = batch.github_request(
                "test-token", "POST", "/repos/owner/repo/actions/workflows/maintain-supabase.yml/dispatches", payload
            )
        self.assertEqual(result["workflow_run_id"], 42)
        request = open_url.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(json.loads(request.data), payload)
        self.assertEqual(request.get_header("X-github-api-version"), "2026-03-10")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-token")


if __name__ == "__main__":
    unittest.main()
