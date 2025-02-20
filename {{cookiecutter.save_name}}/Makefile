test:
	uv run python3 -m pytest tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "logs" -exec rm -rf {} +
lint:
	uv run ruff check .

format:
	uv run python3 -m isort . && black . && ruff format

pre-commit:
	uv run pre-commit run --all-files
