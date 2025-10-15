#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : test_rules_directory.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

import unittest
from datetime import datetime

from shareql.evaluate.evaluator import RulesEvaluationResult, RulesEvaluator
from shareql.grammar.parser import RuleParser
from shareql.objects.directory import RuleObjectDirectory
from shareql.objects.host import RuleObjectHost
from shareql.objects.share import RuleObjectShare


class TestCanExplore(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_can_explore_of_deny_share_exploration_of_common_shares_if_share_name_in_list(
        self,
    ):
        ruletext = "DENY EXPLORATION IF SHARE.NAME IN ['c$','print$','ipc$','admin$']\nALLOW EXPLORATION "
        for share_name, expected_allowed, expected_result in [
            ("sysvol", True, RulesEvaluationResult.MATCH),
            ("print$", False, RulesEvaluationResult.MATCH),
            ("ipc$", False, RulesEvaluationResult.MATCH),
            ("admin$", False, RulesEvaluationResult.MATCH),
            ("public", True, RulesEvaluationResult.MATCH),
        ]:
            rules, errors = RuleParser().parse(ruletext)
            self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
            self.assertEqual(len(rules), 2, "Expected exactly two rules")

            re = RulesEvaluator(rules=rules)

            re.context.set_share(
                RuleObjectShare(name=share_name, description="test", hidden=False)
            )
            re.context.set_host(RuleObjectHost(name="PC01", address="192.168.1.1"))
            re.context.set_path(
                [
                    RuleObjectDirectory(
                        name="parent",
                        path="\\192.168.1.1\\Share",
                        modified_at=datetime.now(),
                        created_at=datetime.now(),
                    )
                ]
            )
            re.context.set_depth(0)

            rule, allowed, result = re.evaluate(
                RuleObjectShare(
                    name=share_name,
                    description="test",
                    hidden=False,
                )
            )
            if rule is not None:
                self.assertEqual(
                    allowed,
                    expected_allowed,
                    f"Share {share_name} | Allowed: {allowed}, Expected: {expected_allowed}",
                )
                self.assertEqual(
                    result,
                    expected_result,
                    f"Share {share_name} | Result: {result}, Expected: {expected_result}",
                )

    def test_can_explore_of_deny_directory_exploration_of_common_shares_if_share_name_in_list(
        self,
    ):
        ruletext = "DENY EXPLORATION IF DIRECTORY.NAME IN ['notthisdirectory']\nALLOW EXPLORATION "
        for directory_name, expected_allowed, expected_result in [
            ("thisdirectory", True, RulesEvaluationResult.MATCH),
            ("notthisdirectory", False, RulesEvaluationResult.MATCH),
        ]:
            rules, errors = RuleParser().parse(ruletext)
            self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
            self.assertEqual(len(rules), 2, "Expected exactly two rules")

            re = RulesEvaluator(rules=rules)

            re.context.set_share(
                RuleObjectShare(name="Share", description="test", hidden=False)
            )
            re.context.set_host(RuleObjectHost(name="PC01", address="192.168.1.1"))
            re.context.set_path([])
            re.context.set_depth(0)

            rule, allowed, result = re.evaluate(
                RuleObjectDirectory(
                    name=directory_name,
                    path="\\192.168.1.1\\Share",
                    modified_at=datetime.now(),
                    created_at=datetime.now(),
                )
            )
            if rule is not None:
                self.assertEqual(
                    allowed,
                    expected_allowed,
                    f"Directory {directory_name} | Allowed: {allowed}, Expected: {expected_allowed}",
                )
                self.assertEqual(
                    result,
                    expected_result,
                    f"Directory {directory_name} | Result: {result}, Expected: {expected_result}",
                )


if __name__ == "__main__":
    unittest.main()
