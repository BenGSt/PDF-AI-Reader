# TESTING.md

Purpose
- Document the project's testing policy, tooling, and recommended Test-Driven Development (TDD) workflow for contributors.

Scope
- Applies to all code in `src/` and to integration/smoke tests in `tests/`.
- Tests are developer-facing artifacts and live in the repository; they are not packaged into production releases but must be run by CI and during development.

TDD policy (short)
- For new modules and significant feature changes: write a failing test first, implement the minimum code to make it pass, then refactor.
- Small bug fixes may be accompanied by a regression test that reproduces the bug first.
- All PRs should include tests for new behavior and maintain or improve test coverage.

Test pyramid and types
- Unit tests (fast, isolated): test single functions/classes. Place under `tests/unit/` with `test_*.py` naming.
- Integration tests: test interactions across modules (ChromaDB, embedding pipeline, document loader). Place under `tests/integration/`.
- Smoke/end-to-end tests: lightweight E2E flows that exercise the full add->index->query path. Place under `tests/smoke/` and name `test_smoke_*.py`.

Tools & dependencies
- Test runner: pytest
- Coverage: coverage.py (generate reports with `coverage run -m pytest && coverage report -m`)
- Parallel test runner (optional): pytest-xdist
- Linting/format: flake8/black/isort (run in pre-commit)
- Optional: hypothesis for property-based tests
- Put test deps in `requirements/test.txt`.

Repository layout (tests)
- `tests/unit/` — unit tests
- `tests/integration/` — integration tests
- `tests/smoke/` — smoke / E2E tests
- `tests/fixtures/` — pytest fixtures and small test assets (keep binaries out of repo)

Test naming conventions
- Files: `test_<module>_*.py`
- Functions: `test_<behavior>_<condition>`
- Keep tests small, deterministic, and fast where possible.

Writing tests (practical rules)
- Use fixtures for shared setup and tear-down (keep I/O minimal in unit tests).
- Mock external services/network/LLM backends in unit tests; use real backends in integration/smoke tests where feasible.
- For tests that require models/data, add small, checked-in fixtures or a script to download minimal data during CI.
- Seed RNGs and set deterministic seeds for pseudo-random behavior.
- Prefer explicit assertions over broad ``assert`` patterns; assert shape and content when possible.

Smoke tests (must-have for MVP)
- `tests/smoke/test_smoke_index.py` — index a small sample PDF and assert embeddings generated and stored.
- `tests/smoke/test_smoke_query.py` — run a query against the indexed sample and assert non-empty answer + sources list.

How to run locally

```bash
# install test deps (macOS/Linux/zsh)
python -m pip install -r requirements/test.txt

# run all tests
pytest -q

# run smoke tests only
pytest -q tests/smoke/

# run a single test file
pytest -q tests/smoke/test_smoke_index.py

# coverage report
coverage run -m pytest && coverage report -m
```

CI recommendations
- Run `pytest` and `coverage` on every PR. Fail the build if critical smoke tests fail.
- Set a minimum coverage gate for the MVP (e.g., 60%) and increase over time.
- Cache downloaded models/artifacts in CI to speed integration tests.
- Use matrix builds to test multiple Python versions if necessary.

Dealing with flaky tests
- Mark flaky tests with `@pytest.mark.flaky` or `xfail` and open an issue to fix them.
- Aim to keep the test suite stable; flaky tests should be temporary and triaged.

Adding tests for a new module (developer checklist)
- [ ] Add `tests/unit/test_<module>.py` with a failing test that describes the expected behavior.
- [ ] Implement minimal code to pass the test.
- [ ] Add integration/smoke tests if the module touches storage, models, or the RAG pipeline.
- [ ] Run `pytest` and ensure local coverage is acceptable.
- [ ] Add the change to the changelog/PR description and include test notes.

Test data and large artifacts
- Avoid committing large model files to the repo.
- Use small fixtures for smoke tests; provide download scripts for larger artifacts and cache them in CI.

Suggested `requirements/test.txt` (example)
```
pytest
pytest-xdist
coverage
pytest-mock
pytest-cov
# optional
hypothesis
```

Contacts and escalation
- Include test failures and flaky tests as part of regular grooming.
- Create issues for flaky/regression tests and assign an owner.

Notes
- The spec documents repository contents and visible repo layout; detailed test-first workflow and enforcement live in `plan.md` and this `TESTING.md` for developer guidance.
- If you want, I can scaffold `requirements/test.txt` and the two smoke test stubs next.
