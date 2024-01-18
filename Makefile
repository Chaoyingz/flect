path = src/python-tui

.PHONY: install
install:
	pip install -U pip pre-commit pdm
	pdm install -p $(path)
	pre-commit install

.PHONY: format
format:
	ruff check --fix-only $(path) demo
	ruff format $(path) demo

.PHONY: lint
lint:
	ruff check $(path) demo
	ruff format --check $(path) demo

.PHONY: typecheck
typecheck:
	pyright

.PHONY: dev
dev:
	uvicorn demo.app:app --reload --reload-dir .
