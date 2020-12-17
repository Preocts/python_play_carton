SRC_DIR=src/egg_afk_clock

.PHONY: update-deps init update install clean clean-pyc clean-build clean-test test package

update-deps:
	pip-compile --upgrade --generate-hashes
	pip-compile --upgrade --generate-hashes --output-file dev-requirements.txt dev-requirements.in

install:
	pip install --upgrade pip setuptools wheel
	pip install --upgrade -r requirements.txt  -r dev-requirements.txt
	pip install --editable .

init:
	pip install pip-tools

update: init update-deps install

# Run all cleaning steps
clean: clean-build clean-pyc clean-test

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build: ## Remove build artifacts.
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf vendors/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test: ## Remove test artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	find . -name '.pytest_cache' -exec rm -fr {} +

blacken: ## Run Black against code
	black --line-length 79 ./${SRC_DIR}
	black --line-length 79 ./tests

test: ## Run all tests found in the /tests directory.
	coverage run -m pytest tests/
	coverage report --include "*/${SRC_DIR}/*" --show-missing
