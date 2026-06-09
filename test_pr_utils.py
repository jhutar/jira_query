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
        
        # User reported patterns (Jira links with brackets and formatting)
        ("PR [konflux-ci/build-definitions#3560|https://github.com/konflux-ci/build-definitions/pull/3560] has been closed without merging.",
         ["https://github.com/konflux-ci/build-definitions/pull/3560"]),
        
        ("requested a new tenant with [+https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006+|https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006]",
         ["https://gitlab.cee.redhat.com/releng/konflux-release-data/-/merge_requests/18006"]),
        
        # Smart links (duplicated URL in one pattern)
        ("PR for artifact validation improvements (addressing feedback from PR #67):\n[https://github.com/konflux-ci/perfscale/pull/68|https://github.com/konflux-ci/perfscale/pull/68|smart-link]",
         ["https://github.com/konflux-ci/perfscale/pull/68"]),
        
        # GitHub Commit links
        ("Fix in https://github.com/redhat-performance/opl/commit/82e4d494f495e7406e0ad85b0f4eedef369eda71",
         ["https://github.com/redhat-performance/opl/commit/82e4d494f495e7406e0ad85b0f4eedef369eda71"]),
        
        # GitLab Commit links
        ("Merged in https://gitlab.cee.redhat.com/konflux/docs/users/-/commit/e8a9f510d4554d129a10af1fc671b3af1c53d729",
         ["https://gitlab.cee.redhat.com/konflux/docs/users/-/commit/e8a9f510d4554d129a10af1fc671b3af1c53d729"]),
    ]

    for text, expected_urls in test_cases:
        results = enrich_with_prs(text)
        found_urls = [r["url"] for r in results]
        
        assert sorted(found_urls) == sorted(expected_urls), f"Failed for text: {text}"

if __name__ == "__main__":
    pytest.main([__file__])
