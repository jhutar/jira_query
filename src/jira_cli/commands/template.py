#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def add_arguments(subparsers):
    subparsers.add_parser(
        "template",
        help="Work with issue templates",
    )


def run(ctx, args):
    for name, data in ctx.config["issue_templates"].items():
        print(f"Template {name}")
        for k, v in data.items():
            if type(v) is list:
                v = ", ".join(v)
            print(f"  {k}: {v}")
