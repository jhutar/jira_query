import datetime

import pytest

from jira_cli.report.time_range import (
    format_jql_date,
    parse_explicit_dates,
    parse_range,
)

JULY_14 = datetime.date(2026, 7, 14)


class TestParseRangeDays:
    def test_7d(self):
        start, end = parse_range("7d", today=JULY_14)
        assert start == datetime.date(2026, 7, 7)
        assert end == JULY_14

    def test_30d(self):
        start, end = parse_range("30d", today=JULY_14)
        assert start == datetime.date(2026, 6, 14)
        assert end == JULY_14

    def test_1d(self):
        start, end = parse_range("1d", today=JULY_14)
        assert start == datetime.date(2026, 7, 13)
        assert end == JULY_14


class TestParseRangeWeeks:
    def test_1w(self):
        start, end = parse_range("1w", today=JULY_14)
        assert start == datetime.date(2026, 7, 7)
        assert end == JULY_14

    def test_2w(self):
        start, end = parse_range("2w", today=JULY_14)
        assert start == datetime.date(2026, 6, 30)
        assert end == JULY_14


class TestParseRangeMonths:
    def test_1m(self):
        start, end = parse_range("1m", today=JULY_14)
        assert start == datetime.date(2026, 6, 1)
        assert end == datetime.date(2026, 6, 30)

    def test_3m(self):
        start, end = parse_range("3m", today=JULY_14)
        assert start == datetime.date(2026, 4, 1)
        assert end == datetime.date(2026, 6, 30)

    def test_6m(self):
        start, end = parse_range("6m", today=JULY_14)
        assert start == datetime.date(2026, 1, 1)
        assert end == datetime.date(2026, 6, 30)

    def test_year_boundary(self):
        jan_15 = datetime.date(2026, 1, 15)
        start, end = parse_range("1m", today=jan_15)
        assert start == datetime.date(2025, 12, 1)
        assert end == datetime.date(2025, 12, 31)

    def test_3m_across_year(self):
        feb_10 = datetime.date(2026, 2, 10)
        start, end = parse_range("3m", today=feb_10)
        assert start == datetime.date(2025, 11, 1)
        assert end == datetime.date(2026, 1, 31)

    def test_12m(self):
        start, end = parse_range("12m", today=JULY_14)
        assert start == datetime.date(2025, 7, 1)
        assert end == datetime.date(2026, 6, 30)


class TestParseRangeInvalid:
    def test_bad_format(self):
        with pytest.raises(ValueError, match="Invalid range format"):
            parse_range("abc")

    def test_no_unit(self):
        with pytest.raises(ValueError, match="Invalid range format"):
            parse_range("7")

    def test_zero(self):
        with pytest.raises(ValueError, match="at least 1"):
            parse_range("0d")


class TestParseExplicitDates:
    def test_valid(self):
        start, end = parse_explicit_dates("2026-01-01", "2026-06-30")
        assert start == datetime.date(2026, 1, 1)
        assert end == datetime.date(2026, 6, 30)

    def test_same_day(self):
        start, end = parse_explicit_dates("2026-07-14", "2026-07-14")
        assert start == end

    def test_inverted(self):
        with pytest.raises(ValueError, match="after"):
            parse_explicit_dates("2026-07-14", "2026-01-01")

    def test_bad_format(self):
        with pytest.raises(ValueError):
            parse_explicit_dates("14-07-2026", "2026-07-14")


class TestFormatJqlDate:
    def test_format(self):
        assert format_jql_date(datetime.date(2026, 7, 14)) == "2026-07-14"

    def test_zero_padded(self):
        assert format_jql_date(datetime.date(2026, 1, 5)) == "2026-01-05"
