.PHONY: install lint test run docs check
install:
	cd backend && uv sync
lint:
	cd backend && uv run ruff format --check . && uv run ruff check . && uv run mypy
test:
	cd backend && uv run pytest
run:
	cd backend && uv run uvicorn prra.main:create_app --factory --reload
docs:
	python scripts/check_docs.py
check: lint test docs
