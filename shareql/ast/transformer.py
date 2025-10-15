#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : transformer.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

from lark import Transformer

from shareql.ast.boolop import BoolOp
from shareql.ast.condition import Condition
from shareql.ast.notop import NotOp
from shareql.ast.rule import Rule


class RuleTransformer(Transformer):
    """
    Transformer for the rules.
    """

    def ACTION(self, token):
        return str(token)

    def OPERATION(self, token):
        return str(token)

    def FIELD(self, token):
        return str(token)

    def OPERATOR(self, token):
        return str(token)

    def STRING(self, token):
        return token[1:-1]

    def NUMBER(self, token):
        return int(token)

    def REGEX(self, token):
        inside = token[token.find("(") + 1 : token.rfind(")")]
        return ("REGEX", inside.strip('"'))

    def list(self, items):
        return list(items)

    def condition(self, items):
        return Condition(field=items[0], operator=items[1], value=items[2])

    def or_(self, items):
        return BoolOp("OR", items[0], items[1])

    def and_(self, items):
        return BoolOp("AND", items[0], items[1])

    def xor(self, items):
        return BoolOp("XOR", items[0], items[1])

    def not_(self, items):
        return NotOp(items[0])

    def default_rule(self, items):
        """Handle DEFAULT rule."""
        return Rule(action=items[0], operation="DEFAULT", condition=None)

    def rule(self, items):
        # Handle regular rules
        action = items[0]
        op = None
        cond = None
        rest = items[1:]
        if rest:
            if isinstance(rest[0], str) and rest[0] not in ("IF",):
                op = rest[0]
                if len(rest) > 1:
                    cond = rest[1]
            else:
                cond = rest[0]
        return Rule(action=action, operation=op, condition=cond)

    def start(self, items):
        return items
