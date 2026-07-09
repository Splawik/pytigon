.DEFAULT_GOAL := test

test:
	ptig @pytest tests/

lint:
	ruff check .

fmt:
	ruff format .

check: lint test
