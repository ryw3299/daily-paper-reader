# Repository Guidelines

## Project Structure & Module Organization

Daily Paper Reader combines a Python recommendation pipeline with a static docsify reader deployed through GitHub Actions and Pages.

- `src/`: pipeline orchestration (`main.py`), numbered processing stages, retrieval, and research modules; `src/maintain/` handles ingestion and synchronization.
- `app/` and `index.html`: browser JavaScript, CSS, and entry point; `app/vendor/` contains third-party assets.
- `tests/`: Python and JavaScript regression tests.
- `sql/`, `scripts/`, `.github/workflows/`: database schemas/RPCs, development utilities, and automation.
- `docs_init/`: reusable site templates; `docs/` and `archive/`: generated reading pages and pipeline state. `others/` stores README images.

## Build, Test, and Development Commands

Run commands from the repository root with Python 3.11 and Node.js:

- `python -m pip install -r requirements.txt pytest pytest-subtests`: install lightweight runtime and test dependencies.
- `python src/local_debug_server.py --host 127.0.0.1 --port 8567`: serve the reader and local workflow backend.
- `bash scripts/bootstrap_local.sh`: create a virtual environment, install dependencies, and start development in a compatible Bash environment.
- `python src/main.py --fetch-days 10`: run the recommendation pipeline; requires configured services and writes generated output.
- `python -m pytest -q`: run Python regressions.
- `node tests/test_topic_preview.js`: run one JavaScript regression; CI runs every `tests/test_*.js` separately.

The frontend uses static assets without a bundler build.

## Coding Style & Naming Conventions

Use four-space Python indentation and `snake_case` functions/modules. Follow surrounding JavaScript style, generally two-space indentation and `camelCase` functions. Preserve numbered pipeline filenames and existing browser module interfaces. No repository-wide formatter or linter is configured.

## Testing Guidelines

Python tests use pytest discovery, often with `unittest` and mocks; JavaScript tests use Node assertions. Name tests `tests/test_<feature>.py` or `.js`. Add focused regressions for changed behavior and mock external services. No numeric coverage threshold is configured. For visual fixes, verify served assets and browser DOM/computed styles or screenshots.

## Commit & Pull Request Guidelines

History uses `fix:`, `chore:`, and bracketed prefixes such as `[fix]` and `[update]`. Write concise, descriptive subjects. Agent-created commits must end with:

```text
Co-Authored-By: xixi <3495302215@qq.com>
```

PRs should describe behavior changes, link relevant issues, list validation, and include screenshots for UI changes. Keep personalized configuration and generated outputs out of upstream contributions; edit `docs_init/` templates for reusable site changes.

## Security & Configuration

Use `.env.example` to configure local `.env`; never commit plaintext credentials or expose Supabase service-role keys to browsers. Treat `secret.private`, reading state, and existing paper routes as user data to preserve.

## Response Style

把所有的防御性话术统一放到最后一段，并拆成两类，真影响结论的风险单拎出来和另一类单独说的纯套话。
