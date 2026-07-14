import sys

from jira_cli.cli import convert_issue_adf_to_md
from jira_cli.pr_utils import enrich_issue_with_prs
from jira_cli.report.jql_builder import CATEGORY_BUILDERS
from jira_cli.report.project_configs import CATEGORY_TITLES, PROJECT_CONFIGS
from jira_cli.report.time_range import format_jql_date


class ReportRunner:
    def __init__(
        self, jira, user_resolver, renderer, start_date, end_date,
        projects, categories, assignee_emails,
    ):
        self._jira = jira
        self._resolver = user_resolver
        self._renderer = renderer
        self._start = format_jql_date(start_date)
        self._end = format_jql_date(end_date)
        self._projects = projects
        self._categories = categories
        self._assignee_ids = None
        if assignee_emails:
            self._assignee_ids = set()
            for email in assignee_emails:
                self._assignee_ids.add(user_resolver.get_account_id(email))

    def run(self):
        output = []
        for project_name in self._projects:
            config = PROJECT_CONFIGS.get(project_name)
            if not config:
                print(
                    f"Warning: Unknown project '{project_name}', skipping.",
                    file=sys.stderr,
                )
                continue

            output.append(f"# {project_name}")

            try:
                team_ids = self._resolver.get_team_ids(config["team"])
            except ValueError as e:
                print(f"Warning: {e}, skipping project.", file=sys.stderr)
                continue

            for category in self._categories:
                title = CATEGORY_TITLES[category]
                output.append(f"## {title}")

                if category == "stale":
                    issues = self._query_stale(config, team_ids)
                else:
                    issues = self._query_category(config, category, team_ids)

                self._post_process(issues)

                if self._assignee_ids is not None:
                    issues = self._filter_by_assignees(issues)

                rendered = self._renderer.render({"issues": issues})
                output.append(rendered)

            output.append("\n")

        return "\n".join(output)

    def _query_category(self, config, category, team_ids):
        builder = CATEGORY_BUILDERS[category]
        jql = builder(
            base_jql=config["base_jql"],
            start=self._start,
            end=self._end,
            review_statuses=config.get("review_statuses", []),
            team_ids=team_ids,
        )
        return list(self._jira.search_issues(jql, maxResults=False))

    def _query_stale(self, config, team_ids):
        builder = CATEGORY_BUILDERS["stale"]
        jql = builder(base_jql=config["base_jql"])
        issues = list(
            self._jira.search_issues(
                jql, expand="changelog", maxResults=False
            )
        )
        return [i for i in issues if self._is_stale(i, team_ids)]

    def _is_stale(self, issue, team_ids):
        team_ids_set = set(team_ids)

        if hasattr(issue, "changelog") and issue.changelog:
            for history in issue.changelog.histories:
                if not (self._start <= history.created[:10] <= self._end):
                    continue
                for item in history.items:
                    if item.field == "status":
                        return False

        if hasattr(issue.fields, "comment") and issue.fields.comment:
            for comment in issue.fields.comment.comments:
                if not (self._start <= comment.created[:10] <= self._end):
                    continue
                author_id = getattr(comment.author, "accountId", None) or getattr(
                    comment.author, "name", None
                )
                if author_id in team_ids_set:
                    return False

        return True

    def _post_process(self, issues):
        for issue in issues:
            convert_issue_adf_to_md(issue)
            enrich_issue_with_prs(issue)
            if hasattr(issue.fields, "comment") and issue.fields.comment:
                issue.fields.comment.comments = [
                    c
                    for c in issue.fields.comment.comments
                    if self._start <= c.created[:10] <= self._end
                ]

    def _filter_by_assignees(self, issues):
        filtered = []
        for issue in issues:
            if not issue.fields.assignee:
                continue
            assignee_id = getattr(
                issue.fields.assignee, "accountId", None
            ) or getattr(issue.fields.assignee, "name", None)
            if assignee_id in self._assignee_ids:
                filtered.append(issue)
        return filtered
