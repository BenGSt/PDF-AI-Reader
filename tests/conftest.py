import os
import sys

# Ensure the project's root directory is on sys.path so `import src` works
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def pytest_runtest_logreport(report):
    """Print test nodeid and result (PASS/FAIL/SKIP) after each test call phase.

    Uses the terminal reporter to ensure messages appear in the test output.
    """
    if report.when != "call":
        return
    try:
        tr = report.config.pluginmanager.getplugin("terminalreporter")
        if tr:
            tr.write_line(f"{report.nodeid}  {report.outcome.upper()}")
    except Exception:
        # best-effort: fall back to print if terminal reporter unavailable
        print(f"{report.nodeid}  {report.outcome.upper()}")

