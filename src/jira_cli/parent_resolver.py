#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def resolve_parent_field(config, issue_type_name, parent_key):
    """Return (field_name, value) for parent linking based on config and issue type."""
    custom_fields = config.get("custom_fields", {})
    if "parent_link" in custom_fields:
        if issue_type_name in ("Task", "Bug", "Story"):
            return custom_fields["epic"], parent_key
        elif issue_type_name == "Epic":
            return custom_fields["parent_link"], parent_key
    return "parent", {"key": parent_key}
