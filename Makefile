.PHONY: example
example:
	@poetry run python example

.PHONY: lint
lint:
	@poetry run tox -e py37-lint-black,py37-lint-flake8,py37-lint-isort,py37-lint-mypy

.PHONY: test
test:
	@poetry run tox -e py37-test
