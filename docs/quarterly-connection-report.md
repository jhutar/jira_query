# Quarterly Connection Report

How to regenerate the brag-list / priorities report for the quarterly connection (performance review conversation).

## Steps

1. **Get completed work for the quarter** (brag list source):

   ```shell
   uv run report-data.py --categories completed --assignees <your-email> \
       --start <last-quarter-start> --end <last-quarter-end> --no-enrich > /tmp/report-completed.md
   ```

   Example for Q3 2026 (i.e. Jun-Sep 2026):

   ```shell
   uv run report-data.py --categories completed --assignees jhutar@redhat.com \
       --start 2026-06-01 --end 2026-09-01 --no-enrich > /tmp/report-completed.md
   ```

2. **Get in-progress work** (current priorities source):

   ```shell
   uv run report-data.py --categories active --assignees <your-email> \
       --start <last-quarter-start> --end <todays-date> --no-enrich > /tmp/report-active.md
   ```

3. **Summarize with an AI agent.** Feed both report files to the agent and ask
   for two answers:

   - *"What accomplishments are you most proud of last quarter? Reflect not
     only on WHAT you've accomplished but also on HOW you've accomplished it."*
     — max 10 bullets, max 2 sentences each, no filler words.
   - *"What are your top priorities for this quarter?"* — max 3 bullets,
     max 2 sentences each, no filler words.

4. **Review and adjust.** Verify ticket references and numbers against the
   raw reports before using the output.

## Notes

- Full output is large; read it in chunks.
- Tasks with bigger number of story points are more importnat for this
  report than smaller tasks.
- If possible group tasks per their epic as that alligns to a project.
