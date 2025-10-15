#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : context.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 02 Sep 2025

from shareql.objects.directory import RuleObjectDirectory
from shareql.objects.host import RuleObjectHost
from shareql.objects.share import RuleObjectShare


class RulesEvaluationContext(object):
    """
    RulesEvaluationContext class.

    Attributes:
        depth: The depth of the context
        share: The share of the context
        host: The host of the context
        path: The path of the context
    """

    depth: int

    share: RuleObjectShare
    host: RuleObjectHost
    path: list[RuleObjectDirectory]

    def __init__(
        self,
        depth: int,
        share: RuleObjectShare,
        host: RuleObjectHost,
        path: list[RuleObjectDirectory],
    ) -> None:
        self.depth = depth
        self.share = share
        self.host = host
        self.path = path

    def push_directory(self, directory: RuleObjectDirectory) -> None:
        """
        Push a directory onto the path stack.

        Args:
            directory: The directory to push onto the path
        """
        self.path.append(directory)
        self.depth += 1

    def pop_directory(self) -> RuleObjectDirectory:
        """
        Pop a directory from the path stack.

        Returns:
            The directory that was popped from the path

        Raises:
            IndexError: If the path is empty
        """
        if not self.path:
            raise IndexError("Cannot pop from empty path")

        directory = self.path.pop()
        self.depth -= 1
        return directory

    def set_share(self, share: RuleObjectShare) -> None:
        """
        Set the share of the context.
        """
        self.share = share

    def set_host(self, host: RuleObjectHost) -> None:
        """
        Set the host of the context.
        """
        self.host = host

    def set_depth(self, depth: int) -> None:
        """
        Set the depth of the context.
        """
        self.depth = depth

    def set_path(self, path: list[RuleObjectDirectory]) -> None:
        """
        Set the path of the context.
        """
        self.path = path

    def __repr__(self) -> str:
        return f"RulesEvaluationContext(depth={self.depth}, share={self.share}, host={self.host}, path={self.path})"
