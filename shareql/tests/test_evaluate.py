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


class TestEvaluate(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_evaluate_of_deny_directory_exploration_if_directory_name_matches_admin(
        self,
    ):
        ruletext = 'DENY EXPLORATION IF DIRECTORY.NAME MATCHES "admin"'
        for directory_name, expected_allowed, expected_result in [
            ("admin", False, RulesEvaluationResult.MATCH),
            ("ADMIN", True, RulesEvaluationResult.NO_MATCH),
        ]:
            rules, errors = RuleParser().parse(ruletext)
            self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
            self.assertEqual(len(rules), 1, "Expected exactly one rule")

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
            re.context.set_depth(0)

            allowed_explore = re.can_explore(
                RuleObjectDirectory(
                    name=directory_name,
                    path="\\192.168.1.1\\Share",
                    modified_at=datetime.now(),
                    created_at=datetime.now(),
                )
            )

            self.assertEqual(
                allowed_explore,
                expected_allowed,
                f"Allowed: {allowed_explore}, Expected: {expected_allowed}",
            )


if __name__ == "__main__":
    unittest.main()
