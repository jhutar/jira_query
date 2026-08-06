---
disable-model-invocation: true
description: Generates a weekly, monthly, quarterly, or yearly report for a given team with a given form.
---

## Usage

This skill provides the command to generate raw data and guideance on how to form a final report from them.

**Invoke with:** `/generate-report <team> <range> <form>`

-   `<team>`: The team name (one of `Konflux`, `Pipelines`, `Satellite`, `ConsoleDot` also known as `HCC`).
-   `<range>`: The report range: `weekly` (use `1w`), `monthly` (use `1m`), `quarterly` (use `3m`), or `yearly` (use `12m`).
-   `<form>`: Form of a report, defaults to "Normal". See below for other possibilities.

## Step 1: Generate the data

Run the following command in your terminal to collect raw report data from Jira optionally enritched with content of linked pull requests, Slack threads and so on.

Redirect the output to temporary file so we can let user to review it later and to process it in an efficient way.

Note: If running for longer period than `weekly`, add `--no-enrich` option to disable enritchment and limit amount of data generated.

*   **weekly**: `./report-data.py --range 1w`
*   **monthly**: `./report-data.py --range 1m --no-enrich`
*   **quarterly**: `./report-data.py --range 3m --no-enrich`
*   **yearly**: `./report-data.py --range 12m --no-enrich`

```bash
./report-data.py --projects <project> --range <range> >"<some_temp_file>"   # optionally add `--no-enrich` option
```

## Step 2: Use the data with an LLM

Now generate status update based on the raw report data file content.

**Task:** Please synthesize this data into a breaf, professional, concise, high level weekly summary. Lanfuage NUST have minimum filer words, pleasantries and hedging language. NEVER assume things when something is unclear. Use Feature > Epic > Task/Story/Bug > Sub-task and story points (see "sp" in output) and Priority/Severity as indication of how big the task was.

Based on seleced report "form", pick one of the templates below:

### Report formed as "Normal"

´´´markdown
# Team <team> range <range>
* **Weekly Overview:** (Start with a 0-3 sentence overview of the most significant progress made across all teams this week. This is a bragging but honest section, but do not make up things.)
* **What was done:**
  * ... (Provide 0-3 bullet points summarizing team key activities. Focus on *outcomes* and *impact* (what was finished, what moved into review) rather than just listing ticket IDs, but include short links to the tickets. Use additional data to provide technical context where helpful.)
  * ...
* **What is moving:**
  * ... (Provide 0-3 bullet points summarizing transition of issues from "New" or "In Progress" to "In Review" or "Finished" (only if not already closed and mentioned in "What was done" section). Identify any blockers if they are apparent from the descriptions.)
  * ...
´´´

### Report formed as "Quarterly Review"

```markdown
# Perf & Scale Quarterly Review for <team>
## Top of Mind
* ... (Provide 0-3 bullet points summarizing biggest activities done or going on. Be VERY short, each bullet 10 words at max.)
* ...
## Risks/Concerns
* ... (Provide 0-3 bullet points summarizing risks and concerns for in progress or planed work. Be VERY short, each bullet 10 words at max.)
* ...
## Coming up
* ... (Provide 0-3 bullet points summarizing planed work. Be VERY short, each bullet 10 words at max.)
* ...
## Collaboration Opportunities
* ... (Provide 0-3 bullet points summarizing team collaboration with other teams (like engineering or any other group besides <team>). Be VERY short, each bullet 10 words at max.)
* ...
```
