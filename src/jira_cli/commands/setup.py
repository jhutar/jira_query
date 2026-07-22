#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pathlib import Path
import yaml


def add_arguments(subparsers):
    subparsers.add_parser(
        "setup",
        help="Interactive setup wizard to configure jira-cli",
    )


def run(ctx, args):
    config_path = Path(args.config).expanduser()

    print("Welcome to the jira-cli setup wizard!")
    print("This wizard will help you configure your Jira CLI client.")
    print(f"The configuration will be written to: {config_path}")
    print()

    # 1) Wizard prompts
    url = input("What is your Jira instance? [https://redhat.atlassian.net/]: ").strip()
    if not url:
        url = "https://redhat.atlassian.net/"

    username = input("What is your username? ").strip()
    token = input("What is your Jira token? ").strip()

    print("\nUsing default settings for 'boards_list', 'project_defaults', 'custom_fields', and 'sprint_regexps'.")

    # 2) Construct config dictionary
    config_data = {
        "server": {
            "url": url,
            "auth": {
                "basic_auth": {
                    "token": token,
                    "username": username
                }
            }
        },
        "boards_list": [
            "Konflux/RHTAP Perf&Scale board",
            "Pipelines Perf&Scale board",
            "Perf&Scale Infra tasks",
            "HCE Perf sprint board",
            "Satellite Perf&Scale scrum board"
        ],
        "issue_templates": {},
        "project_defaults": {
            "KONFLUX": {
                "type": "Task",
                "security": "Red Hat Employee",
                "components": ["Performance"]
            },
            "SAT": {
                "type": "Task",
                "security": "Red Hat Employee",
                "components": ["Performance"]
            },
            "SRVKP": {
                "type": "Task",
                "security": "Red Hat Employee",
                "components": ["Performance"]
            },
            "HCEPERF": {
                "type": "Task",
                "security": "Red Hat Employee"
            }
        },
        "custom_fields": {
            "epic": "customfield_10014",
            "epic_name": "customfield_10011",
            "story_points": "customfield_10028",
            "sprint": "customfield_10020",
            "target_start": "customfield_10015",
            "target_end": "customfield_10701"
        },
        "sprint_regexps": {
            "KONFLUX": "Konflux perf&scale sprint [0-9]+",
            "HCEPERF": "HCE Sprint [0-9]+",
            "SRVKP": "Pipelines perf&scale sprint [0-9]+",
            "SAT": "Satellite Perf&Scale Sprint [0-9]+"
        }
    }

    # 3) Ensure parent directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # 4) Write configuration file
    with open(config_path, "w", encoding="utf-8") as fd:
        yaml.safe_dump(config_data, fd, default_flow_style=False, sort_keys=False)

    print(f"\nConfiguration successfully written to '{config_path}'!")
