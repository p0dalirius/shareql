#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : test_files.py
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


class TestFiles(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.parser = RuleParser()

    def test_deny_processing_if_file_name_is_in_list(
        self,
    ):
        ruletext = "ALLOW PROCESSING IF FILE.NAME IN ['migration.xml']\n"
        ruletext += "DENY EXPLORATION IF DEPTH > 1\n"
        ruletext += "ALLOW EXPLORATION\n"
        ruletext += "DENY PROCESSING\n"
        for file_name, expected_allowed, expected_result in [
            ("migration.xml", True, RulesEvaluationResult.MATCH),
            ("backup.exe", False, RulesEvaluationResult.MATCH),
            ("temp.dll", False, RulesEvaluationResult.MATCH),
            ("file.txt", False, RulesEvaluationResult.MATCH),
        ]:
            rules, errors = RuleParser().parse(ruletext)
            self.assertEqual(len(errors), 0, f"Parsing errors found: {errors}")
            self.assertEqual(len(rules), 4, "Expected exactly three rules")

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

            allowed_process = re.can_process(
                RuleObjectFile(
                    name=file_name,
                    path="\\192.168.1.1\\Share\\{file_name}",
                    size=1024,
                    modified_at=datetime.now(),
                    created_at=datetime.now(),
                )
            )
            self.assertEqual(
                allowed_process,
                expected_allowed,
                f"File name {file_name} | Allowed: {allowed_process}, Expected: {expected_allowed}",
            )

            # rule, allowed, result = re.evaluate(
            #     RuleObjectFile(
            #         name=file_name,
            #         path="\\192.168.1.1\\Share\\{file_name}",
            #         size=1024,
            #         modified_at=datetime.now(),
            #         created_at=datetime.now(),
            #     )
            # )

            # if rule is not None:
            #     self.assertEqual(
            #         allowed,
            #         expected_allowed,
            #         f"File name {file_name} | Allowed: {allowed}, Expected: {expected_allowed}, by rule {rule.id}",
            #     )
            #     self.assertEqual(
            #         result,
            #         expected_result,
            #         f"File name {file_name} | Result: {result}, Expected: {expected_result}, by rule {rule.id}",
            #     )


if __name__ == "__main__":
    unittest.main()
