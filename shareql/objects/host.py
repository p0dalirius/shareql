#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : RuleObjectHost.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025


class RuleObjectHost(object):
    """
    RuleObjectHost class.
    """

    name: str
    address: str

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def __repr__(self):
        return f"RuleObjectHost(name={self.name}, address={self.address})"
