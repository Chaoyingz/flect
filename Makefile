path = src/python-tui

.PHONY: install
install:
	pip install -U pip pre-commit pdm
	pdm install -p $(path)
	pre-commit install

.PHONY: format
format:
	ruff check --fix-only $(path) demo docs
	ruff format $(path) demo docs

.PHONY: lint
lint:
	ruff check $(path) demo
	ruff format --check $(path) demo docs

.PHONY: typecheck
typecheck:
	pyright

.PHONY: dev
dev:
	uvicorn demo.app:app --reload --reload-dir .
