path = src/python-tui/

.PHONY: install
install:
	pip install -U pip pre-commit pdm
	pdm install -p $(path)
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
	uvicorn docs.main:app --reload --reload-dir .
