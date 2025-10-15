#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : notop.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025

from dataclasses import dataclass
from typing import Any


@dataclass
class NotOp:
    expr: Any
