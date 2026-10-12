# Quarterly Connection Report

How to regenerate the brag-list / priorities report for the quarterly connection (performance review conversation).

## Steps

1. **Get completed work for the quarter** (brag list source):

   ```shell
   uv run report-data.py --categories completed --assignees <your-email> \
       --start <quarter-start> --end <quarter-end> --no-enrich > /tmp/report-completed.md
   ```

   Example for Q3-ish window (Jun-Sep 2026):

   ```shell
   uv run report-data.py --categories completed --assignees jhutar@redhat.com \
       --start 2026-06-01 --end 2026-09-01 --no-enrich > /tmp/report-completed.md
   ```

2. **Get in-progress work** (current priorities source). Note: category is
   `active`, not `in_progress` (see `--categories` choices in `report-data.py`;
   valid values: `completed, in-review, active, incoming, stale`):

   ```shell
   uv run report-data.py --categories active --assignees jhutar@redhat.com \
       --start 2026-06-01 --end 2026-10-12 --no-enrich > /tmp/report-active.md
   ```

   Set `--end` to today's date.

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

- Always use `--no-enrich`: the PR/commit/Slack enrichment (`glab`,
  `slack-cli`) hangs or 404s and can time out the run. Output is still rich
  enough (descriptions + comments) for summarization.
- Some project queries may fail server-side (e.g. Satellite returned Jira
  HTTP 500); the rest of the report is still generated.
- Full output is large (~2600 lines); read it in chunks.
