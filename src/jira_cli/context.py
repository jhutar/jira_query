#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import jira as jira_lib
import yaml


class JiraQueryError(Exception):
    pass


@dataclass
class Context:
    config: Dict[str, Any]
    jira: jira_lib.JIRA
    logger: logging.Logger


def get_default_config_path() -> str:
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return os.path.join(xdg_config_home, "jira-cli", "config.yaml")
    return os.path.expanduser("~/.config/jira-cli/config.yaml")


def load_config(config_path) -> Dict[str, Any]:
    config_path = Path(config_path).expanduser()

    if not config_path.is_file():
        raise JiraQueryError(
            f"Configuration file not found at '{config_path}'.\n"
            "Please run 'jira-cli setup' to create a new configuration."
        )

    try:
        with open(config_path, "r", encoding="utf-8") as fd:
            config_data = yaml.safe_load(fd)
    except Exception as e:
        raise JiraQueryError(
            f"Error reading configuration file at '{config_path}': {e}"
        ) from e

    assert isinstance(config_data, dict)
    assert "server" in config_data
    assert "url" in config_data["server"]
    assert "auth" in config_data["server"]
    assert "basic_auth" in config_data["server"]["auth"]
    assert "username" in config_data["server"]["auth"]["basic_auth"]
    assert "token" in config_data["server"]["auth"]["basic_auth"]
    return config_data


def load_server_config(config_path) -> Dict[str, Any]:
    return load_config(config_path)["server"]


def _create_jira_client(url, username, token):
    options = {
        "server": url,
        "rest_api_version": "3",
    }
    return jira_lib.JIRA(
        options=options,
        basic_auth=(username, token),
    )


def create_context(args) -> Context:
    logger = logging.getLogger("jira_cli")
    config = load_config(args.config)
    auth = config["server"]["auth"]["basic_auth"]
    jira_client = _create_jira_client(
        config["server"]["url"], auth["username"], auth["token"]
    )
    return Context(config=config, jira=jira_client, logger=logger)
