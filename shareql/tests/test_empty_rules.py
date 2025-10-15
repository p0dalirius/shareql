#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : test_empty_rules.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

import unittest
from datetime import datetime

from shareql.evaluate.evaluator import RulesEvaluationResult, RulesEvaluator
from shareql.grammar.parser import RuleParser
from shareql.objects.directory import RuleObjectDirectory
from shareql.objects.file import RuleObjectFile
from shareql.objects.host import RuleObjectHost
from shareql.objects.share import RuleObjectShare


class TestEmptyRules(unittest.TestCase):
    """
    Test cases for empty rules scenarios.

    These tests verify the default behavior when no rules are set:
    - If no rules at all: default to ALLOW
    - If DEFAULT ALLOW is set: ALLOW
    - If DEFAULT DENY is set: DENY
    """

    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_empty_rules_no_default_should_allow(self):
        """
        Test Case 1: Empty rules (no rules at all) - should default to ALLOW.

        When no rules are provided at all, both EXPLORATION and PROCESSING
        should default to ALLOW behavior.
        """
        # Create evaluator with empty rules list
        re = RulesEvaluator(rules=[])

        # Set up context
        re.context.set_share(
            RuleObjectShare(name="TestShare", description="Test share", hidden=False)
        )
        re.context.set_host(RuleObjectHost(name="TestHost", address="192.168.1.100"))
        re.context.set_depth(0)
        re.context.set_path([])

        # Test file object
        test_file = RuleObjectFile(
            name="test.txt",
            path="\\TestHost\\TestShare\\test.txt",
            size=1024,
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test directory object
        test_directory = RuleObjectDirectory(
            name="test_dir",
            path="\\TestHost\\TestShare\\test_dir",
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test share object
        test_share = RuleObjectShare(
            name="TestShare", description="Test share for exploration", hidden=False
        )

        # Test evaluation results
        rule, allowed, result = re.evaluate(test_file)

        # Should return None rule, True allowed, NO_MATCH result
        self.assertIsNone(rule, "No rules should match")
        self.assertTrue(allowed, "Should default to ALLOW when no rules")
        self.assertEqual(
            result, RulesEvaluationResult.NO_MATCH, "Should be NO_MATCH when no rules"
        )

        # Test can_process method
        can_process = re.can_process(test_file)
        self.assertTrue(can_process, "can_process should return True when no rules")

        # Test can_explore method with directory
        can_explore_dir = re.can_explore(test_directory)
        self.assertTrue(
            can_explore_dir,
            "can_explore should return True for directory when no rules",
        )

        # Test can_explore method with share
        can_explore_share = re.can_explore(test_share)
        self.assertTrue(
            can_explore_share, "can_explore should return True for share when no rules"
        )

    def test_empty_rules_with_default_allow_should_allow(self):
        """
        Test Case 2: Empty rules with DEFAULT ALLOW - should ALLOW.

        When only a DEFAULT ALLOW rule is provided, both EXPLORATION and PROCESSING
        should be ALLOWED.
        """
        # Parse DEFAULT ALLOW rule
        ruletext = "DEFAULT: ALLOW"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")
        self.assertEqual(rules[0].operation, "DEFAULT")
        self.assertEqual(rules[0].action, "ALLOW")

        # Create evaluator with DEFAULT ALLOW rule
        re = RulesEvaluator(rules=rules)

        # Set up context
        re.context.set_share(
            RuleObjectShare(name="TestShare", description="Test share", hidden=False)
        )
        re.context.set_host(RuleObjectHost(name="TestHost", address="192.168.1.100"))
        re.context.set_depth(0)
        re.context.set_path([])

        # Test file object
        test_file = RuleObjectFile(
            name="test.txt",
            path="\\TestHost\\TestShare\\test.txt",
            size=1024,
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test directory object
        test_directory = RuleObjectDirectory(
            name="test_dir",
            path="\\TestHost\\TestShare\\test_dir",
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test share object
        test_share = RuleObjectShare(
            name="TestShare", description="Test share for exploration", hidden=False
        )

        # Test evaluation results
        rule, allowed, result = re.evaluate(test_file)

        # Should return DEFAULT rule, True allowed, NO_MATCH result
        self.assertIsNotNone(rule, "DEFAULT rule should be returned")
        self.assertEqual(rule.operation, "DEFAULT", "Should be DEFAULT rule")
        self.assertEqual(rule.action, "ALLOW", "Should be ALLOW action")
        self.assertTrue(allowed, "Should be ALLOWED with DEFAULT ALLOW")
        self.assertEqual(
            result,
            RulesEvaluationResult.NO_MATCH,
            "Should be NO_MATCH for DEFAULT rule",
        )

        # Test can_process method
        can_process = re.can_process(test_file)
        self.assertTrue(
            can_process, "can_process should return True with DEFAULT ALLOW"
        )

        # Test can_explore method with directory
        can_explore_dir = re.can_explore(test_directory)
        self.assertTrue(
            can_explore_dir,
            "can_explore should return True for directory with DEFAULT ALLOW",
        )

        # Test can_explore method with share
        can_explore_share = re.can_explore(test_share)
        self.assertTrue(
            can_explore_share,
            "can_explore should return True for share with DEFAULT ALLOW",
        )

    def test_empty_rules_with_default_deny_should_deny(self):
        """
        Test Case 3: Empty rules with DEFAULT DENY - should DENY.

        When only a DEFAULT DENY rule is provided, both EXPLORATION and PROCESSING
        should be DENIED.
        """
        # Parse DEFAULT DENY rule
        ruletext = "DEFAULT: DENY"
        rules, errors = self.parser.parse(ruletext)
        self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
        self.assertEqual(len(rules), 1, "Expected exactly one rule")
        self.assertEqual(rules[0].operation, "DEFAULT")
        self.assertEqual(rules[0].action, "DENY")

        # Create evaluator with DEFAULT DENY rule
        re = RulesEvaluator(rules=rules)

        # Set up context
        re.context.set_share(
            RuleObjectShare(name="TestShare", description="Test share", hidden=False)
        )
        re.context.set_host(RuleObjectHost(name="TestHost", address="192.168.1.100"))
        re.context.set_depth(0)
        re.context.set_path([])

        # Test file object
        test_file = RuleObjectFile(
            name="test.txt",
            path="\\TestHost\\TestShare\\test.txt",
            size=1024,
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test directory object
        test_directory = RuleObjectDirectory(
            name="test_dir",
            path="\\TestHost\\TestShare\\test_dir",
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        # Test share object
        test_share = RuleObjectShare(
            name="TestShare", description="Test share for exploration", hidden=False
        )

        # Test evaluation results
        rule, allowed, result = re.evaluate(test_file)

        # Should return DEFAULT rule, False allowed, NO_MATCH result
        self.assertIsNotNone(rule, "DEFAULT rule should be returned")
        self.assertEqual(rule.operation, "DEFAULT", "Should be DEFAULT rule")
        self.assertEqual(rule.action, "DENY", "Should be DENY action")
        self.assertFalse(allowed, "Should be DENIED with DEFAULT DENY")
        self.assertEqual(
            result,
            RulesEvaluationResult.NO_MATCH,
            "Should be NO_MATCH for DEFAULT rule",
        )

        # Test can_process method
        can_process = re.can_process(test_file)
        self.assertFalse(
            can_process, "can_process should return False with DEFAULT DENY"
        )

        # Test can_explore method with directory
        can_explore_dir = re.can_explore(test_directory)
        self.assertFalse(
            can_explore_dir,
            "can_explore should return False for directory with DEFAULT DENY",
        )

        # Test can_explore method with share
        can_explore_share = re.can_explore(test_share)
        self.assertFalse(
            can_explore_share,
            "can_explore should return False for share with DEFAULT DENY",
        )

    def test_empty_rules_consistency_across_operations(self):
        """
        Additional test: Verify that empty rules behavior is consistent
        across different operations (EXPLORATION vs PROCESSING).
        """
        # Test with no rules at all
        re_no_rules = RulesEvaluator(rules=[])

        # Test with DEFAULT ALLOW
        rules_allow, _ = self.parser.parse("DEFAULT: ALLOW")
        re_default_allow = RulesEvaluator(rules=rules_allow)

        # Test with DEFAULT DENY
        rules_deny, _ = self.parser.parse("DEFAULT: DENY")
        re_default_deny = RulesEvaluator(rules=rules_deny)

        # Set up context for all evaluators
        test_file = RuleObjectFile(
            name="test.txt",
            path="\\TestHost\\TestShare\\test.txt",
            size=1024,
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        test_directory = RuleObjectDirectory(
            name="test_dir",
            path="\\TestHost\\TestShare\\test_dir",
            modified_at=datetime.now(),
            created_at=datetime.now(),
        )

        test_share = RuleObjectShare(
            name="TestShare", description="Test share for exploration", hidden=False
        )

        # Test no rules - should allow both operations
        self.assertTrue(
            re_no_rules.can_process(test_file), "No rules should allow PROCESSING"
        )
        self.assertTrue(
            re_no_rules.can_explore(test_directory),
            "No rules should allow EXPLORATION (directory)",
        )
        self.assertTrue(
            re_no_rules.can_explore(test_share),
            "No rules should allow EXPLORATION (share)",
        )

        # Test DEFAULT ALLOW - should allow both operations
        self.assertTrue(
            re_default_allow.can_process(test_file),
            "DEFAULT ALLOW should allow PROCESSING",
        )
        self.assertTrue(
            re_default_allow.can_explore(test_directory),
            "DEFAULT ALLOW should allow EXPLORATION (directory)",
        )
        self.assertTrue(
            re_default_allow.can_explore(test_share),
            "DEFAULT ALLOW should allow EXPLORATION (share)",
        )

        # Test DEFAULT DENY - should deny both operations
        self.assertFalse(
            re_default_deny.can_process(test_file),
            "DEFAULT DENY should deny PROCESSING",
        )
        self.assertFalse(
            re_default_deny.can_explore(test_directory),
            "DEFAULT DENY should deny EXPLORATION (directory)",
        )
        self.assertFalse(
            re_default_deny.can_explore(test_share),
            "DEFAULT DENY should deny EXPLORATION (share)",
        )


if __name__ == "__main__":
    unittest.main()
