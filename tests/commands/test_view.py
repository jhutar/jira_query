#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
from pathlib import Path

from unittest.mock import MagicMock, patch

from jira_cli.commands import view


def test_view_prints_issue_details(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-123"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-123"
    mock_issue.fields.summary = "Investigate Pipeline performance issues"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "In Progress"
    mock_issue.fields.assignee.displayName = "John Doe"
    mock_issue.fields.assignee.emailAddress = "john.doe@redhat.com"
    mock_issue.fields.reporter.displayName = "Jane Smith"
    mock_issue.fields.priority.name = "Major"
    mock_issue.fields.description = "Plain text description"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", 5.0)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "KONFLUX-123" in output
    assert "In Progress" in output
    assert "Task" in output
    assert "Points: 5.0" in output
    assert "Investigate Pipeline performance issues" in output
    assert "John Doe (john.doe@redhat.com)" in output
    assert "Jane Smith" in output
    assert "Major" in output
    assert "Plain text description" in output


@patch("jira_cli.commands.view._translate_content")
def test_view_converts_adf_description(mock_translate, mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-456"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    adf_desc = {"type": "doc", "content": []}
    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-456"
    mock_issue.raw = {"fields": {"description": adf_desc}}
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Bug"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = adf_desc
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_translate.return_value = "Converted markdown description"

    view.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    output = capsys.readouterr().out
    assert "Converted markdown description" in output
    assert "Unassigned" in output


@patch("jira_cli.commands.view._translate_content")
def test_view_description_not_raw_object(mock_translate, mock_ctx, mock_args, capsys):
    """Ensure PropertyHolder description objects are converted via raw ADF, not repr()."""
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-789"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    adf_desc = {
        "type": "doc",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
        ],
    }
    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-789"
    mock_issue.raw = {"fields": {"description": adf_desc}}
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "New"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = MagicMock()
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_translate.return_value = "Hello markdown"

    view.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_desc))
    output = capsys.readouterr().out
    assert "Hello markdown" in output
    assert "PropertyHolder" not in output
    assert "MagicMock" not in output


@patch("jira_cli.commands.view._translate_content")
def test_view_converts_adf_comments(mock_translate, mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-789"
    mock_args.with_comments = True
    mock_args.with_enrichment = False

    adf_body = {"type": "doc", "content": []}
    mock_comment = MagicMock()
    mock_comment.author.displayName = "Alice"
    mock_comment.created = "2026-06-18T14:20:00.000+0000"
    mock_comment.body = adf_body

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-789"
    mock_issue.raw = {"fields": {"comment": {"comments": [{"body": adf_body}]}}}
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_translate.return_value = "Comment in markdown"

    view.run(mock_ctx, mock_args)

    mock_translate.assert_called_once_with("to-md", json.dumps(adf_body))
    output = capsys.readouterr().out
    assert "Alice" in output
    assert "Comment in markdown" in output


def test_view_dump_writes_json(mock_ctx, mock_args, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-100"
    mock_args.dump = True
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-100"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_issue.raw = {"key": "KONFLUX-100", "fields": {}}
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output_file = Path("jira_issue_details") / "issue-KONFLUX-100.json"
    assert output_file.exists()
    with open(output_file, "r") as f:
        data = json.load(f)
    assert data["key"] == "KONFLUX-100"
    output_file.unlink()
    try:
        Path("jira_issue_details").rmdir()
    except OSError:
        pass


def test_view_no_comments_by_default(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-200"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Bob"
    mock_comment.created = "2026-06-18T10:00:00.000+0000"
    mock_comment.body = "This should not appear"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-200"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Comments:" not in output
    assert "Bob" not in output
    assert "This should not appear" not in output


def test_view_with_comments(mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-201"
    mock_args.with_comments = True
    mock_args.with_enrichment = False

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Alice"
    mock_comment.created = "2026-06-18T14:20:00.000+0000"
    mock_comment.body = "Great progress on this"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-201"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Comments:" in output
    assert "Alice" in output
    assert "Great progress on this" in output


@patch("jira_cli.commands.view.enrich_with_prs")
def test_view_with_enrichment(mock_enrich, mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-202"
    mock_args.with_comments = False
    mock_args.with_enrichment = True

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-202"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "See https://github.com/org/repo/pull/42"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_enrich.return_value = [
        {
            "url": "https://github.com/org/repo/pull/42",
            "info": "Title: Fix bug\nSome body",
        },
    ]

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Enrichment:" in output
    assert "https://github.com/org/repo/pull/42" in output
    assert "Title: Fix bug" in output
    mock_enrich.assert_called_once()


@patch("jira_cli.commands.view.enrich_with_prs")
def test_view_enrichment_includes_comments(mock_enrich, mock_ctx, mock_args, capsys):
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-203"
    mock_args.with_comments = True
    mock_args.with_enrichment = True

    mock_comment = MagicMock()
    mock_comment.author.displayName = "Dev"
    mock_comment.created = "2026-06-18T10:00:00.000+0000"
    mock_comment.body = "Fixed in https://github.com/org/repo/pull/99"

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-203"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "Some description"
    mock_issue.fields.comment.comments = [mock_comment]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_enrich.return_value = []

    view.run(mock_ctx, mock_args)

    call_text = mock_enrich.call_args[0][0]
    assert "Some description" in call_text
    assert "Fixed in https://github.com/org/repo/pull/99" in call_text


@patch("jira_cli.commands.view.enrich_with_prs")
def test_view_with_diff_passes_flag(mock_enrich, mock_ctx, mock_args, capsys):
    """--with-diff implies --with-enrichment and passes with_diff=True."""
    mock_args.subparser_name = "view"
    mock_args.issue_key = "KONFLUX-300"
    mock_args.with_comments = False
    mock_args.with_enrichment = False
    mock_args.with_diff = True

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-300"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "See https://github.com/org/repo/pull/1"
    mock_issue.fields.comment.comments = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    mock_enrich.return_value = []

    view.run(mock_ctx, mock_args)

    mock_enrich.assert_called_once()
    assert mock_enrich.call_args[1]["with_diff"] is True


def test_view_shows_links(mock_ctx, mock_args, capsys):
    mock_args.issue_key = "KONFLUX-500"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    outward_link = MagicMock()
    outward_link.type.outward = "blocks"
    outward_link.outwardIssue.key = "KONFLUX-501"

    inward_link = MagicMock()
    inward_link.type.inward = "is blocked by"
    inward_link.inwardIssue.key = "KONFLUX-502"
    del inward_link.outwardIssue

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-500"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = []
    mock_issue.fields.issuelinks = [outward_link, inward_link]
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Links:" in output
    assert "blocks KONFLUX-501" in output
    assert "is blocked by KONFLUX-502" in output


def test_view_no_links(mock_ctx, mock_args, capsys):
    mock_args.issue_key = "KONFLUX-600"
    mock_args.with_comments = False
    mock_args.with_enrichment = False

    mock_issue = MagicMock()
    mock_issue.key = "KONFLUX-600"
    mock_issue.fields.summary = "Test"
    mock_issue.fields.issuetype.name = "Task"
    mock_issue.fields.status.name = "Open"
    mock_issue.fields.assignee = None
    mock_issue.fields.reporter = None
    mock_issue.fields.priority = None
    mock_issue.fields.description = "desc"
    mock_issue.fields.comment.comments = []
    mock_issue.fields.issuelinks = []
    setattr(mock_issue.fields, "customfield_10002", None)
    setattr(mock_issue.fields, "customfield_10005", None)
    mock_issue.fields.parent = None
    mock_ctx.jira.issue.return_value = mock_issue

    view.run(mock_ctx, mock_args)

    output = capsys.readouterr().out
    assert "Links:" not in output
