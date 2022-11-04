#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os

import jinja2

import jira

import yaml


def list_issues(my_jira, jql):
    return my_jira.search_issues(jql, maxResults=False)


def main():
    parser = argparse.ArgumentParser(
        description="Query Jira",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        default="~/.jira_query.yaml",
        help="Config file",
    )
    parser.add_argument(
        "--template",
        default="templates/default.md.j2",
        help="Jinja2 template",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Show debug output",
    )
    parser.add_argument(
        "query",
        help="Jira query",
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Argumets are %s" % args)

    args.config = os.path.expanduser(args.config)
    with open(args.config, "r") as fd:
        my_config = yaml.load(fd, Loader=yaml.Loader)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(args.template))
    )
    template = env.get_template(os.path.basename(args.template))

    my_jira = jira.JIRA(
        my_config["server"]["url"],
        token_auth=my_config["server"]["auth"]["token_auth"],
    )

    issues = list_issues(my_jira, args.query)

    logging.debug(dir(issues[0]))
    logging.debug(dir(issues[0].fields))
    logging.debug(dir(issues[0].fields.assignee))
    logging.debug(dir(issues[0].fields.status))

    print(template.render({"issues": issues}))


if __name__ == "__main__":
    main()
