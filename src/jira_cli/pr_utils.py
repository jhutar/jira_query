#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import re
import subprocess


def _run_command(cmd, env=None):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, env=env
        )
        return result.stdout.strip(), None
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "No stderr"
        return (
            None,
            f"Command {cmd} failed with exit status {e.returncode}.\nStderr: {stderr}",
        )
    except Exception as e:
        return None, str(e)


def _get_github_pr(repo, pr_id):
    cmd = [
        "gh",
        "pr",
        "view",
        pr_id,
        "--repo",
        repo,
        "--json",
        "title,body",
        "--jq",
        '"Title: \\(.title)\\n\\(.body)"',
    ]
    stdout, error = _run_command(cmd)
    if error:
        return f"(Failed to fetch GitHub PR info: {error})"
    return stdout


def _get_github_commit(repo, sha):
    cmd = [
        "gh",
        "api",
        f"repos/{repo}/commits/{sha}",
        "--jq",
        '".commit.message"',
    ]
    stdout, error = _run_command(cmd)
    if error:
        return f"(Failed to fetch GitHub commit info: {error})"
    return f"Commit Message:\n{stdout}"


def _get_gitlab_mr(host, repo, mr_id):
    env = os.environ.copy()
    env["GL_HOST"] = host
    cmd = ["glab", "mr", "view", mr_id, "-R", repo, "-F", "json"]
    stdout, error = _run_command(cmd, env=env)
    if error:
        return f"(Failed to fetch GitLab MR info: {error})"
    data = json.loads(stdout)
    return f"Title: {data.get('title')}\n{data.get('description')}"


def _get_gitlab_commit(host, repo, sha):
    # GitLab API requires URL-encoded project path
    encoded_repo = repo.replace("/", "%2F")
    env = os.environ.copy()
    env["GL_HOST"] = host
    cmd = ["glab", "api", f"projects/{encoded_repo}/repository/commits/{sha}"]
    stdout, error = _run_command(cmd, env=env)
    if error:
        return f"(Failed to fetch GitLab commit info: {error})"
    data = json.loads(stdout)
    return f"Commit Message:\n{data.get('message', '').strip()}"


def get_pr_info(url):
    if "github.com" in url:
        # GitHub PR Pattern: https://github.com/owner/repo/pull/id
        pr_match = re.search(r"github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
        if pr_match:
            repo, pr_id = pr_match.groups()
            return _get_github_pr(repo, pr_id)

        # GitHub Commit Pattern: https://github.com/owner/repo/commit/sha
        commit_match = re.search(
            r"github\.com/([^/]+/[^/]+)/commit/([0-9a-f]{7,40})", url
        )
        if commit_match:
            repo, sha = commit_match.groups()
            return _get_github_commit(repo, sha)

    elif "gitlab" in url:
        # GitLab MR Pattern: https://host/path/to/repo/-/merge_requests/id
        mr_match = re.search(r"https://([^/]+)/(.+)/-/merge_requests/(\d+)", url)
        if mr_match:
            host, repo, mr_id = mr_match.groups()
            return _get_gitlab_mr(host, repo, mr_id)

        # GitLab Commit Pattern: https://host/path/to/repo/-/commit/sha
        commit_match = re.search(r"https://([^/]+)/(.+)/-/commit/([0-9a-f]{7,40})", url)
        if commit_match:
            host, repo, sha = commit_match.groups()
            return _get_gitlab_commit(host, repo, sha)

    return ""


def enrich_with_prs(text):
    if not text:
        return []
    # Find PR/Commit links
    # We stop at delimiters like |, ], ), or whitespace to handle Jira markdown links
    patterns = [
        r"https://github\.com/[^\s|\]\)]+/pull/\d+",
        r"https://github\.com/[^\s|\]\)]+/commit/[0-9a-f]{7,40}",
        r"https://gitlab[^\s|\]\)]*/-/merge_requests/\d+",
        r"https://gitlab[^\s|\]\)]*/-/commit/[0-9a-f]{7,40}",
    ]

    urls = []
    for p in patterns:
        urls += re.findall(p, text)

    urls = list(set(urls))

    enrichment = []
    for url in urls:
        info = get_pr_info(url)
        if info:
            enrichment.append({"url": url, "info": info})

    return enrichment


def enrich_issue_with_prs(issue):
    # Collect text only from explicitly requested fields to find PR links
    text_to_search = []

    # 1. Description
    if hasattr(issue.fields, "description") and issue.fields.description:
        text_to_search.append(issue.fields.description)

    # 2. Comments
    if hasattr(issue.fields, "comment") and issue.fields.comment:
        for comment in issue.fields.comment.comments:
            text_to_search.append(comment.body)

    # 3. "Git Pull Request" field (customfield_10875 in this workspace)
    if hasattr(issue.fields, "customfield_10875") and issue.fields.customfield_10875:
        val = issue.fields.customfield_10875
        if isinstance(val, str):
            text_to_search.append(val)
        elif isinstance(val, (list, tuple)):
            for item in val:
                if isinstance(item, str):
                    text_to_search.append(item)

    combined_text = "\n".join(text_to_search)
    issue.prs = enrich_with_prs(combined_text)
