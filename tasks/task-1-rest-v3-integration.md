# Task 1: Migrate to Jira REST API v3

## Overview
Jira Cloud has deprecated many legacy v2 REST API endpoints and fields (such as legacy Epic Links). This task focuses on switching the CLI client in `jira-cli.py` to target the Jira Cloud REST API v3 explicitly and preparing the codebase for v3 JSON formats.

## Current State
Currently, `_create_jira_client` initializes the `JIRA` client without specifying an API version, which defaults to v2:
```python
def _create_jira_client(url, username, token):
    options = {"server": url}
    return jira.JIRA(
        options=options,
        basic_auth=(username, token),
    )
```

## Requirements & Technical Specifications

1. **Client Initialization:**
   Modify `_create_jira_client` in `jira-cli.py` to explicitly set `'rest_api_version': '3'` in the `options` dictionary:
   ```python
   def _create_jira_client(url, username, token):
       options = {
           "server": url,
           "rest_api_version": "3",  # Switch client to Jira Cloud REST API v3
       }
       return jira.JIRA(
           options=options,
           basic_auth=(username, token),
       )
   ```

2. **Verify/Adjust Authentication:**
   Confirm that the basic authentication using username and API token continues to function properly under v3 options.

3. **Handle Unified `parent` Field:**
   In REST API v3, modern projects use a unified `parent` JSON structure to relate issues instead of custom fields (like `customfield_10014` or `customfield_10018`).
   When setting a parent link in API v3, the payload format should look like:
   ```json
   "fields": {
       "parent": { "key": "PARENT-ISSUE-KEY" }
   }
   ```
   Add fallback/transition code to use the `parent` field when interacting with modern projects under v3.

## Testing & Verification Criteria
*   Run the test suite using `pytest test_jira_cli.py` to ensure mock project validation, status validation, and assignee lookup tests are updated and pass with the new client initialization logic.
*   Update mocks in `test_jira_cli.py` to reflect v3 responses where appropriate.
*   Verify with a dry-run issue creation (`--dry-run` flag) that the client successfully initializes and displays the expected fields.
