# Task 3: Unified Hierarchy & Parent Linking

## Overview
Jira Cloud's unified hierarchy uses the modern `parent` field to link all issue levels (Sub-task to Task, Task to Epic, Epic to Feature). However, some projects or configurations might still expect legacy Epic Link (`customfield_10014`) or Parent Link (`customfield_10018`) fields. This task adds a robust `--parent` command-line argument that seamlessly handles both modern v3 hierarchy payloads and fallback configuration mapping.

## Requirements & Technical Specifications

1. **Add `--parent` CLI Flag:**
   In both `parser_create` and `parser_update` in `jira-cli.py`, add a `--parent` argument:
   ```python
   parser_create.add_argument(
       "--parent",
       help="Parent issue key to link this issue under (unifies Epic Link, Parent Link, and Sub-task parents)",
   )
   ```
   *(Note: Ensure this is also added to the `update` parser to allow moving or updating an issue's parent.)*

2. **Hierarchical Routing Logic (v3 vs. Legacy):**
   In `Doer._update_fields` (or during creation), implement smart routing:
   *   **Jira Cloud API v3 Mode:** Set the top-level `parent` field directly during issue creation or update:
       ```python
       fields = {
           "parent": {"key": self._args.parent}
       }
       ```
   *   **Legacy Custom Fields Fallback:** If custom fields are configured, fall back to setting the appropriate legacy ID based on target issue type:
       *   If linking **Task/Bug to Epic**: Use Epic Link mapping `self._config["custom_fields"]["epic"]` (typically `customfield_10014`).
       *   If linking **Epic to Feature**: Use Parent Link mapping `self._config["custom_fields"]["parent_link"]` (typically `customfield_10018`).

3. **Validation of Parent Key:**
   Before assigning a parent, pre-validate that the parent issue exists and is accessible:
   ```python
   if self._args.parent is not None:
       try:
           self._jira.issue(self._args.parent, fields="issuetype")
       except Exception as e:
           raise AssertionError(f"Parent issue '{self._args.parent}' not found or inaccessible: {e}")
   ```

## Testing & Verification Criteria
*   Write unit tests in `test_jira_cli.py` to mock a parent issue lookup.
*   Test that when `--parent` is specified under the v3 API configuration, the JSON payload successfully contains `"parent": {"key": "PARENT-123"}`.
*   Test legacy fallback behavior where `--parent` routes to `customfield_10014` or `customfield_10018` when legacy mappings are detected.
