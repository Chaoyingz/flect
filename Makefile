path = src/python-tui

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
	pyright

.PHONY: dev
dev:
	uvicorn docs.app:app --reload --reload-dir .
