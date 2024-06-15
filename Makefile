PROJECT_NAME = gdpr-obfuscator
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip

create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

ACTIVATE_ENV := source venv/bin/activate

define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

bandit:
	$(call execute_in_env, $(PIP) install bandit)

safety:
	$(call execute_in_env, $(PIP) install safety)

flake:
	$(call execute_in_env, $(PIP) install flake8)

coverage:
	$(call execute_in_env, $(PIP) install coverage)

dev-setup: bandit safety flake coverage

security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)

	$(call execute_in_env, bandit -lll *c/*/*.py)

run-flake:
	$(call execute_in_env, flake8  ./src/*.py ./src/*/*.py ./test/*.py ./test/*/*.py)

unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest $(filter-out $@,$(MAKECMDGOALS)) -v)

check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} coverage run --omit 'venv/*' -m pytest && coverage report -m)

mark-test-error-handling:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -m error_handling -v)

pre-commit:
	$(call execute_in_env, pre-commit run --all-files)

run-checks: security-test run-flake unit-test check-coverage
