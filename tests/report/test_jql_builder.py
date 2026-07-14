from jira_cli.report.jql_builder import (
    build_active_jql,
    build_completed_jql,
    build_in_review_jql,
    build_incoming_jql,
    build_stale_jql,
)

BASE = "project = TEST AND component = Perf"
START = "2026-06-01"
END = "2026-06-30"


class TestBuildCompletedJql:
    def test_basic(self):
        jql = build_completed_jql(BASE, START, END)
        assert "status CHANGED TO (Closed, Done)" in jql
        assert f'DURING ("{START}", "{END}")' in jql
        assert jql.startswith(BASE)


class TestBuildInReviewJql:
    def test_single_status(self):
        jql = build_in_review_jql(BASE, START, END, review_statuses=["Review"])
        assert "status in ('Review')" in jql
        assert "status CHANGED TO ('Review')" in jql

    def test_multiple_statuses(self):
        jql = build_in_review_jql(
            BASE, START, END, review_statuses=["Review", "Code Review"]
        )
        assert "'Review', 'Code Review'" in jql


class TestBuildActiveJql:
    def test_includes_commented(self):
        jql = build_active_jql(BASE, START, END, team_ids=["id1", "id2"])
        assert "status = 'In Progress'" in jql
        assert "commented('2026-06-01', '2026-06-30', id1, id2)" in jql
        assert "type not in (Feature, Outcome)" in jql

    def test_single_team_member(self):
        jql = build_active_jql(BASE, START, END, team_ids=["only-one"])
        assert "commented('2026-06-01', '2026-06-30', only-one)" in jql


class TestBuildIncomingJql:
    def test_basic(self):
        jql = build_incoming_jql(BASE, START, END)
        assert f'created >= "{START}"' in jql
        assert f'created < "{END}"' in jql
        assert "assignee is not EMPTY" in jql
        assert "status not in (Closed, Done)" in jql


class TestBuildStaleJql:
    def test_basic(self):
        jql = build_stale_jql(BASE)
        assert jql == f"{BASE} AND status = 'In Progress'"

    def test_ignores_extra_kwargs(self):
        jql = build_stale_jql(BASE, start=START, end=END, team_ids=["x"])
        assert jql == f"{BASE} AND status = 'In Progress'"
