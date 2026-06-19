# Task 8: Automatic Project-level Defaults

## Overview
Currently, creating (but NOT updating) a ticket in different Jira projects requires manually specifying security levels (`--security`), components (`--components`), and sprint associations (`--sprint-current`). This task implements a robust project-level defaults system, allowing the CLI to load project-specific attributes automatically from the configuration file without forcing the user to supply repetitive arguments.

---

## Subtask 8.1: Configuration Schema Definition
Extend the YAML configuration file (`config.yaml` / `~/.jira_query.yaml`) to support a `project_defaults` block. Each project key contains an associative dictionary mapping CLI arguments to their default fallback values:

```yaml
project_defaults:
  KONFLUX:
    security: "Red Hat Employee"
    components: ["Performance"]
    sprint_current: true  # Automatically look up and assign the active sprint
  HCEPERF:
    security: "Red Hat Employee"
  SRVKP:
    security: "Red Hat Employee"
    components: ["Performance"]
    sprint_current: true
  SAT:
    security: "Red Hat Employee"
    components: ["Performance"]
    sprint_current: true
```

---

## Subtask 8.2: Argument Resolution & Cascading Precedence Logic
In `Doer.do_create` (NOT in `Doer.do_update`), implement a priority hierarchy for setting ticket parameters. The resolution sequence (from highest to lowest priority) must be:

1. **Command Line Flag:** Directly specified by the user (e.g. `--security "Public"`).
2. **Issue Template:** Populated if the user supplied a `--template` argument.
3. **Project Defaults:** Loaded automatically from the configuration key matching the target project key.
4. **Global Defaults / Hardcoded Fallbacks:** Default fallback values (e.g. defaulting security to "Red Hat Employee").

Every time a parameter is set based on Project Defaults or Global Defaults, message is presented to the user to let them know this happened (to avoid surprises).

### Implementation Reference Code:
```python
# During validation/preparation in do_create():
proj_defaults = self._config.get("project_defaults", {}).get(self._args.project, {})

for attr_name, default_value in proj_defaults.items():
    # If the user did not supply this flag on command line, and it wasn't populated by a template:
    if getattr(self._args, attr_name, None) is None:
        setattr(self._args, attr_name, default_value)
```

---

## Subtask 8.3: Automatic Active Sprint Bindings
If `sprint_current: True` is resolved for the project (either by explicit flag, template, or project defaults), automatically activate the sprint lookup and linkage logic.

In `jira-cli.py`, confirm that if `self._args.sprint_current` resolves to `True`, the script will automatically invoke sprint caching and query matching using the project's sprint regex map:
```python
if self._args.sprint_current:
    assert self._args.project in self._config["sprint_regexps"], (
        f"Project '{self._args.project}' is not configured in 'sprint_regexps' of config file."
    )
    # The active sprint lookup should execute automatically
```

---

## Subtask 8.4: Every option have a way override default

E.g. when project default is `components: ["Performance"]`, thi can be overwitten on command line by e.g. `--components ""` option.

---

## Testing & Verification Criteria
*   Create a test configuration file in `test_jira_cli.py` containing a mock `project_defaults` section.
*   Write unit tests to assert that:
    1. Creating a ticket without specifying `--security` or `--components` successfully inherits the security level and component list defined in `project_defaults` for that project.
    2. Explicitly specifying a command-line argument (e.g., `--security "Public"`) overrides the project default values.
    3. Setting `sprint_current: true` in the configuration file successfully triggers current sprint lookup during execution without passing `--sprint-current` on the command line.
