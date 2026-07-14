def _format_status_list(statuses):
    return ", ".join(f"'{s}'" for s in statuses)


def _format_team_ids(team_ids):
    return ", ".join(team_ids)


def build_completed_jql(base_jql, start, end, **kwargs):
    return (
        f'{base_jql} AND status CHANGED TO (Closed, Done)'
        f' DURING ("{start}", "{end}")'
    )


def build_in_review_jql(base_jql, start, end, review_statuses, **kwargs):
    statuses = _format_status_list(review_statuses)
    return (
        f"{base_jql} AND status in ({statuses})"
        f' AND status CHANGED TO ({statuses}) DURING ("{start}", "{end}")'
    )


def build_active_jql(base_jql, start, end, team_ids, **kwargs):
    team = _format_team_ids(team_ids)
    return (
        f"{base_jql} AND type not in (Feature, Outcome)"
        f" AND status = 'In Progress'"
        f' AND (status CHANGED TO \'In Progress\' DURING ("{start}", "{end}")'
        f" OR issuekey IN commented('{start}', '{end}', {team}))"
    )


def build_incoming_jql(base_jql, start, end, **kwargs):
    return (
        f'{base_jql} AND created >= "{start}" AND created < "{end}"'
        f" AND assignee is not EMPTY AND status not in (Closed, Done)"
    )


def build_stale_jql(base_jql, **kwargs):
    return f"{base_jql} AND status = 'In Progress'"


CATEGORY_BUILDERS = {
    "completed": build_completed_jql,
    "in-review": build_in_review_jql,
    "active": build_active_jql,
    "incoming": build_incoming_jql,
    "stale": build_stale_jql,
}
