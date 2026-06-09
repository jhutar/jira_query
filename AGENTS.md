# Agent Guidelines

Welcome, Agent. To maintain the quality and consistency of this codebase, please follow these guidelines:

## Code Formatting

Always format your Python code using `ruff`.

- **To format all files:** `ruff format *.py`
- **To format a specific file:** `ruff format <file_path>`

## Testing

Before committing changes, ensure that you run the existing test suite to prevent regressions.

- **To run the PR utility tests:** `pytest test_pr_utils.py`
- **To run all tests:** `pytest` (if more tests are added)

## PR and Commit Enrichment

When modifying logic related to PR or commit extraction, update `test_pr_utils.py` with the new patterns you are supporting.
