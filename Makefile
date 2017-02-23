# Top-level control of the building/installation/cleaning of various targets

# virtual environment
VIRTUALENV_DIR := .venv
ACTIVATE := $(VIRTUALENV_DIR)/bin/activate

.PHONY: default run clean_pyc clean style venv swagger

default: run

venv: $(ACTIVATE)
$(ACTIVATE): requirements.txt
	@echo "Updating virtualenv dependencies in: $(VIRTUALENV_DIR)..."
	@test -d $(VIRTUALENV_DIR) || virtualenv $(VIRTUALENV_DIR)
	@. $(ACTIVATE); pip install -U pip
	@. $(ACTIVATE); pip install -Ur requirements.txt
	@touch $(ACTIVATE)

run: venv
	@echo "Running (on port 8080)..."
	$(VIRTUALENV_DIR)/bin/python main.py

clean_pyc:
	@-find . -name '*.py[co]' -exec rm {} \;

clean:
	@echo "Removing virtual environment files"
	@rm -rf $(VIRTUALENV_DIR)

style: venv
	@. $(ACTIVATE); flake8 --exclude=.venv .

# due to a bug with flaskswagger, going to write out to an output dir
# and then redirect that to the screen. Otherwise it prints
# the swagger twice
swagger: venv
	@. $(ACTIVATE); flaskswagger main:app --out-dir . && cat swagger.json && echo && rm swagger.json
