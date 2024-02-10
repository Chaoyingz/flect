path = src/python-tui/
docs_path = docs/src

.PHONY: install
install:
	pip install -U pip pre-commit pdm
	pdm install
	pip install -e .
	pre-commit install

.PHONY: format
format:
	ruff check --fix-only $(path) docs
	ruff format $(path) docs

.PHONY: lint
lint:
	ruff check $(path) docs
	ruff format --check $(path) docs

.PHONY: typecheck
typecheck:
	pdm run pyright


.PHONY: test
test:
	coverage run -m pytest


.PHONY: testcov
testcov: test
	coverage html

.PHONY: dev
dev:
	export PYTHONPATH=$(docs_path) && uvicorn docs.src.document.main:app --reload --reload-dir .
