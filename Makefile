POETRY ?= $(HOME)/.poetry/bin/poetry

.PHONY: example
example:
	@$(POETRY) run python example

.PHONY: docs-serve
docs-serve:
	@$(POETRY) run mkdocs serve

.PHONY: docs-gh-deploy
docs-gh-deploy:
	@$(POETRY) run mkdocs gh-deploy

.PHONY: install-poetry
install-poetry:
	@curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

.PHONY: install-deps
install-deps:
	@$(POETRY) install -vv

.PHONY: install
install: install-poetry install-deps

.PHONY: lint-black
lint-black:
	@echo "\033[92m< linting using black...\033[0m"
	@$(POETRY) run black --check --diff .
	@echo "\033[92m> done\033[0m"
	@echo

.PHONY: lint-flake8
lint-flake8:
	@echo "\033[92m< linting using flake8...\033[0m"
	@$(POETRY) run flake8 aioapi example tests
	@echo "\033[92m> done\033[0m"
	@echo

.PHONY: lint-isort
lint-isort:
	@echo "\033[92m< linting using isort...\033[0m"
	@$(POETRY) run isort --check-only --diff --recursive .
	@echo "\033[92m> done\033[0m"
	@echo

.PHONY: lint-mypy
lint-mypy:
	@echo "\033[92m< linting using mypy...\033[0m"
	@$(POETRY) run mypy --ignore-missing-imports --follow-imports=silent aioapi example tests
	@echo "\033[92m> done\033[0m"
	@echo

.PHONY: lint
lint: lint-black lint-flake8 lint-isort lint-mypy

.PHONY: test
test:
	@$(POETRY) run pytest --cov-report term --cov-report html --cov=aioapi -vv

.PHONY: codecov
codecov:
	@$(POETRY) run codecov --token=$(CODECOV_TOKEN)

.PHONY: publish
publish:
	@$(POETRY) publish --username=$(PYPI_USERNAME) --password=$(PYPI_PASSWORD) --build
