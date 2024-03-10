path = src/python-flect/src/flect/
docs_path = docs/src

.PHONY: install
install:
	rye sync
	rye install pre-commit
	pre-commit install

.PHONY: format
format:
	rye run ruff check --fix-only $(path) docs src/python-flect/
	rye run ruff format $(path) docs src/python-flect/

.PHONY: lint
lint:
	rye run ruff check $(path) docs src/python-flect/
	rye run ruff format --check $(path) docs src/python-flect/

.PHONY: typecheck
typecheck:
	rye run pyright


.PHONY: test
test:
	export PYTHONPATH=$(docs_path) && rye run coverage run -m pytest


.PHONY: testcov
testcov: test
	coverage html


.PHONY: build
build:
	npm run build

.PHONY: dev
dev:
	export PYTHONPATH=$(docs_path) && uvicorn docs.src.documentation.main:app --reload --reload-dir .
