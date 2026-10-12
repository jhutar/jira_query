# Quarterly Connection Report

How to regenerate the brag-list / priorities report for the quarterly connection (performance review conversation).

## Steps

1. **Get completed work for the quarter** (brag list source):

   Quarter boundaries: calendar quarters. If today is in Q<N> of year <Y>, then
   `<last-quarter-start>` is the first day of Q<N-1> and `<last-quarter-end>` is
   the first day of the current quarter (exclusive end). Example: today in Q4 2026
   -> last quarter is Q3 2026 -> `--start 2026-06-01 --end 2026-09-01`.

   ```shell
   uv run report-data.py --categories completed --assignees <your-email> \
       --start <last-quarter-start> --end <last-quarter-end> --no-enrich > /tmp/report-completed.md
   ```

   Example for Q3 2026 (i.e. Jun-Sep 2026):

   ```shell
   uv run report-data.py --categories completed --assignees jhutar@redhat.com \
       --start 2026-06-01 --end 2026-09-01 --no-enrich > /tmp/report-completed.md
   ```

2. **Get in-progress work** (current priorities source). Same start as step 1,
   end = today (includes early current-quarter work, which is what you want for
   "current priorities"):

   ```shell
   uv run report-data.py --categories active --assignees <your-email> \
       --start <last-quarter-start> --end <todays-date> --no-enrich > /tmp/report-active.md
   ```

3. **Summarize with an AI agent.** Feed both report files to the agent and use
   this prompt (adjust quarter name):

   > You are writing a quarterly connection (performance review) summary.
   > Read /tmp/report-completed.md (completed work for Q<N> <Y>) and
   > /tmp/report-active.md (in-progress work).
   >
   > Answer two questions:
   >
   > 1. "What accomplishments are you most proud of last quarter? Reflect not
   >    only on WHAT you've accomplished but also on HOW you've accomplished it."
   >    — max 10 bullets, max 2 sentences each, no filler words.
   > 2. "What are your top priorities for this quarter?" — max 3 bullets,
   >    max 2 sentences each, no filler words.
   >
   > Rules:
   > - Full output is large; read it in chunks.
   > - Tasks with higher story points matter more than tasks with fewer.
   > - Group tasks by their epic where possible (an epic aligns to a project).
   > - Keep ticket references (e.g. KONFLUX-12345) in the bullets so claims can
   >   be verified against the raw reports.
   > - Note where work is currently blocked — it feeds the priorities answer.

4. **Review and adjust.** Verify ticket references and numbers against the
   raw reports before using the output. Save the result (e.g. as
   `docs/connection-reports/<year>-Q<n>.md`) so past summaries are diffable.
