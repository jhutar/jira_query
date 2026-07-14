import json
import sys
from pathlib import Path


USERS_PATH = Path("~/.jira-cli/users.json").expanduser()
TEAMS_PATH = Path("~/.jira-cli/teams.json").expanduser()

TEAMS_EXAMPLE = """\
Example ~/.jira-cli/teams.json:
{
    "KONFLUX": ["alice@redhat.com", "bob@redhat.com"],
    "HCEPERF": ["carol@redhat.com", "dave@redhat.com"]
}"""


class UserResolver:
    def __init__(self, jira_client):
        self._jira = jira_client
        self._users = self._load_users()
        self._teams = self._load_teams()

    def _load_users(self):
        if not USERS_PATH.exists():
            USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
            USERS_PATH.write_text("{}", encoding="utf-8")
            return {}
        try:
            return json.loads(USERS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(
                f"Error: {USERS_PATH} contains invalid JSON: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    def _load_teams(self):
        if not TEAMS_PATH.exists():
            print(
                f"Error: {TEAMS_PATH} not found.\n\n{TEAMS_EXAMPLE}",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            return json.loads(TEAMS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(
                f"Error: {TEAMS_PATH} contains invalid JSON: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    def _save_users(self):
        USERS_PATH.write_text(json.dumps(self._users, indent=2), encoding="utf-8")

    def get_account_id(self, email):
        if email in self._users:
            return self._users[email]

        users = self._jira.search_users(
            query=email, includeActive=True, includeInactive=False
        )

        if len(users) > 1:
            exact = [u for u in users if getattr(u, "emailAddress", None) == email]
            if len(exact) == 1:
                users = exact

        if len(users) != 1:
            found = [
                f"{u.displayName} ({getattr(u, 'accountId', 'no-id')})" for u in users
            ]
            raise ValueError(
                f"Expected exactly one user for '{email}', found {len(users)}: {found}"
            )

        account_id = users[0].accountId
        self._users[email] = account_id
        self._save_users()
        return account_id

    def get_team_emails(self, team_key):
        if team_key not in self._teams:
            raise ValueError(
                f"Team '{team_key}' not found in {TEAMS_PATH}. "
                f"Available teams: {list(self._teams.keys())}"
            )
        return self._teams[team_key]

    def get_team_ids(self, team_key):
        return [self.get_account_id(email) for email in self.get_team_emails(team_key)]

    def get_all_team_emails(self):
        all_emails = set()
        for emails in self._teams.values():
            all_emails.update(emails)
        return sorted(all_emails)
