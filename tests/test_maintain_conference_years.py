import contextlib
import importlib.util
import io
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
MAINTAIN_DIR = ROOT / "src" / "maintain"
if str(MAINTAIN_DIR) not in sys.path:
    sys.path.insert(0, str(MAINTAIN_DIR))

from common import resolve_target_years


CONFERENCES = ("neurips", "icml", "iclr", "aaai", "cvpr", "eccv", "ijcai", "acl", "emnlp")
YEAR_CASES = (
    ("2024,2026", [2024, 2026]),
    ("2023,2024,2025", [2023, 2024, 2025]),
    ("2022,2024,2026", [2022, 2024, 2026]),
    ("2026,2024,2026", [2026, 2024]),
    (" 2024; 2026, ", [2024, 2026]),
    ("2025", [2025]),
)


def load_script(name):
    spec = importlib.util.spec_from_file_location(
        "conference_years_" + name, MAINTAIN_DIR / (name + ".py")
    )
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {"torch": None}):
        spec.loader.exec_module(module)
    return module


def run_main(module, args):
    with mock.patch.object(sys, "argv", [module.__file__, *args]):
        with contextlib.redirect_stdout(io.StringIO()):
            module.main()


def option(command, name):
    return command[command.index(name) + 1]


class ConferenceYearsTest(unittest.TestCase):
    def test_explicit_years_override_range_without_filling_gaps(self):
        for value, expected in YEAR_CASES:
            with self.subTest(value=value):
                self.assertEqual(
                    resolve_target_years(years=value, year_end=2030, year_count=2),
                    expected,
                )

    def test_empty_years_keep_legacy_range_and_minimum_count(self):
        for value in ("", " ", None):
            for count, expected in ((3, [2023, 2024, 2025]), (0, [2025]), (-1, [2025])):
                with self.subTest(value=value, count=count):
                    self.assertEqual(
                        resolve_target_years(years=value, year_end=2025, year_count=count),
                        expected,
                    )

    def test_invalid_years_are_rejected(self):
        for value in ("2024,nope", "0", "-1", "2024-2026"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    resolve_target_years(years=value, year_end=2026, year_count=3)

    def check_pipeline(self, conference, args, expected):
        wrapper = load_script(conference)
        with mock.patch.object(wrapper, "cleanup_backend"):
            with mock.patch.object(wrapper, "ensure_parent_dir"):
                with mock.patch.object(wrapper, "run_step") as run:
                    run_main(wrapper, [*args, "--skip-cleanup", "--run-date", "20261124"])
        command = run.call_args.args[1]
        expected_csv = ",".join(map(str, expected))
        self.assertEqual(option(command, "--years"), expected_csv)
        self.assertNotIn("--year-count", command)
        raw_path = option(command, "--raw-input")
        self.assertIn("-".join(map(str, expected)) + "_20261124.json", raw_path)

        initializer = load_script("init_" + conference)
        with mock.patch.object(initializer, "run_step") as run:
            run_main(initializer, command[2:])
        self.assertEqual(run.call_count, 2)
        fetch_command = run.call_args_list[0].args[1]
        self.assertEqual(option(fetch_command, "--years"), expected_csv)
        self.assertNotIn("--year-count", fetch_command)
        self.assertEqual(option(fetch_command, "--output"), raw_path)
        self.assertEqual(option(run.call_args_list[1].args[1], "--raw-input"), raw_path)

    def test_explicit_years_reach_fetchers_through_both_entrypoints(self):
        for conference in CONFERENCES:
            for value, expected in YEAR_CASES:
                with self.subTest(conference=conference, value=value):
                    self.check_pipeline(conference, ["--years", value], expected)

    def test_legacy_year_range_reaches_fetchers(self):
        for conference in CONFERENCES:
            for count, expected in ((3, [2023, 2024, 2025]), (0, [2025])):
                with self.subTest(conference=conference, count=count):
                    self.check_pipeline(
                        conference, ["--year-end", "2025", "--year-count", str(count)], expected
                    )

    def test_aaai_fetcher_cli_keeps_explicit_years(self):
        fetcher = load_script("fetchers/fetch_aaai_ojs")
        for value, expected in YEAR_CASES:
            with self.subTest(value=value):
                with mock.patch.object(fetcher, "fetch_aaai_ojs_papers", return_value=[]) as fetch:
                    with mock.patch.object(fetcher, "save_output", return_value="unused.json"):
                        run_main(fetcher, ["--years", value])
                self.assertEqual(fetch.call_args.kwargs["years"], expected)

    def test_initializer_defaults_use_exact_years_in_raw_filename(self):
        for conference in CONFERENCES:
            with self.subTest(conference=conference):
                initializer = load_script("init_" + conference)
                with mock.patch.object(initializer, "run_step") as run:
                    run_main(initializer, ["--years", "2024,2026"])
                command = run.call_args_list[0].args[1]
                self.assertEqual(option(command, "--years"), "2024,2026")
                self.assertTrue(option(command, "--output").endswith("2024-2026.json"))

    def test_skip_fetch_preserves_explicit_raw_input(self):
        for conference in CONFERENCES:
            with self.subTest(conference=conference):
                initializer = load_script("init_" + conference)
                with mock.patch.object(initializer, "run_step") as run:
                    run_main(initializer, ["--years", "2024,2026", "--skip-fetch", "--raw-input", "archive/existing.json"])
                run.assert_called_once()
                self.assertEqual(
                    pathlib.Path(option(run.call_args.args[1], "--raw-input")),
                    ROOT / "archive" / "existing.json",
                )

    def test_cvf_and_ijcai_fetch_only_requested_years(self):
        for name, conference, function in (
            ("fetch_cvf", "CVPR", "fetch_cvpr"),
            ("fetch_cvf", "ECCV", "fetch_eccv"),
            ("fetch_ijcai", None, "fetch_year"),
        ):
            fetcher = load_script("fetchers/" + name)
            for value, expected in YEAR_CASES:
                with self.subTest(conference=conference or "IJCAI", value=value):
                    with mock.patch.object(fetcher, function, return_value=[]) as fetch:
                        with mock.patch.object(fetcher, "save_output"):
                            # The maintenance entrypoint normalizes and deduplicates first.
                            args = ["--years", ",".join(map(str, expected))]
                            if conference:
                                args += ["--conference", conference]
                            run_main(fetcher, args)
                    self.assertEqual([call.args[0] for call in fetch.call_args_list], sorted(expected))

    def test_anthology_cli_visits_only_requested_years(self):
        fetcher = load_script("fetchers/fetch_acl_anthology")
        for conference in ("ACL", "EMNLP"):
            for value, expected in YEAR_CASES:
                with self.subTest(conference=conference, value=value):
                    with tempfile.TemporaryDirectory() as tmp:
                        with mock.patch.object(fetcher, "collect_volume_paper_urls", return_value=[]) as collect:
                            with mock.patch.object(fetcher, "fetch_emnlp_program", return_value=[]):
                                run_main(fetcher, ["--conference", conference, "--years", value, "--output", str(pathlib.Path(tmp) / "rows.json")])
                        self.assertEqual(list(dict.fromkeys(call.args[1] for call in collect.call_args_list)), expected)

    def test_workflow_passes_exact_years_to_all_conference_wrappers(self):
        text = (ROOT / ".github/workflows/maintain-supabase.yml").read_text(encoding="utf-8")
        for conference in CONFERENCES:
            with self.subTest(conference=conference):
                self.assertIn('python src/maintain/' + conference + '.py --years "$YEARS" --skip-cleanup', text)


if __name__ == "__main__":
    unittest.main()
