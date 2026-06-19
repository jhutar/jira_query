# Task 6: Direct Ticket Viewing Command (`view` subcommand)

## Overview
Currently, `jira-cli.py` has no direct command to inspect the details of a single ticket (e.g. `jira-cli.py view KEY-123`). CLI users are forced to run JQL list searches (`jira-cli.py list --query "key = KEY-123"`) to see details, which is slow and inconvenient. This task adds a dedicated `view` subcommand to print a clean, detailed summary of one or more specified issues, integrating the ADF-to-Markdown conversion from Task 2.

## Requirements & Technical Specifications

1. **Add `view` Subparser:**
   Define a `view` subcommand in the subparser definitions of `main()` in `jira-cli.py`:
   ```python
   parser_view = subparsers.add_parser(
       "view",
       help="View details of a specific issue",
   )
   parser_view.add_argument(
       "issue_key",
       help="The Jira issue key to view (e.g., 'KONFLUX-123')",
       type=str,
   )
   ```

2. **Define `do_view()` Execution Logic:**
   Add a `do_view` method to the `Doer` class.
   *   Fetch the issue using the specified `issue_key`.
   *   Use the `expand="renderedFields"` option to support HTML rendering, or directly retrieve fields.
   *   Print formatted details to stdout, including:
       *   Key, Summary, Type, Status, Assignee, Reporter, Priority, Story Points, Sprint, and Parent/Epic.
       *   **Description:** Converted from ADF JSON (or HTML) using the `adfmd` library (Task 2).
       *   **Comments:** Listed with author, timestamp, and body converted from ADF JSON using `adfmd`.

   *Example Output Template:*
   ```text
   ================================================================================
   [KONFLUX-123]   Status: In Progress   Type: Task   Points: 5.0
   Summary:   Investigate Pipeline performance issues
   Assignee:  John Doe (john.doe@redhat.com)
   Sprint:    Konflux Sprint 10
   --------------------------------------------------------------------------------
   Description:
   This task is focused on investigating why pipeline jobs stall during high
   concurrency. We should focus on container load bottlenecks.
   --------------------------------------------------------------------------------
   Comments:
   - Jane Smith (2026-06-18 14:20):
     I've added some debug logs to help locate the bottleneck.
   ================================================================================
   ```

3. **Incorporate JSON Dumping:**
   If the global `--dump` flag is set, save the raw issue JSON details to the `jira_issue_details` folder (similar to the behavior in `do_list`):
   ```python
   if self._args.dump:
       # Write issue.raw to a JSON file
   ```

## Testing & Verification Criteria
*   Verify that `jira-cli.py view KEY-123` correctly prints the ticket structure to stdout.
*   Write unit tests in `test_jira_cli.py` mocking the issue retrieval and validating that description/comments conversions are executed successfully.
