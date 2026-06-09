#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
from unittest.mock import patch
from pr_utils import enrich_with_prs

@pytest.fixture
def mock_get_pr_info():
    with patch("pr_utils.get_pr_info") as mock:
        mock.side_effect = lambda url: f"Mock info for {url}"
        yield mock

def test_enrich_with_prs_patterns(mock_get_pr_info):
    test_cases = [
        # Basic GitHub PR
        ("Check this: https://github.com/org/repo/pull/123", ["https://github.com/org/repo/pull/123"]),
        
        # Basic GitLab MR
        ("Check this: https://gitlab.com/org/repo/-/merge_requests/456", ["https://gitlab.com/org/repo/-/merge_requests/456"]),
        
        # Jira-style markdown links
        ("[PR #123|https://github.com/org/repo/pull/123]", ["https://github.com/org/repo/pull/123"]),
        ("[MR #456|https://gitlab.com/org/repo/-/merge_requests/456]", ["https://gitlab.com/org/repo/-/merge_requests/456"]),
        
        # Multiple links in text
        ("Fixes https://github.com/org/repo/pull/1 and https://github.com/org/repo/pull/2", 
         ["https://github.com/org/repo/pull/1", "https://github.com/org/repo/pull/2"]),
        
        # Links in parentheses
        ("(see https://github.com/org/repo/pull/789)", ["https://github.com/org/repo/pull/789"]),
        
        # Duplicated links should be unique
        ("Repeat: https://github.com/org/repo/pull/1 and https://github.com/org/repo/pull/1", 
         ["https://github.com/org/repo/pull/1"]),
        
        # GitLab with deep subgroups
        ("https://gitlab.cee.redhat.com/releng/sub/group/repo/-/merge_requests/123", 
         ["https://gitlab.cee.redhat.com/releng/sub/group/repo/-/merge_requests/123"]),
    ]

    for text, expected_urls in test_cases:
        results = enrich_with_prs(text)
        found_urls = [r["url"] for r in results]
        
        assert sorted(found_urls) == sorted(expected_urls), f"Failed for text: {text}"

if __name__ == "__main__":
    pytest.main([__file__])
