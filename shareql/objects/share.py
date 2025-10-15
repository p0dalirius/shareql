#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : RuleObjectShare.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025


class RuleObjectShare(object):
    """
    RuleObjectShare class.
    """

    name: str
    description: str
    hidden: bool

    def __init__(self, name: str, description: str, hidden: bool):
        self.name = name
        self.description = description
        self.hidden = hidden

    def __repr__(self):
        return f"RuleObjectShare(name={self.name}, description={self.description}, hidden={self.hidden})"
