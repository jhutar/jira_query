# Task 2: Internal ADF-Markdown Translation with `adfmd`

## Overview
Under the Jira Cloud REST API v3, rich-text fields (like descriptions and comments) are transmitted and stored as complex, nested Atlassian Document Format (ADF) JSON structures. However, end users of `jira-cli.py` should interact exclusively with standard Markdown. They should write descriptions and comments in Markdown, and see output in Markdown.

To achieve this, `jira-cli.py` must use the system binary **`adfmd`** internally to perform seamless, bidirectional translation behind the scenes. This completely abstracts ADF away from the user, requiring zero manual conversion or awareness of ADF.

---

## 1. Internal Translation Helper

Implement a helper function within `jira-cli.py` to run the system `adfmd` binary using Python's `subprocess` module:

```python
import subprocess
import json

def _translate_content(subcommand: str, input_str: str) -> str:
    """
    Invokes the system 'adfmd' binary to perform bidirectional translation.

    Args:
        subcommand: Either "to-md" (ADF -> Markdown) or "to-adf" (Markdown -> ADF)
        input_str: Input text to translate (either raw Markdown or ADF JSON string)

    Returns:
        Translated string output from adfmd stdout.
    """
    try:
        proc = subprocess.run(
            ["adfmd", subcommand],
            input=input_str,
            capture_output=True,
            text=True,
            check=True,
        )
        return proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.getLogger("jira_cli").error(
            f"adfmd {subcommand} failed (exit {e.returncode}): {e.stderr}"
        )
        raise RuntimeError(f"Content translation failed: {e.stderr}") from e
```

---

## 2. Converting User Markdown input to ADF (Outbound Payload)

When a user provides standard Markdown text (e.g., in a description file, direct `--description` string, inline editor, or a comment), `jira-cli.py` must internally translate it to ADF JSON before sending it to Jira:

1. **Creating or Updating Description:**
   Prior to creating or updating an issue, convert the user's Markdown description:
   ```python
   # Translate user markdown description to ADF JSON structure
   adf_json_str = _translate_content("to-adf", user_markdown_description)
   issue_payload["description"] = json.loads(adf_json_str)
   ```

2. **Adding Comments:**
   Convert the user's Markdown comment text to ADF JSON:
   ```python
   # Translate comment markdown to ADF JSON
   adf_json_str = _translate_content("to-adf", user_markdown_comment)
   self._jira.add_comment(issue, json.loads(adf_json_str))
   ```

---

## 3. Converting ADF to Markdown (Inbound Display)

When listing or viewing tickets, `jira-cli.py` retrieves descriptions and comments as ADF JSON. It must translate them back to Markdown before presenting them to the user:

1. **Viewing Descriptions:**
   If `issue.fields.description` is returned as a dict/object (representing ADF JSON under API v3), translate it to standard Markdown for rendering:
   ```python
   adf_desc = issue.fields.description
   if isinstance(adf_desc, dict):
       # Translate ADF structure to Markdown
       markdown_description = _translate_content("to-md", json.dumps(adf_desc))
   else:
       markdown_description = adf_desc
   ```

2. **Viewing Comments:**
   Translate comment bodies from ADF to Markdown before listing them:
   ```python
   for comment in issue.fields.comment.comments:
       adf_body = comment.body
       if isinstance(adf_body, dict):
           markdown_comment = _translate_content("to-md", json.dumps(adf_body))
       else:
           markdown_comment = adf_body
   ```

---

## Testing & Verification Criteria
*   Verify that no python-level dependencies (like `markdownify` or `adfmd`) are added to `requirements.txt`, as we are solely relying on the pre-installed system `adfmd` binary.
*   Write unit tests in `test_jira_cli.py` mocking the `subprocess.run` calls to assert that:
    1. Descriptions and comments are converted using `_translate_content("to-adf", ...)` prior to creating/posting.
    2. Received fields are translated using `_translate_content("to-md", ...)` prior to displaying or outputting.
