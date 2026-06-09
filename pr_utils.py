#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import re
import subprocess

def get_pr_info(url):
    cmd = []
    try:
        if "github.com" in url:
            # Pattern: https://github.com/owner/repo/pull/id
            match = re.search(r"github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
            if match:
                repo, pr_id = match.groups()
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
                    '."Title: \\(.title)\\n\\(.body)"',
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return result.stdout.strip()
        elif "gitlab" in url:
            # Pattern: https://host/path/to/repo/-/merge_requests/id
            match = re.search(r"https://([^/]+)/(.+)/-/merge_requests/(\d+)", url)
            if match:
                host, repo, mr_id = match.groups()
                # Setting GL_HOST to gitlab.cee.redhat.com handles instances for this specific context
                env = os.environ.copy()
                env["GL_HOST"] = host
                cmd = ["glab", "mr", "view", mr_id, "-R", repo, "-F", "json"]
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=True, env=env
                )
                data = json.loads(result.stdout)
                return f"Title: {data.get('title')}\n{data.get('description')}"
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "No stderr"
        return f"(Failed to fetch PR info: Command {cmd} failed with exit status {e.returncode}.\nStderr: {stderr})"
    except Exception as e:
        return f"(Failed to fetch PR info: {e})"
    return ""


def enrich_with_prs(text):
    if not text:
        return []
    # Find PR links
    # We stop at delimiters like |, ], ), or whitespace to handle Jira markdown links
    # GitHub: any path followed by /pull/ and digits
    urls = re.findall(r"https://github\.com/[^\s|\]\)]+/pull/\d+", text)
    # GitLab: any path followed by /-/merge_requests/ and digits
    urls += re.findall(r"https://gitlab[^\s|\]\)]*/-/merge_requests/\d+", text)
    urls = list(set(urls))

    enrichment = []
    for url in urls:
        info = get_pr_info(url)
        if info:
            enrichment.append({"url": url, "info": info})

    return enrichment


def enrich_issue_with_prs(issue):
    # Collect text from all possible fields to find PR links
    text_to_search = []
    
    def collect_strings(val):
        if isinstance(val, str):
            text_to_search.append(val)
        elif isinstance(val, dict):
            for v in val.values():
                collect_strings(v)
        elif isinstance(val, (list, tuple)):
            for item in val:
                collect_strings(item)
    
    # Use raw data if available to be sure we see everything exactly as Jira sent it
    if hasattr(issue, 'raw') and 'fields' in issue.raw:
        collect_strings(issue.raw['fields'])
    
    # Also look at issue.fields attributes just in case jira-python did some processing
    if hasattr(issue, 'fields'):
        for field_name in dir(issue.fields):
            if field_name.startswith("_"):
                continue
            try:
                val = getattr(issue.fields, field_name)
                # Avoid re-scanning large objects we already handled or that might be circular
                if not isinstance(val, (str, list, tuple, dict)):
                    continue
                collect_strings(val)
            except AttributeError:
                continue

    combined_text = "\n".join(text_to_search)
    issue.prs = enrich_with_prs(combined_text)
