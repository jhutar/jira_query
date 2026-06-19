# Task 7: Sprint Query Command (`sprints` subcommand)

## Overview
The ACLI cheatsheet highlights the frequent need to list active sprints on a board to find active sprint IDs (e.g. `acli jira board list-sprints --id BOARD_ID --state "active"`). While `jira-cli.py` implements an internal caching function for sprints, this functionality is completely hidden from the user. This task exposes a dedicated `sprints` subcommand so users can easily list and search active or future sprints directly from the terminal.

## Requirements & Technical Specifications

1. **Add `sprints` Subparser:**
   Define a `sprints` subcommand in `main()` of `jira-cli.py`:
   ```python
   parser_sprints = subparsers.add_parser(
       "sprints",
       help="List sprints for a specific board or project",
   )
   parser_sprints.add_argument(
       "--board-id",
       help="Filter sprints by board ID",
       type=int,
   )
   parser_sprints.add_argument(
       "--state",
       choices=["active", "future", "closed", "all"],
       default="active",
       help="Filter sprints by state",
   )
   ```

2. **Define `do_sprints()` Execution Logic:**
   Add a `do_sprints` method to the `Doer` class:
   *   Call `self._list_sprints()` to retrieve cached sprint data (or refresh if cache is expired).
   *   Filter the sprint list based on specified `--board-id` (if provided) and `--state` (if provided and not "all").
   *   Format and print a table/list of matching sprints, displaying the board ID, sprint ID, name, and current state:
       ```text
       Board ID  Sprint ID  Sprint Name        State
       -----------------------------------------------
       6067      12040      Konflux Sprint 10  active
       10332     13251      Sat Sprint 84      active
       ```

3. **Incorporate Refresh Trigger:**
   Add a `--refresh` flag to force eviction of the local `sprints.json` cache file and query the API live:
   ```python
   parser_sprints.add_argument(
       "--refresh",
       action="store_true",
       help="Force refresh the cached sprint data",
   )
   ```
   If `--refresh` is selected, delete/clear `~/.jira-cli/sprints.json` (or set its age to be obsolete) before executing the query.

## Testing & Verification Criteria
*   Ensure running `jira-cli.py sprints` outputs a properly formatted table.
*   Write unit tests in `test_jira_cli.py` to assert that:
    *   The `sprints` subparser is registered correctly.
    *   The filtering on `--board-id` and `--state` yields correct subsets of mock sprint data.
    *   The force refresh flag correctly invalidates the cache file.
