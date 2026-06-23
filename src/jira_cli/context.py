#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
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


def load_config(config_path) -> Dict[str, Any]:
    config_path = Path(config_path).expanduser()

    with open(config_path, "r", encoding="utf-8") as fd:
        config_data = yaml.safe_load(fd)
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
