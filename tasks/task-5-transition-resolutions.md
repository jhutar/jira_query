# Task 5: Support Transitions with Resolutions

## Overview
When moving a ticket to a closed or resolved state (e.g., "Closed", "Resolved", "Done"), Jira workflows often require or expect a **Resolution** (e.g., "Done", "Not a Bug", "Cannot Reproduce", "Duplicate"). If `jira-cli.py` transitions a ticket without specifying the resolution, the operation will fail if the transition screen makes resolution mandatory, or it will leave the issue in an inconsistent state. This task adds support for a `--resolution` flag.

## Requirements & Technical Specifications

1. **Add CLI Argument:**
   Add a `--resolution` flag to both `parser_create` and `parser_update` subparsers in `jira-cli.py`:
   ```python
   parser_update.add_argument(
       "--resolution",
       help="Resolution name to set when transitioning (e.g., 'Done', 'Not a Bug', 'Cannot Reproduce')",
   )
   ```

2. **Transition Payload Mapping:**
   When transitioning an issue, if a resolution is specified, construct the transition fields dictionary and pass it to the transition method.

   In `Doer._update_status`:
   ```python
   transition_fields = {}
   if self._args.resolution is not None:
       transition_fields["resolution"] = {"name": self._args.resolution}

   if self._args.dry_run:
       _pretty(f"Would transition to {self._args.status} with fields:", transition_fields)
   else:
       # Access transitions to find ID
       transitions = self._jira.transitions(issue)
       status_transitions = {t["name"]: t["id"] for t in transitions}
       assert self._args.status in status_transitions, (
           f"Status {self._args.status} not found in available statuses ({', '.join(status_transitions)})"
       )

       # Execute transition passing fields dictionary
       if transition_fields:
           self._jira.transition_issue(
               issue,
               status_transitions[self._args.status],
               fields=transition_fields
           )
       else:
           self._jira.transition_issue(issue, status_transitions[self._args.status])
   ```

## Testing & Verification Criteria
*   Verify that `--resolution` is parsed correctly as a string option.
*   Write a unit test in `test_jira_cli.py` mocking the `transitions` lookup and `transition_issue` invocation. Assert that when `--resolution` is passed, `self._jira.transition_issue` is called with the correct `fields={"resolution": {"name": "RESOLUTION_NAME"}}` dictionary.
