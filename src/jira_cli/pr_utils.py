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


def _truncate_diff(text, max_lines=200):
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    truncated = "\n".join(lines[:max_lines])
    return f"{truncated}\n... (truncated, showing {max_lines} of {len(lines)} lines)"


def _get_github_pr(repo, pr_id, with_diff=False):
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
    result = stdout
    if with_diff:
        diff_cmd = ["gh", "pr", "diff", pr_id, "--repo", repo]
        diff_stdout, diff_error = _run_command(diff_cmd)
        if diff_error:
            result += f"\n\nDiff:\n(Failed to fetch diff: {diff_error})"
        elif diff_stdout:
            result += f"\n\nDiff:\n{_truncate_diff(diff_stdout)}"
    return result


def _get_github_commit(repo, sha, with_diff=False):
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
    result = f"Commit Message:\n{stdout}"
    if with_diff:
        diff_cmd = [
            "gh",
            "api",
            f"repos/{repo}/commits/{sha}",
            "--jq",
            '.files[] | "--- \\(.filename)\\n\\(.patch // "")"',
        ]
        diff_stdout, diff_error = _run_command(diff_cmd)
        if diff_error:
            result += f"\n\nDiff:\n(Failed to fetch diff: {diff_error})"
        elif diff_stdout:
            result += f"\n\nDiff:\n{_truncate_diff(diff_stdout)}"
    return result


def _get_gitlab_mr(host, repo, mr_id, with_diff=False):
    env = os.environ.copy()
    env["GL_HOST"] = host
    cmd = ["glab", "mr", "view", mr_id, "-R", repo, "-F", "json"]
    stdout, error = _run_command(cmd, env=env)
    if error:
        return f"(Failed to fetch GitLab MR info: {error})"
    data = json.loads(stdout)
    result = f"Title: {data.get('title')}\n{data.get('description')}"
    if with_diff:
        diff_cmd = ["glab", "mr", "diff", mr_id, "-R", repo]
        diff_stdout, diff_error = _run_command(diff_cmd, env=env)
        if diff_error:
            result += f"\n\nDiff:\n(Failed to fetch diff: {diff_error})"
        elif diff_stdout:
            result += f"\n\nDiff:\n{_truncate_diff(diff_stdout)}"
    return result


def _get_gitlab_commit(host, repo, sha, with_diff=False):
    encoded_repo = repo.replace("/", "%2F")
    env = os.environ.copy()
    env["GL_HOST"] = host
    cmd = ["glab", "api", f"projects/{encoded_repo}/repository/commits/{sha}"]
    stdout, error = _run_command(cmd, env=env)
    if error:
        return f"(Failed to fetch GitLab commit info: {error})"
    data = json.loads(stdout)
    result = f"Commit Message:\n{data.get('message', '').strip()}"
    if with_diff:
        diff_cmd = [
            "glab",
            "api",
            f"projects/{encoded_repo}/repository/commits/{sha}/diff",
        ]
        diff_stdout, diff_error = _run_command(diff_cmd, env=env)
        if diff_error:
            result += f"\n\nDiff:\n(Failed to fetch diff: {diff_error})"
        elif diff_stdout:
            diff_data = json.loads(diff_stdout)
            diff_lines = []
            for entry in diff_data:
                diff_lines.append(f"--- {entry.get('old_path', '')}")
                diff_lines.append(f"+++ {entry.get('new_path', '')}")
                diff_lines.append(entry.get("diff", ""))
            result += f"\n\nDiff:\n{_truncate_diff(chr(10).join(diff_lines))}"
    return result


def _get_slack_message(url):
    cmd = ["slack-cli", "read", url]
    stdout, error = _run_command(cmd)
    if error:
        return f"(Failed to fetch Slack message: {error})"
    return stdout


def get_pr_info(url, with_diff=False):
    if "github.com" in url:
        pr_match = re.search(r"github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
        if pr_match:
            repo, pr_id = pr_match.groups()
            return _get_github_pr(repo, pr_id, with_diff=with_diff)

        commit_match = re.search(
            r"github\.com/([^/]+/[^/]+)/commit/([0-9a-f]{7,40})", url
        )
        if commit_match:
            repo, sha = commit_match.groups()
            return _get_github_commit(repo, sha, with_diff=with_diff)

    if "slack.com/archives/" in url:
        return _get_slack_message(url)

    if "gitlab" in url:
        mr_match = re.search(r"https://([^/]+)/(.+)/-/merge_requests/(\d+)", url)
        if mr_match:
            host, repo, mr_id = mr_match.groups()
            return _get_gitlab_mr(host, repo, mr_id, with_diff=with_diff)

        commit_match = re.search(r"https://([^/]+)/(.+)/-/commit/([0-9a-f]{7,40})", url)
        if commit_match:
            host, repo, sha = commit_match.groups()
            return _get_gitlab_commit(host, repo, sha, with_diff=with_diff)

    return ""


def enrich_with_prs(text, with_diff=False):
    if not text:
        return []
    patterns = [
        r"https://github\.com/[^\s|\]\)]+/pull/\d+",
        r"https://github\.com/[^\s|\]\)]+/commit/[0-9a-f]{7,40}",
        r"https://gitlab[^\s|\]\)]*/-/merge_requests/\d+",
        r"https://gitlab[^\s|\]\)]*/-/commit/[0-9a-f]{7,40}",
        r"https://[^\s|\]\)]*slack\.com/archives/[^\s|\]\)]+",
    ]

    urls = []
    for p in patterns:
        urls += re.findall(p, text)

    urls = list(set(urls))

    enrichment = []
    for url in urls:
        info = get_pr_info(url, with_diff=with_diff)
        if info:
            enrichment.append({"url": url, "info": info})

    return enrichment
