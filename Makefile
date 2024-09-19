# Globals
GLOBAL_PYTHON = $(DEFAULT_PYTHON)
PYTHON_VENV_NAME = .venv
PROJECT_NAME = file_manager

ifeq ($(OS),Windows_NT)
	PYTHON_INTERPRETER = $(PYTHON_VENV_NAME)/scripts/python
else
	PYTHON_INTERPRETER = $(PYTHON_VENV_NAME)/bin/python
endif

.PHONY: create_venv
create_venv:
	$(GLOBAL_PYTHON) -m venv $(PYTHON_VENV_NAME)
	$(PYTHON_INTERPRETER) -m pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m pip install setuptools

.PHONY: delete_venv
delete_venv:
	rm $(PYTHON_VENV_NAME)/ -r

.PHONY: install
install:
	$(PYTHON_INTERPRETER) -m pip install -e .
	$(PYTHON_INTERPRETER) -m pip freeze > requirements.txt --exclude-editable

.PHONY: full_install
full_install:
	$(PYTHON_INTERPRETER) -m pip install -e .[full]
	$(PYTHON_INTERPRETER) -m pip freeze > requirements.txt --exclude-editable

.PHONY: dev_install
dev_install:
	$(PYTHON_INTERPRETER) -m pip install -e .[dev]
	$(PYTHON_INTERPRETER) -m pip freeze > dev-requirements.txt --exclude-editable
	echo "-e ." >> dev-requirements.txt

.PHONY: install_reqs
install_reqs:
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

.PHONY: install_dev_reqs
install_dev_reqs:
	$(PYTHON_INTERPRETER) -m pip install -r dev-requirements.txt

.PHONY: coverage
coverage:
	$(PYTHON_INTERPRETER) -m pytest --cov=$(PROJECT_NAME) tests/
