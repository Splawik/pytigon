.DEFAULT_GOAL := test

test:
	ptig @pytest tests/

# Gating lint: syntax errors and undefined names only. Deliberately kept green
# so it can block a merge. Widen it in pyproject.toml as findings are fixed.
lint:
	ruff check . --select E9,F63,F7,F82

# Full rule set. Informational only - the repo still has open findings.
lint-full:
	ruff check .

fmt:
	ruff format .

# Informational: reports the typing debt, does not gate (hundreds of
# findings today). Kept in CI so the number is visible and cannot grow
# silently.
typecheck:
	-mypy pytigon

check: lint test
