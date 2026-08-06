---
disable-model-invocation: true
description: Generates a weekly, monthly, quarterly, or yearly report for a given team with a given form.
allowed-tools: Bash(./report-data.py *) Bash(rm *reports/*-raw.md) Edit(reports/**)
---

## Usage

This skill runs the data-collection command, then gives guidance for turning that data into a final report.

**Invoke with:** `/generate-report <team> <range> <form>`

-   `<team>`: The team name (one of `Konflux`, `Pipelines`, `Satellite`, `ConsoleDot` also known as `HCC`).
-   `<range>`: The report range: `weekly` (use `1w`), `monthly` (use `1m`), `quarterly` (use `3m`), or `yearly` (use `12m`).
-   `<form>`: Form of a report, defaults to "Normal". See below for other possibilities.

## Step 1: Generate the data

Run this command to collect raw report data from Jira and save it to `reports/<team>-<range>-<date>-raw.md` (lowercase `<team>`, today's `<date>` as `YYYY-MM-DD`) for review before Step 2:

`./report-data.py --projects <team> --range <range_flag> [--no-enrich] > reports/<team>-<range>-<date>-raw.md`

| `<range>` | `<range_flag>` | `--no-enrich` |
| --- | --- | --- |
| weekly | `1w` | omit — enrichment stays on |
| monthly | `1m` | required |
| quarterly | `3m` | required |
| yearly | `12m` | required |

`--no-enrich` skips fetching linked pull requests, commits, and Slack threads — required beyond weekly to keep data volume manageable.

Completion criterion: the raw file exists under `reports/` and the command printed no errors.

## Step 2: Use the data with an LLM

Now generate a status update from the raw report data file content.

**Task:** Synthesize this data into a terse, professional status summary for engineering leadership. State only what the data supports — flag anything unclear rather than guessing. Weight Feature > Epic > Task/Story/Bug > Sub-task, story points (`sp` in the output), and Priority/Severity as signals of how big each piece of work was. Every ticket you mention must link to its Jira URL, and to its linked pull request/merge request URL when the raw data has one, so the reader can drill down to the source.

Based on the selected report `form`, pick one of the templates below. Completion criterion: every `...` placeholder is replaced with real content grounded in the data, or the bullet is dropped if the data doesn't support it.

### Report formed as "Normal"

```markdown
# Team <team> range <range>
* **Overview:** (Start with a 0-3 sentence overview of the most significant progress made across all teams this period. This is a bragging but honest section, but do not make up things.)
* **What was done:**
  * ... (Provide 0-3 bullet points summarizing team key activities. Focus on *outcomes* and *impact* (what was finished, what moved into review) rather than just listing ticket IDs. Use additional data to provide technical context where helpful.)
  * ...
* **What is moving:**
  * ... (Provide 0-3 bullet points summarizing transition of issues from "New" or "In Progress" to "In Review" or "Finished" (only if not already closed and mentioned in "What was done" section). Identify any blockers if they are apparent from the descriptions.)
  * ...
```

### Report formed as "Quarterly Review"

Be VERY short, each bullet 8 words at max.

```markdown
# Perf & Scale Quarterly Review for <team>
## Top of Mind
* ... (Provide 0-3 bullet points summarizing biggest activities done or going on.
* ...
## Risks/Concerns
* ... (Provide 0-3 bullet points summarizing risks and concerns for in progress or planned work.)
* ...
## Coming up
* ... (Provide 0-3 bullet points summarizing planned work.)
* ...
## Collaboration Opportunities
* ... (Provide 0-3 bullet points summarizing team collaboration with other teams (like engineering or any other group besides <team>).)
* ...
```

## Step 3: Save the report

Write the finished report to `reports/<team>-<range>-<date>.md`, using the same `<team>`/`<range>`/`<date>` values as the raw file from Step 1. Then delete that `-raw.md` scratch file — it's not meant to be committed.

Completion criterion: `reports/<team>-<range>-<date>.md` exists and holds the full rendered report — not the raw data from Step 1 — and the `-raw.md` file from Step 1 no longer exists.
