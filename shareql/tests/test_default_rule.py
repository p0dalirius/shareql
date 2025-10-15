#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : test_default_rule.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

import unittest

from shareql.evaluate.evaluator import RulesEvaluationResult, RulesEvaluator
from shareql.grammar.parser import RuleParser
from shareql.objects.directory import RuleObjectDirectory
from shareql.objects.file import RuleObjectFile


class TestDefaultRule(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_default_allow_when_no_rules_match(self):
        """Test that DEFAULT: ALLOW works when no rules match."""
        ruletext = "DEFAULT: ALLOW"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")
        self.assertEqual(rules[0].operation, "DEFAULT")
        self.assertEqual(rules[0].action, "ALLOW")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match any rules
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="test.txt",
                path="/some/path/test.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "DEFAULT")
        self.assertEqual(rule.action, "ALLOW")
        self.assertTrue(allowed)
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_default_deny_when_no_rules_match(self):
        """Test that DEFAULT: DENY works when no rules match."""
        ruletext = "DEFAULT: DENY"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")
        self.assertEqual(rules[0].operation, "DEFAULT")
        self.assertEqual(rules[0].action, "DENY")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match any rules
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="test.txt",
                path="/some/path/test.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "DEFAULT")
        self.assertEqual(rule.action, "DENY")
        self.assertFalse(allowed)
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_default_allow_with_specific_rules(self):
        """Test that DEFAULT: ALLOW works with specific rules that don't match."""
        ruletext = """DENY PROCESSING IF FILE.NAME MATCHES "blocked.txt"
DEFAULT: ALLOW"""
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 2, "Expected exactly two rules")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match the DENY rule
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="allowed.txt",
                path="/some/path/allowed.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "DEFAULT")
        self.assertEqual(rule.action, "ALLOW")
        self.assertTrue(allowed)
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_default_deny_with_specific_rules(self):
        """Test that DEFAULT: DENY works with specific rules that don't match."""
        ruletext = """ALLOW PROCESSING IF FILE.NAME MATCHES "allowed.txt"
DEFAULT: DENY"""
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 2, "Expected exactly two rules")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match the ALLOW rule
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="blocked.txt",
                path="/some/path/blocked.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "DEFAULT")
        self.assertEqual(rule.action, "DENY")
        self.assertFalse(allowed)
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_specific_rule_overrides_default(self):
        """Test that specific rules override the default rule."""
        ruletext = """DENY PROCESSING IF FILE.NAME MATCHES "blocked.txt"
DEFAULT: ALLOW"""
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")

        re = RulesEvaluator(rules=rules)

        # Test with a file that matches the DENY rule
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="blocked.txt",
                path="/some/path/blocked.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "PROCESSING")
        self.assertEqual(rule.action, "DENY")
        self.assertFalse(allowed)
        self.assertEqual(result, RulesEvaluationResult.MATCH)

    def test_multiple_default_rules_last_wins(self):
        """Test that when multiple DEFAULT rules exist, the last one wins."""
        ruletext = """DEFAULT: ALLOW
DEFAULT: DENY"""
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 2, "Expected exactly two rules")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match any rules
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="test.txt",
                path="/some/path/test.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNotNone(rule)
        self.assertEqual(rule.operation, "DEFAULT")
        self.assertEqual(rule.action, "DENY")  # Last DEFAULT rule should win
        self.assertFalse(allowed)
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_no_default_rule_defaults_to_allow(self):
        """Test that when no DEFAULT rule is specified, it defaults to ALLOW."""
        ruletext = 'DENY PROCESSING IF FILE.NAME MATCHES "blocked.txt"'
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")

        re = RulesEvaluator(rules=rules)

        # Test with a file that doesn't match the DENY rule
        rule, allowed, result = re.evaluate(
            RuleObjectFile(
                name="allowed.txt",
                path="/some/path/allowed.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )

        self.assertIsNone(rule)  # No rule matched
        self.assertTrue(allowed)  # Default to ALLOW
        self.assertEqual(result, RulesEvaluationResult.NO_MATCH)

    def test_can_explore_with_default_rule(self):
        """Test that can_explore works with DEFAULT rules."""
        ruletext = "DEFAULT: ALLOW"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")

        re = RulesEvaluator(rules=rules)

        # Test exploration with DEFAULT: ALLOW
        can_explore = re.can_explore(
            RuleObjectDirectory(
                name="test_dir",
                path="/some/path/test_dir",
                modified_at=None,
                created_at=None,
            )
        )
        self.assertTrue(can_explore)

    def test_can_process_with_default_rule(self):
        """Test that can_process works with DEFAULT rules."""
        ruletext = "DEFAULT: DENY"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")

        re = RulesEvaluator(rules=rules)

        # Test processing with DEFAULT: DENY
        can_process = re.can_process(
            RuleObjectFile(
                name="test.txt",
                path="/some/path/test.txt",
                size=100,
                modified_at=None,
                created_at=None,
            )
        )
        self.assertFalse(can_process)


if __name__ == "__main__":
    unittest.main()
