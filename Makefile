# Define your Poetry virtual environment
VENV := $(shell poetry env info --path)

# Define common commands
start:
	@poetry run uvicorn main:app --host 0.0.0.0 --port 4000 --reload

test:
	@poetry run pytest

test-cov:
	@poetry run pytest --cov=. --cov-report=term-missing

test-cov-html:
	@poetry run pytest --cov=. --cov-report=html

install:
	@poetry install

# Clean up coverage files
clean:
	@rm -rf htmlcov .coverage

.PHONY: start test test-cov test-cov-html install clean
