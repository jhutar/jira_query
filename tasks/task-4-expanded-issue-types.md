# Task 4: Support for Feature and Sub-task Issue Types

## Overview
Currently, `jira-cli.py` restricts new issue creation to only "Task", "Bug", and "Epic". The cheatsheet shows that projects frequently use the **`Feature`** (Epic's parent) and **`Sub-task`** (Task's child) types. This task expands the supported types and enforces structural validation when creating hierarchical tickets.

## Requirements & Technical Specifications

1. **Update CLI Argument choices:**
   Locate the `--type` argument in `parser_create` within `jira-cli.py`:
   ```python
   parser_create.add_argument(
       "--type",
       choices=["Task", "Bug", "Epic", "Feature", "Sub-task"],  # Added Feature and Sub-task
       default="Task",
       help="Issue type",
   )
   ```

2. **Add Sub-task Validation:**
   If a user tries to create a `Sub-task`, a parent ticket is strictly required. Enforce this prior to making the creation API call:
   ```python
   if self._args.type == "Sub-task":
       assert self._args.parent is not None, "A parent issue key (via --parent) is required when creating a Sub-task."
   ```

3. **Sub-task Parent Payload Mapping:**
   When creating a `Sub-task` via the API:
   *   For v3 API, use the unified `parent` field:
       ```python
       issue_payload["parent"] = {"key": self._args.parent}
       ```
   *   For v2/fallback API, use the legacy field:
       ```python
       issue_payload["parent"] = {"id": parent_issue.id}  # Or "key" depending on client version
       ```

## Testing & Verification Criteria
*   Verify that passing `--type Feature` or `--type Sub-task` passes ArgumentParser validation.
*   Write unit tests in `test_jira_cli.py` ensuring that trying to create a `Sub-task` *without* a `--parent` parameter raises an `AssertionError`.
*   Write unit tests ensuring that valid project issue type checks accept `Feature` and `Sub-task` if returned by the mock project metadata.
