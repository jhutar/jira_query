disable-model-invocation: true
description: "Generates instructions for creating a weekly, monthly, quarterly, or yearly report for a given team."

## Usage

This skill provides the command to generate raw data and the prompt to use with an LLM to create a report.

**Invoke with:** `/generate-report <team> <range>`

-   `<team>`: The team name (e.g., `Konflux`, `Pipelines`).
-   `<range>`: The report range: `weekly`, `monthly`, `quarterly`, or `yearly`.

The skill will then provide you with a two-step process:
1.  A command to run in your terminal to get the report data.
2.  A complete prompt to use with your preferred LLM (like Gemini, Claude, etc.), which includes the content of the relevant `...-report-ai-prompt.txt` file.

---

## Example Walkthrough

**If you run:** `/generate-report Konflux weekly`

**The skill will respond with instructions like this:**

### Step 1: Generate the data

Run the following command in your terminal:

```bash
./report-data.py --projects Konflux --range 1w
```

### Step 2: Use the data with an LLM

Copy the output from the command above and paste it into the `[PASTE DATA HERE]` section of the prompt below. Then, use the combined text as a prompt for your LLM.

```text
# AI Weekly Report Summary Prompt

Execute this prompt in AI agent alongside with `./report-data.py --range 1w` output to generate a polished weekly status update.

Generate independent status update for each of the teams: Konflux, Pipelines, ConsoleDot, and Satellite.

---

**Context:** Attached is a raw data for the past 7 days, generated from Jira issues and linked Pull Request descriptions and Slack threads.

**Task:** Please synthesize this data into a breaf, professional, concise, high level weekly summary. Minimum filer words, pleasantries and hedging language. Do not assume things when something is unclear. Use Feature > Epic > Task/Story/Bug > Sub-task and story points (see "sp" in output) and Priority/Severity (neither currently not provided in the report) as indication of how big the task was.

**Requirements:**
1. **Weekly Overview:** Start with a 0-3 sentence overview of the most significant progress made across all teams this week. This is a honest bragging section, but do not made up things.
2. **What was done:** Provide 0-3 bullet points summarizing team key activities. Focus on *outcomes* and *impact* (what was finished, what moved into review) rather than just listing ticket IDs, but include short links to the tickets. Use additional data to provide technical context where helpful.
3. **What is moving:** Provide 0-3 bullet points summarizing transition of issues from "New" or "In Progress" to "In Review" or "Finished" (only if not already closed and mentioned in "What was done" section). Identify any blockers if they are apparent from the descriptions.
4. **Template:** Use this template:

´´´
# Team <team_name>
* **Weekly Overview:** ...
* **What was done:**
  * ...
  * ...
* **What is moving:**
  * ...
  * ...
´´´

**Input Data:**
[PASTE DATA HERE]
```

---
## Range to command mapping:

*   **weekly**: `./report-data.py --range 1w` (uses `weekly-report-ai-prompt.txt`)
*   **monthly**: `./report-data.py --range 1m` (uses `monthly-report-ai-prompt.txt`)
*   **quarterly**: `./report-data.py --range 3m` (uses `monthly-report-ai-prompt.txt`)
*   **yearly**: `./report-data.py --range 12m` (uses `monthly-report-ai-prompt.txt`)
