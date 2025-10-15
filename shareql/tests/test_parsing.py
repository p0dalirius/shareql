#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : test_rules_directory.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

import os
import unittest

from lark import Token, Tree

from shareql.ast.rule import Rule
from shareql.grammar.parser import RuleParser


class TestRulesDirectory(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_parsing_of_deny_directory_exploration_if_directory_name_matches_admin(
        self,
    ):
        rule = 'DENY EXPLORATION IF DIRECTORY.NAME MATCHES "admin"'

        rules, errors = self.parser.parse(rule)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")

        self.assertIsInstance(rules[0], Rule, "Rule should be a Rule")
        self.assertEqual(rules[0].action, "DENY")
        self.assertEqual(rules[0].operation, "EXPLORATION")
        self.assertEqual(rules[0].condition.field, "DIRECTORY.NAME")
        self.assertEqual(rules[0].condition.operator, "MATCHES")
        self.assertEqual(
            rules[0].condition.value, Tree(Token("RULE", "value"), ["admin"])
        )

    def test_parsing_of_allow_directory_exploration_if_directory_name_matches_admin(
        self,
    ):
        rule = 'ALLOW EXPLORATION IF DIRECTORY.NAME MATCHES "admin"'

        rules, errors = self.parser.parse(rule)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")

        self.assertIsInstance(rules[0], Rule, "Rule should be a Rule")
        self.assertEqual(rules[0].action, "ALLOW")
        self.assertEqual(rules[0].operation, "EXPLORATION")
        self.assertEqual(rules[0].condition.field, "DIRECTORY.NAME")
        self.assertEqual(rules[0].condition.operator, "MATCHES")
        self.assertEqual(
            rules[0].condition.value, Tree(Token("RULE", "value"), ["admin"])
        )

    def test_parsing_of_deny_directory_processing_if_directory_name_matches_admin(
        self,
    ):
        rule = 'DENY PROCESSING IF DIRECTORY.NAME MATCHES "admin"'

        rules, errors = self.parser.parse(rule)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")

        self.assertIsInstance(rules[0], Rule, "Rule should be a Rule")
        self.assertEqual(rules[0].action, "DENY")
        self.assertEqual(rules[0].operation, "PROCESSING")
        self.assertEqual(rules[0].condition.field, "DIRECTORY.NAME")
        self.assertEqual(rules[0].condition.operator, "MATCHES")
        self.assertEqual(
            rules[0].condition.value, Tree(Token("RULE", "value"), ["admin"])
        )

    def test_parsing_of_allow_directory_processing_if_directory_name_matches_admin(
        self,
    ):
        rule = 'ALLOW PROCESSING IF DIRECTORY.NAME MATCHES "admin"'

        rules, errors = self.parser.parse(rule)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")

        self.assertIsInstance(rules[0], Rule, "Rule should be a Rule")
        self.assertEqual(rules[0].action, "ALLOW")
        self.assertEqual(rules[0].operation, "PROCESSING")
        self.assertEqual(rules[0].condition.field, "DIRECTORY.NAME")
        self.assertEqual(rules[0].condition.operator, "MATCHES")
        self.assertEqual(
            rules[0].condition.value, Tree(Token("RULE", "value"), ["admin"])
        )

    def test_parsing_of_example_rules(self):
        """Test parsing the example rules file."""
        example_rules_path = os.path.join(
            os.path.dirname(__file__), "..", "examples", "example_rules.txt"
        )

        with open(example_rules_path, "r") as f:
            text = f.read().strip()

        rules, errors = self.parser.parse(text)

        # Should have no parsing errors
        if len(errors) > 0:
            print()
            for errorlist in errors:
                print(errorlist)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")

        # Should have parsed some rules
        self.assertGreater(len(rules), 0, "No rules were parsed")

        # Verify all rules are valid objects
        for rule in rules:
            self.assertIsNotNone(rule, "Rule should not be None")


if __name__ == "__main__":
    unittest.main()
