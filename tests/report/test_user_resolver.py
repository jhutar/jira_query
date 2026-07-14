import json
from unittest.mock import MagicMock

import pytest

from jira_cli.report.user_resolver import UserResolver


@pytest.fixture
def tmp_paths(tmp_path, monkeypatch):
    users_path = tmp_path / "users.json"
    teams_path = tmp_path / "teams.json"
    monkeypatch.setattr("jira_cli.report.user_resolver.USERS_PATH", users_path)
    monkeypatch.setattr("jira_cli.report.user_resolver.TEAMS_PATH", teams_path)
    return users_path, teams_path


def _make_user(display_name, email, account_id):
    user = MagicMock()
    user.displayName = display_name
    user.emailAddress = email
    user.accountId = account_id
    return user


class TestLoadTeams:
    def test_missing_teams_file_exits(self, tmp_paths):
        users_path, teams_path = tmp_paths
        jira = MagicMock()
        with pytest.raises(SystemExit):
            UserResolver(jira)

    def test_invalid_json_exits(self, tmp_paths):
        users_path, teams_path = tmp_paths
        teams_path.write_text("{bad json", encoding="utf-8")
        jira = MagicMock()
        with pytest.raises(SystemExit):
            UserResolver(jira)


class TestLoadUsers:
    def test_creates_empty_users_file(self, tmp_paths):
        users_path, teams_path = tmp_paths
        teams_path.write_text('{"TEAM_A": ["a@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        UserResolver(jira)
        assert users_path.exists()
        assert json.loads(users_path.read_text(encoding="utf-8")) == {}

    def test_loads_existing_users(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text('{"a@test.com": "id-a"}', encoding="utf-8")
        teams_path.write_text('{"TEAM_A": ["a@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        resolver = UserResolver(jira)
        assert resolver.get_account_id("a@test.com") == "id-a"
        jira.search_users.assert_not_called()


class TestGetAccountId:
    def test_cached_no_api_call(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text('{"a@test.com": "id-a"}', encoding="utf-8")
        teams_path.write_text('{"T": ["a@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        resolver = UserResolver(jira)
        assert resolver.get_account_id("a@test.com") == "id-a"
        jira.search_users.assert_not_called()

    def test_uncached_calls_api_and_caches(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text('{"T": ["b@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        jira.search_users.return_value = [
            _make_user("Bob", "b@test.com", "id-b")
        ]
        resolver = UserResolver(jira)
        assert resolver.get_account_id("b@test.com") == "id-b"
        jira.search_users.assert_called_once()
        saved = json.loads(users_path.read_text(encoding="utf-8"))
        assert saved["b@test.com"] == "id-b"

    def test_ambiguous_resolves_by_email(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text('{"T": ["c@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        jira.search_users.return_value = [
            _make_user("Charlie X", "cx@test.com", "id-cx"),
            _make_user("Charlie", "c@test.com", "id-c"),
        ]
        resolver = UserResolver(jira)
        assert resolver.get_account_id("c@test.com") == "id-c"

    def test_no_match_raises(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text('{"T": ["x@test.com"]}', encoding="utf-8")
        jira = MagicMock()
        jira.search_users.return_value = []
        resolver = UserResolver(jira)
        with pytest.raises(ValueError, match="Expected exactly one"):
            resolver.get_account_id("x@test.com")


class TestGetTeamEmails:
    def test_returns_emails(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text(
            '{"A": ["a@t.com", "b@t.com"], "B": ["c@t.com"]}',
            encoding="utf-8",
        )
        jira = MagicMock()
        resolver = UserResolver(jira)
        assert resolver.get_team_emails("A") == ["a@t.com", "b@t.com"]

    def test_unknown_team_raises(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text('{"A": ["a@t.com"]}', encoding="utf-8")
        jira = MagicMock()
        resolver = UserResolver(jira)
        with pytest.raises(ValueError, match="not found"):
            resolver.get_team_emails("NOPE")


class TestGetTeamIds:
    def test_resolves_all_emails(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text(
            '{"a@t.com": "id-a", "b@t.com": "id-b"}', encoding="utf-8"
        )
        teams_path.write_text('{"X": ["a@t.com", "b@t.com"]}', encoding="utf-8")
        jira = MagicMock()
        resolver = UserResolver(jira)
        assert resolver.get_team_ids("X") == ["id-a", "id-b"]


class TestGetAllTeamEmails:
    def test_deduplicates_across_teams(self, tmp_paths):
        users_path, teams_path = tmp_paths
        users_path.write_text("{}", encoding="utf-8")
        teams_path.write_text(
            '{"A": ["a@t.com", "shared@t.com"], "B": ["b@t.com", "shared@t.com"]}',
            encoding="utf-8",
        )
        jira = MagicMock()
        resolver = UserResolver(jira)
        emails = resolver.get_all_team_emails()
        assert emails == ["a@t.com", "b@t.com", "shared@t.com"]
