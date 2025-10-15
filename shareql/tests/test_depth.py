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
from shareql.objects.file import RuleObjectFile
from shareql.objects.host import RuleObjectHost
from shareql.objects.share import RuleObjectShare


class TestDepth(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_depth_of_deny_exploration_if_depth_is_greater_than_1(
        self,
    ):
        ruletext = "DENY EXPLORATION IF DEPTH > 2\nALLOW EXPLORATION"
        for depth, expected_allowed, expected_result in [
            (0, True, RulesEvaluationResult.MATCH),
            (1, True, RulesEvaluationResult.MATCH),
            (2, True, RulesEvaluationResult.MATCH),
            (3, False, RulesEvaluationResult.MATCH),
            (4, False, RulesEvaluationResult.MATCH),
            (5, False, RulesEvaluationResult.MATCH),
        ]:
            rules, errors = RuleParser().parse(ruletext)
            self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
            self.assertEqual(len(rules), 2, "Expected exactly two rules")

            re = RulesEvaluator(rules=rules)

            re.context.set_share(
                RuleObjectShare(name="Share", description="test", hidden=False)
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
            re.context.set_depth(depth)

            rule, allowed, result = re.evaluate(
                RuleObjectFile(
                    name="file.txt",
                    path="\\192.168.1.1\\Share\\file.txt",
                    size=1024,
                    modified_at=datetime.now(),
                    created_at=datetime.now(),
                )
            )
            if rule is not None:
                self.assertEqual(
                    allowed,
                    expected_allowed,
                    f"Depth {depth} | Allowed: {allowed}, Expected: {expected_allowed}",
                )
                self.assertEqual(
                    result,
                    expected_result,
                    f"Depth {depth} | Result: {result}, Expected: {expected_result}",
                )


if __name__ == "__main__":
    unittest.main()
