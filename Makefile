PYTHON=python3.11
VENV=.venv

.PHONY: venv install install-test test clean

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel
	$(VENV)/bin/python -m pip install -r requirements/base.txt

install-test: venv
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel
	$(VENV)/bin/python -m pip install -r requirements/test.txt

test: install-test
	$(VENV)/bin/pytest -q tests/smoke

clean:
	rm -rf $(VENV) .pytest_cache
