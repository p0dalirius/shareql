#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : RulesEvaluationResult.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

from enum import Enum


class RulesEvaluationResult(Enum):
    MATCH = "Rules matched"
    NO_MATCH = "No rules matched"
    ERROR = "Error"
