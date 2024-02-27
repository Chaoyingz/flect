path = src/python-tui/
docs_path = docs/src

.PHONY: install
install:
	curl -sSf https://rye-up.com/get | bash
	rye sync
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
	rye run pyright


.PHONY: test
test:
	coverage run -m pytest


.PHONY: testcov
testcov: test
	coverage html

.PHONY: dev
dev:
	export PYTHONPATH=$(docs_path) && uvicorn docs.src.documentation.main:app --reload --reload-dir .
