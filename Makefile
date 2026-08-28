PYTHON := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: venv install test refresh full serving schedule-install schedule-uninstall understat understat-refresh

venv:
	/opt/homebrew/bin/python3.13 -m venv .venv
	$(PIP) install -r requirements.txt

install: venv

test:
	$(PYTHON) -m pytest -q

refresh:
	./scripts/refresh.sh

understat:
	$(PYTHON) build_understat.py

understat-refresh:
	./scripts/refresh_understat.sh

full:
	$(PYTHON) build.py --full

serving:
	$(PYTHON) build_serving.py

serve:
	$(PYTHON) serve.py

schedule-install:
	./scripts/install_schedule.sh

schedule-uninstall:
	./scripts/uninstall_schedule.sh
