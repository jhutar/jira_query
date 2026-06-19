# Task 2: ADF/HTML to Markdown with `adfmd`

## Overview
Under the Jira Cloud REST API v3, rich-text fields (like descriptions and comments) are returned as complex, nested Atlassian Document Format (ADF) JSON objects. When listing or viewing tickets, displaying raw ADF JSON to CLI users is not acceptable. This task focuses on utilizing the `adfmd` library to convert ADF JSON objects (or HTML from `renderedFields`) back into standard, human-readable Markdown for CLI display.

## Requirements & Technical Specifications

1. **Add Dependency:**
   Add `adfmd` to `requirements.txt`:
   ```text
   adfmd
   ```
   *(Note: `adfmd` has an identical interface to `markdownify`, but natively supports both direct ADF JSON and HTML to Markdown conversion.)*

2. **Integrate `adfmd` in Output Formatting:**
   Import `markdownify` from `adfmd` to convert retrieved fields:
   ```python
   from adfmd import markdownify as md
   ```

3. **Scenario A: Converting Direct ADF JSON (Preferred for Offline/Raw):**
   When `issue.fields.description` is returned as an ADF JSON structure, use `md` to convert it to a clean Markdown string:
   ```python
   adf_desc = issue.fields.description
   markdown_desc = md(adf_desc) if isinstance(adf_desc, dict) else adf_desc
   ```

4. **Scenario B: Converting Rendered HTML (Alternative):**
   To support server-side rendering, request issues with the `renderedFields` expansion (e.g. `jira.issue(key, expand="renderedFields")` or `jira.search_issues(query, expand="renderedFields")`).
   Then, convert the HTML returned in the `renderedFields` dictionary to Markdown:
   ```python
   html_desc = issue.raw.get("renderedFields", {}).get("description")
   markdown_desc = md(html_desc) if html_desc else "No description"
   ```

5. **Apply Conversion to Comments:**
   Apply the same `adfmd` translation to comments retrieved under the v3 API:
   ```python
   for comment in issue.fields.comment.comments:
       # Convert comment body from ADF to Markdown
       markdown_comment = md(comment.body) if isinstance(comment.body, dict) else comment.body
   ```

## Testing & Verification Criteria
*   Add unit tests in `test_jira_cli.py` to verify that `adfmd` conversion is invoked correctly on mock ADF JSON objects.
*   Assert that raw nested ADF JSON outputs are converted to the expected clean markdown output (e.g. `{"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}]}` becomes `"Hello"`).
