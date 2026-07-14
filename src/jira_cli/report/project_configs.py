PROJECT_CONFIGS = {
    "Konflux": {
        "base_jql": "project in (KONFLUX, KFLUXINFRA, KFLUXBUGS) AND component = Performance",
        "review_statuses": ["Review", "Code Review"],
        "team": "KONFLUX",
    },
    "Pipelines": {
        "base_jql": "project = SRVKP AND component = Performance",
        "review_statuses": ["Review", "Code Review"],
        "team": "PIPELINES",
    },
    "ConsoleDot": {
        "base_jql": "project = HCEPERF",
        "review_statuses": ["Review", "Release Pending"],
        "team": "HCEPERF",
    },
    "Satellite": {
        "base_jql": (
            "((project in (SAT) AND (component = Performance OR labels = Performance))"
            " OR (project in (HCEPERF) AND component in"
            " ('RHIN - Image Builder', 'RHIN - Provisioning',"
            " 'RHIN - Pulp', 'RHIN - Repositories')))"
        ),
        "review_statuses": ["Review"],
        "team": "SAT",
    },
}

CATEGORY_TITLES = {
    "completed": "Finished issues",
    "in-review": "In review issues",
    "active": "In progress issues",
    "incoming": "New issues",
    "stale": "Stale issues",
}

ALL_CATEGORIES = list(CATEGORY_TITLES.keys())
