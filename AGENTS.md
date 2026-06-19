# Agent Guidelines

Welcome, Agent. To maintain the quality and consistency of this codebase, please follow these guidelines:

## Code Formatting & Linting

Always format and validate your changes using the configured pre-commit checks.

- **To run lints and formatting on staged changes:** `make check`
- **To run lints and formatting on all files:** `make check-all`

## Testing

Before committing changes, ensure that you run the existing test suite to prevent regressions.

- **To run the full test suite:** `make test`

## PR and Commit Enrichment

When modifying logic related to PR or commit extraction, update `test_pr_utils.py` with the new patterns you are supporting.
