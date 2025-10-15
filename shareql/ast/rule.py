#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : rule.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

from dataclasses import dataclass
from typing import Union

from shareql.ast.boolop import BoolOp
from shareql.ast.condition import Condition
from shareql.ast.notop import NotOp


@dataclass
class Rule:

    id: int
    action: str
    operation: Union[str, None] = None
    condition: Union[Condition, BoolOp, NotOp, None] = None

    def __init__(
        self,
        action: str,
        operation: Union[str, None] = None,
        condition: Union[Condition, BoolOp, NotOp, None] = None,
    ):
        self.action = action
        self.operation = operation
        self.condition = condition
