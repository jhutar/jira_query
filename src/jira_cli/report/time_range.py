import datetime
import re


def parse_range(range_str, today=None):
    """Parse time range string into (start_date, end_date) as date objects.

    Formats:
        Nd - last N days (rolling). end = today.
        Nw - last N weeks (N*7 days, rolling). end = today.
        Nm - last N calendar months (aligned to month boundaries).
             e.g. 1m on July 14 -> June 1..June 30
    """
    if today is None:
        today = datetime.date.today()

    match = re.fullmatch(r"(\d+)([dwm])", range_str)
    if not match:
        raise ValueError(
            f"Invalid range format '{range_str}'. Use Nd, Nw, or Nm (e.g. 7d, 2w, 3m)"
        )

    count = int(match.group(1))
    unit = match.group(2)

    if count < 1:
        raise ValueError("Range count must be at least 1")

    if unit == "d":
        end_date = today
        start_date = today - datetime.timedelta(days=count)
        return start_date, end_date

    if unit == "w":
        end_date = today
        start_date = today - datetime.timedelta(weeks=count)
        return start_date, end_date

    # unit == "m": calendar month boundaries
    # End = last day of previous month
    first_of_this_month = today.replace(day=1)
    end_date = first_of_this_month - datetime.timedelta(days=1)

    # Start = first day of (count) months before end's month
    start_month = end_date.month - count + 1
    start_year = end_date.year
    while start_month < 1:
        start_month += 12
        start_year -= 1
    start_date = datetime.date(start_year, start_month, 1)

    return start_date, end_date


def parse_explicit_dates(start_str, end_str):
    """Parse YYYY-MM-DD date strings, validate start <= end."""
    start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
    if start_date > end_date:
        raise ValueError(
            f"Start date {start_str} is after end date {end_str}"
        )
    return start_date, end_date


def format_jql_date(d):
    """Format date as YYYY-MM-DD string for JQL."""
    return d.strftime("%Y-%m-%d")
