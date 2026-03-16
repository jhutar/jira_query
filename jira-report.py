#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import logging
import sys
import csv
from pathlib import Path
from typing import Any, Dict
import yaml
import jira

# Configuration
DEFAULT_CONFIG_PATH = "~/.jira_query.yaml"


def setup_logging(stderr_level):
    """
    Configures logging to file and stderr.

    Args:
        stderr_level (int): The logging level for stderr output.
    """
    logger = logging.getLogger("jira_report")
    logger.setLevel(logging.DEBUG)

    urllib_logger = logging.getLogger("urllib3.connectionpool")
    urllib_logger.setLevel(stderr_level)

    file_handler = logging.FileHandler("/tmp/jira-report.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(threadName)s %(levelname)s %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(stderr_level)
    stderr_formatter = logging.Formatter(
        "%(asctime)s %(name)s %(threadName)s %(levelname)s %(message)s"
    )
    stderr_handler.setFormatter(stderr_formatter)
    logger.addHandler(stderr_handler)

    return logger


def _load_config(config_path) -> Dict[str, Any]:
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


def _create_jira_client(url, username, token):
    options = {"server": url}
    return jira.JIRA(
        options=options,
        basic_auth=(username, token),
    )


class Doer:
    """Do all the work with Jira to generate the report."""
    def __init__(self, args):
        self._logger = logging.getLogger("jira_report.Doer")

        self._args = args
        self._config = _load_config(self._args.config)
        auth = self._config["server"]["auth"]["basic_auth"]
        self._jira = _create_jira_client(
            self._config["server"]["url"], auth["username"], auth["token"]
        )

    def execute(self):
        assignees = [a.strip() for a in self._args.assignees.split(",")]
        start_date = self._args.start
        end_date = self._args.end

        # Ensure start_date <= end_date
        if start_date > end_date:
            raise ValueError("Start date must be before or equal to end date.")

        assignees_jql = ", ".join([f'"{a}"' for a in assignees])
        # Build JQL to find closed issues in the given time range for the specified assignees.
        # Note: we add ' 23:59' to the end date to include the entire last day.
        jql = f'assignee in ({assignees_jql}) AND resolved >= "{start_date.strftime("%Y-%m-%d")}" AND resolved <= "{end_date.strftime("%Y-%m-%d")} 23:59"'

        self._logger.debug(f"Searching issues using JQL: {jql}")
        issues = self._jira.search_issues(jql, maxResults=False)
        self._logger.debug(f"JQL search returned {len(issues)} issues.")
        self._logger.info(f"Found {len(issues)} closed issues matching the criteria.")

        # Data structure to hold points by assignee and by date
        # points_by_assignee_date[assignee][date] = sum_of_story_points
        points_by_assignee_date = {a: {} for a in assignees}

        for issue in issues:
            # We assume the user who finished the issue is the current assignee
            assignee = issue.fields.assignee.name if issue.fields.assignee else None
            
            # If for some reason the assignee is not in our list, skip
            if assignee not in assignees:
                continue

            resolution_date_str = issue.fields.resolutiondate
            if not resolution_date_str:
                self._logger.warning(f"Issue {issue.key} is returned as resolved but has no resolutiondate.")
                continue

            # Extract just the date part (first 10 characters: YYYY-MM-DD)
            res_date = datetime.datetime.strptime(resolution_date_str[:10], "%Y-%m-%d").date()

            # Retrieve story points using the custom field ID
            sp_value = getattr(issue.fields, "customfield_12310243", 0)
            if sp_value is None:
                sp_value = 0
            
            try:
                sp_value = float(sp_value)
            except ValueError:
                self._logger.warning(f"Could not parse story points for {issue.key}: {sp_value}")
                sp_value = 0

            self._logger.debug(
                f"Counted Issue: {issue.key} | Date: {res_date} | Assignee: {assignee} | "
                f"Story Points: {sp_value} | Link: {issue.permalink()}"
            )

            # Add to the day's sum
            points_by_assignee_date[assignee][res_date] = points_by_assignee_date[assignee].get(res_date, 0) + sp_value

        # Generate the CSV output
        output_path = self._args.output
        self._logger.debug(f"Writing CSV report to {output_path}")

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            header = ["Date"] + assignees
            writer.writerow(header)
            
            current_date = start_date
            cumulative_points = {a: 0.0 for a in assignees}
            
            # Iterate through every day in the time range
            while current_date <= end_date:
                row = [current_date.strftime("%Y-%m-%d")]
                for a in assignees:
                    points_today = points_by_assignee_date[a].get(current_date, 0.0)
                    cumulative_points[a] += points_today
                    row.append(cumulative_points[a])
                writer.writerow(row)
                current_date += datetime.timedelta(days=1)

        print(f"Successfully generated report at: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CSV report of cumulative story points per associate over a given time range.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help="Path to the configuration file",
        type=str,
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable info level logging output",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug level logging output",
    )
    parser.add_argument(
        "--assignees",
        required=True,
        help="Comma separated list of Jira user names (e.g., 'jhutar-1,jane_doe')",
        type=str,
    )
    parser.add_argument(
        "--start",
        required=True,
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
        help="Start date for the report in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end",
        required=True,
        type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
        help="End date for the report in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="report.csv",
        help="Path to the output CSV file",
        type=str,
    )

    args = parser.parse_args()

    if args.debug:
        logger = setup_logging(logging.DEBUG)
    elif args.verbose:
        logger = setup_logging(logging.INFO)
    else:
        logger = setup_logging(logging.WARNING)

    logger.debug(f"Arguments are {args}")

    doer = Doer(args)
    try:
        doer.execute()
    except Exception as e:
        logger.error(f"Error executing report generation: {e}", exc_info=args.debug)
        sys.exit(1)


if __name__ == "__main__":
    main()
