#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __main__.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

import argparse

from shareql.grammar.parser import RuleParser


def parse_args():
    parser = argparse.ArgumentParser(
        description="ShareQL: A domain specific language to provide rule matching in network shares exploration"
    )

    mode_paths = parser.add_argument_group("Paths")
    mode_paths.add_argument(
        "-rf", "--rules-file", type=str, required=True, help="Path to the rules file"
    )

    mode_validate = parser.add_argument_group("Validate")
    mode_validate.add_argument(
        "-rf", "--rules-file", type=str, required=True, help="Path to the rules file"
    )

    # Adding the subparsers to the base parser
    subparsers = parser.add_subparsers(help="Mode", dest="mode", required=True)
    subparsers.add_parser(
        "paths",
        parents=[mode_paths],
        help="Apply ShareQL rules to analyze and match file paths in network shares.",
    )
    subparsers.add_parser(
        "validate",
        parents=[mode_validate],
        help="Validate ShareQL rules syntax and structure without executing them.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.rules:
        rp = RuleParser()
        rules, errors = rp.parse_file(args.rules)
        if len(errors) > 0:
            for error in errors:
                print(f"\x1b[91m{error}\x1b[0m")
        else:
            print(
                f"\x1b[92m{len(rules)} rules validated successfully from {args.rules}\x1b[0m"
            )
    else:
        print("\x1b[91mNo rules file provided\x1b[0m")
        exit(1)


if __name__ == "__main__":
    main()
