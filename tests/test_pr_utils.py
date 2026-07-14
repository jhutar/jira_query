#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
from unittest.mock import patch
from jira_cli.pr_utils import (
    _get_github_commit,
    _get_github_pr,
    _get_gitlab_commit,
    _get_gitlab_mr,
    _get_slack_message,
    _truncate_diff,
    enrich_with_prs,
    enrich_issue_with_prs,
)


@pytest.fixture
def mock_get_pr_info():
    with patch("jira_cli.pr_utils.get_pr_info") as mock:
        mock.side_effect = lambda url, with_diff=False: f"Mock info for {url}"
        yield mock


def test_enrich_with_prs_patterns(mock_get_pr_info):
    test_cases = [
        # Basic GitHub PR
        (
            "Check this: https://github.com/org/repo/pull/123",
            ["https://github.com/org/repo/pull/123"],
        ),
        # Basic GitLab MR
        (
            "Check this: https://gitlab.com/org/repo/-/merge_requests/456",
            ["https://gitlab.com/org/repo/-/merge_requests/456"],
        ),
        # Jira-style markdown links
        (
            "[PR #123|https://github.com/org/repo/pull/123]",
            ["https://github.com/org/repo/pull/123"],
        ),
        (
            "[MR #456|https://gitlab.com/org/repo/-/merge_requests/456]",
            ["https://gitlab.com/org/repo/-/merge_requests/456"],
        ),
        # Multiple links in text
        (
            "Fixes https://github.com/org/repo/pull/1 and https://github.com/org/repo/pull/2",
            [
                "https://github.com/org/repo/pull/1",
                "https://github.com/org/repo/pull/2",
            ],
        ),
        # Links in parentheses
        (
            "(see https://github.com/org/repo/pull/789)",
            ["https://github.com/org/repo/pull/789"],
        ),
        # Duplicated links should be unique
        (
            "Repeat: https://github.com/org/repo/pull/1 and https://github.com/org/repo/pull/1",
            ["https://github.com/org/repo/pull/1"],
        ),
        # GitLab with deep subgroups
        (
            "https://gitlab.cee.redhat.com/releng/sub/group/repo/-/merge_requests/123",
            [
                "https://gitlab.cee.redhat.com/releng/sub/group/repo/-/merge_requests/123"
            ],
        ),
        # User reported patterns (Jira links with brackets and formatting)
        (
            "PR [konflux-ci/build-definitions#3560|https://github.com/konflux-ci/build-definitions/pull/3560] has been closed without merging.",
            ["https://github.com/konflux-ci/build-definitions/pull/3560"],
        ),
        (
            "requested a new tenant with [+https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006+|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006]",
            [
                "https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006"
            ],
        ),
        # Smart links (duplicated URL in one pattern)
        (
            "PR for artifact validation improvements (addressing feedback from PR #67):\n[https://github.com/konflux-ci/perfscale/pull/68|https://github.com/konflux-ci/perfscale/pull/68|smart-link]",
            ["https://github.com/konflux-ci/perfscale/pull/68"],
        ),
        # GitHub Commit links
        (
            "Fix in https://github.com/redhat-performance/opl/commit/82e4d494f495e7406e0ad85b0f4eedef369eda71",
            [
                "https://github.com/redhat-performance/opl/commit/82e4d494f495e7406e0ad85b0f4eedef369eda71"
            ],
        ),
        # GitLab Commit links
        (
            "Merged in https://gitlab.cee.redhat.com/konflux/docs/users/-/commit/e8a9f510d4554d129a10af1fc671b3af1c53d729",
            [
                "https://gitlab.cee.redhat.com/konflux/docs/users/-/commit/e8a9f510d4554d129a10af1fc671b3af1c53d729"
            ],
        ),
        # Basic Slack message link
        (
            "Discussed in https://redhat-internal.slack.com/archives/C04JGQCNX6G/p1781711732712279",
            [
                "https://redhat-internal.slack.com/archives/C04JGQCNX6G/p1781711732712279"
            ],
        ),
        # Slack link in Jira markdown
        (
            "[thread|https://redhat-internal.slack.com/archives/C04JGQCNX6G/p1781711732712279]",
            [
                "https://redhat-internal.slack.com/archives/C04JGQCNX6G/p1781711732712279"
            ],
        ),
        # Trailing comma after Slack URL
        (
            "https://redhat-internal.slack.com/archives/C02CTEB3MMF/p1781072128218249, and more",
            [
                "https://redhat-internal.slack.com/archives/C02CTEB3MMF/p1781072128218249"
            ],
        ),
        # Trailing > after Slack URL (ADF artifact)
        (
            "https://redhat.enterprise.slack.com/archives/C0AUHMVNBAS>",
            ["https://redhat.enterprise.slack.com/archives/C0AUHMVNBAS"],
        ),
        # Trailing period after GitHub PR
        (
            "Fixed in https://github.com/org/repo/pull/42.",
            ["https://github.com/org/repo/pull/42"],
        ),
    ]

    for text, expected_urls in test_cases:
        results = enrich_with_prs(text)
        found_urls = [r["url"] for r in results]

        assert sorted(found_urls) == sorted(expected_urls), f"Failed for text: {text}"


def test_enrich_with_prs_passes_with_diff(mock_get_pr_info):
    text = "Check https://github.com/org/repo/pull/1"
    enrich_with_prs(text, with_diff=True)

    mock_get_pr_info.assert_called_once_with(
        "https://github.com/org/repo/pull/1", with_diff=True
    )


def test_truncate_diff_under_limit():
    text = "\n".join(f"line {i}" for i in range(50))
    assert _truncate_diff(text) == text


def test_truncate_diff_over_limit():
    text = "\n".join(f"line {i}" for i in range(300))
    result = _truncate_diff(text)
    assert result.count("\n") == 200
    assert "truncated, showing 200 of 300 lines" in result


@patch("jira_cli.pr_utils._run_command")
def test_get_github_pr_success(mock_run):
    mock_run.return_value = ("Title: Fix bug\nBody text", None)
    result = _get_github_pr("org/repo", "42")
    assert "Title: Fix bug" in result
    cmd = mock_run.call_args[0][0]
    assert "gh" in cmd
    assert "--repo" in cmd
    assert "org/repo" in cmd


@patch("jira_cli.pr_utils._run_command")
def test_get_github_pr_with_diff(mock_run):
    mock_run.side_effect = [
        ("Title: Fix bug", None),
        ("diff --git a/f.py b/f.py\n+added", None),
    ]
    result = _get_github_pr("org/repo", "42", with_diff=True)
    assert "Diff:" in result
    assert "+added" in result
    assert mock_run.call_count == 2


@patch("jira_cli.pr_utils._run_command")
def test_get_github_pr_failure(mock_run):
    mock_run.return_value = (None, "not found")
    result = _get_github_pr("org/repo", "999")
    assert "Failed to fetch GitHub PR info" in result


@patch("jira_cli.pr_utils._run_command")
def test_get_github_commit_success(mock_run):
    mock_run.return_value = ("Fix the thing", None)
    result = _get_github_commit("org/repo", "abc123")
    assert "Commit Message:" in result
    assert "Fix the thing" in result


@patch("jira_cli.pr_utils._run_command")
def test_get_gitlab_mr_success(mock_run):
    mock_run.return_value = ('{"title": "Add feature", "description": "Details"}', None)
    result = _get_gitlab_mr("gitlab.example.com", "org/repo", "10")
    assert "Title: Add feature" in result
    assert "Details" in result
    env = mock_run.call_args[1]["env"]
    assert env["GL_HOST"] == "gitlab.example.com"


@patch("jira_cli.pr_utils._run_command")
def test_get_gitlab_commit_success(mock_run):
    mock_run.return_value = ('{"message": "Fix stuff\\n"}', None)
    result = _get_gitlab_commit("gitlab.example.com", "org/repo", "def456")
    assert "Commit Message:" in result
    assert "Fix stuff" in result


@patch("jira_cli.pr_utils._run_command")
def test_get_slack_message_success(mock_run):
    mock_run.return_value = ("Slack message content", None)
    result = _get_slack_message("https://slack.com/archives/C123/p456")
    assert result == "Slack message content"


def test_enrich_issue_with_prs(mock_get_pr_info):
    class MockComment:
        def __init__(self, body):
            self.body = body

    class MockComments:
        def __init__(self, comments):
            self.comments = comments

    class MockFields:
        def __init__(self):
            self.description = "Fix: https://github.com/org/repo/pull/123"
            self.comment = MockComments(
                [MockComment("Also check: https://github.com/org/repo/pull/456")]
            )
            self.customfield_10875 = "https://gitlab.com/org/repo/-/merge_requests/789"

    class MockIssue:
        def __init__(self):
            self.fields = MockFields()

    issue = MockIssue()
    enrich_issue_with_prs(issue)

    assert hasattr(issue, "prs")
    urls = [item["url"] for item in issue.prs]
    assert "https://github.com/org/repo/pull/123" in urls
    assert "https://github.com/org/repo/pull/456" in urls
    assert "https://gitlab.com/org/repo/-/merge_requests/789" in urls


if __name__ == "__main__":
    pytest.main([__file__])
