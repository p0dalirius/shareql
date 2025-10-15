#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : evaluate.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

from typing import List

from shareql.evaluate.condition import evaluate_condition
from shareql.evaluate.context import RulesEvaluationContext
from shareql.evaluate.results import RulesEvaluationResult
from shareql.grammar.parser import Rule, RuleParser
from shareql.objects.directory import RuleObjectDirectory
from shareql.objects.file import RuleObjectFile
from shareql.objects.share import RuleObjectShare


class RulesEvaluator(object):
    """
    RulesEvaluator class.
    """

    context: RulesEvaluationContext

    def __init__(self, rules: List[Rule], DEBUG: bool = False):
        self.DEBUG = DEBUG
        self.rules = rules
        self.context = RulesEvaluationContext(depth=0, share=None, host=None, path=[])
        self.default_rule = None
        self._extract_default_rule()

    def _extract_default_rule(self):
        """
        Extract the default rule from the rules list.
        If multiple default rules exist, the last one takes precedence.
        """
        for rule in self.rules:
            if rule.operation == "DEFAULT":
                self.default_rule = rule

    def append_rule(self, rule: Rule) -> None:
        """
        Append a rule to the evaluator.
        """
        rule.id = len(self.rules) + 1
        self.rules.append(rule)
        if rule.operation == "DEFAULT":
            self.default_rule = rule

    def append_rules(self, rules: List[Rule]) -> None:
        """
        Append a list of rules to the evaluator.
        """
        for rule in rules:
            rule.id = len(self.rules) + 1
            self.rules.append(rule)
        self._extract_default_rule()

    def append_rules_from_file(self, file: str) -> None:
        """
        Append rules from a file to the evaluator.
        """
        rp = RuleParser()
        rules, errors = rp.parse(file)
        if len(rules) > 0:
            self.append_rules(rules)
        if len(errors) > 0:
            for error in errors:
                print(f"[error] {error}")

    def append_rules_from_str_list(self, rules: List[str]) -> None:
        """
        Append rules from a list of strings to the evaluator.
        """
        rp = RuleParser()
        rules, errors = rp.parse("\n".join(rules))
        if len(rules) > 0:
            self.append_rules(rules)
        if len(errors) > 0:
            for error in errors:
                print(f"[error] {error}")

    def can_explore(
        self, target_object: RuleObjectShare | RuleObjectFile | RuleObjectDirectory
    ) -> bool:
        """
        Check if the rules can evaluate the target object.

        Args:
            target_object: The target object

        Returns:
            True if the rules can explore the target object, False otherwise
        """

        rule, allowed, result = self.evaluate(target_object, "EXPLORATION")

        if rule is None:
            # No EXPLORATION rules matched, check default behavior
            if self.default_rule is not None:
                return self.default_rule.action == "ALLOW"
            else:
                # Default to ALLOW if no default rule is specified
                return True

        if rule.action.upper() == "DENY":
            return False

        # For DEFAULT rules, result is NO_MATCH but we should still allow if action is ALLOW
        if rule.operation == "DEFAULT":
            return allowed

        return allowed and result == RulesEvaluationResult.MATCH

    def can_process(
        self, target_object: RuleObjectShare | RuleObjectFile | RuleObjectDirectory
    ) -> bool:
        """
        Check if the rules can process the target object.

        Args:
            target_object: The target object

        Returns:
            True if the rules can process the target object, False otherwise
        """

        rule, allowed, result = self.evaluate(target_object, "PROCESSING")

        if rule is None:
            # No PROCESSING rules matched, check default behavior
            if self.default_rule is not None:
                return self.default_rule.action == "ALLOW"
            else:
                # Default to ALLOW if no default rule is specified
                return True

        if rule.action.upper() == "DENY":
            return False

        # For DEFAULT rules, result is NO_MATCH but we should still allow if action is ALLOW
        if rule.operation == "DEFAULT":
            return allowed

        return allowed and result == RulesEvaluationResult.MATCH

    def evaluate(
        self,
        target_object: RuleObjectShare | RuleObjectFile | RuleObjectDirectory,
        operation_filter: str = None,
    ) -> tuple[Rule, bool, RulesEvaluationResult]:
        """
        Evaluate the rules against the target object.

        Args:
            rule: The rule to evaluate
            operation_allowed: The operation allowed
            target_object: The target object
            DEBUG: Whether to print debug information

        Returns:
            The rule, operation allowed, and result
        """

        for rule in self.rules:
            # Skip DEFAULT rules during normal evaluation
            if rule.operation == "DEFAULT":
                continue

            # Filter by operation if specified
            if operation_filter is not None:
                if rule.operation != operation_filter and rule.operation is not None:
                    continue

            operation_allowed = None

            # Check the permission of the rule
            if rule.action == "ALLOW":
                operation_allowed = True
            elif rule.action == "DENY":
                operation_allowed = False
            else:
                continue

            # Check if there's a condition to evaluate
            if rule.condition is not None:
                # Create fields dictionary from the target object
                fields = {}

                if self.context is not None:
                    if self.context.share is not None:
                        # Share fields
                        fields["SHARE.NAME"] = self.context.share.name
                        fields["SHARE.DESCRIPTION"] = self.context.share.description
                        # fields["SHARE.TYPE"] = self.context.share.type

                    if self.context.host is not None:
                        # Host fields
                        fields["HOST.NAME"] = self.context.host.name
                        fields["HOST.ADDRESS"] = self.context.host.address

                    if self.context.depth is not None:
                        # General context fields
                        fields["DEPTH"] = self.context.depth

                if isinstance(target_object, RuleObjectDirectory):
                    # Directory fields
                    fields["DIRECTORY.NAME"] = getattr(target_object, "name", "")
                    fields["DIRECTORY.PATH"] = (getattr(target_object, "path", ""),)
                    fields["DIRECTORY.MODIFIED_AT"] = getattr(
                        target_object, "modified_at", ""
                    )
                    fields["DIRECTORY.CREATED_AT"] = getattr(
                        target_object, "created_at", ""
                    )

                elif isinstance(target_object, RuleObjectFile):
                    # File fields
                    fields["FILE.NAME"] = getattr(target_object, "name", "")
                    fields["FILE.PATH"] = getattr(target_object, "path", "")
                    fields["FILE.SIZE"] = getattr(target_object, "size", "")
                    fields["FILE.MODIFIED_AT"] = getattr(
                        target_object, "modified_at", ""
                    )
                    fields["FILE.CREATED_AT"] = getattr(target_object, "created_at", "")

                # Evaluate the condition
                condition_result = evaluate_condition(rule.condition, fields)

                if condition_result:
                    return rule, operation_allowed, RulesEvaluationResult.MATCH
                else:
                    # Rule doesn't match, continue to next rule
                    continue
            else:
                # Rule has no condition, so it matches
                return rule, operation_allowed, RulesEvaluationResult.MATCH

        # No rules matched, use default behavior
        if self.default_rule is not None:
            # Use the specified default rule
            if self.default_rule.action == "ALLOW":
                return self.default_rule, True, RulesEvaluationResult.NO_MATCH
            else:  # DENY
                return self.default_rule, False, RulesEvaluationResult.NO_MATCH
        else:
            # Default to ALLOW if no default rule is specified
            return None, True, RulesEvaluationResult.NO_MATCH
