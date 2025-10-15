#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : RuleObjectDirectory.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025


from datetime import datetime


class RuleObjectDirectory(object):
    """
    RuleObjectDirectory class.
    """

    name: str
    path: str
    modified_at: datetime
    created_at: datetime

    def __init__(
        self,
        name: str,
        path: str,
        modified_at: datetime,
        created_at: datetime,
    ):
        self.name = name
        self.path = path
        self.modified_at = modified_at
        self.created_at = created_at

    def __repr__(self):
        return f"RuleObjectDirectory(name={self.name}, path={self.path}, modified_at={self.modified_at}, created_at={self.created_at})"
