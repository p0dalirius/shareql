#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : parser.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 05 Sep 2025


import os

from lark import Lark, LarkError, UnexpectedInput

from shareql.ast.rule import Rule
from shareql.ast.transformer import RuleTransformer


class RuleParser(object):
    """
    RuleParser class that extends the Lark class.

    Attributes:
        grammar (str): The grammar to use for parsing.
    """

    rule_id_counter = 1

    def __init__(self):
        self.grammar = None
        self.__load_grammar()
        self.parser = Lark(grammar=self.grammar, parser="lalr")

    def parse_file(self, file: str) -> tuple[list[str], list[str]]:
        """
        Parse a file of rules.
        """
        with open(file, "r") as f:
            text = f.read()
        return self.parse(text)

    def parse(self, text: str) -> tuple[list[str], list[str]]:
        """
        Parse a text of rules.

        Returns:
            tuple[list[str], list[str]]: A tuple containing the parsed rules and any parsing errors.
        """
        parsing_errors = []
        parsed_rules = []
        for lineno, line in enumerate(text.split("\n"), start=1):
            line = line.strip()
            if line == "":
                continue
            try:
                parsed_rules.extend(self.parse_line(line))
            except UnexpectedInput as e:
                prompt_line = f"[line:{lineno}] "
                prompt_indent = " " * (len(prompt_line) - 2) + "│ "
                error_msg = (
                    prompt_line
                    + f"Syntax error in line {lineno} at position {e.column}: {line}\n"
                )
                error_msg += prompt_indent + e.get_context(
                    line, span=40
                ).strip().replace("\n", "\n" + prompt_indent)

                parsing_errors.append(error_msg)
            except LarkError as e:
                parsing_errors.append(
                    f"\nParsing error in line {lineno} at position {e.column}: {line}"
                    + str(e)
                )

        return parsed_rules, parsing_errors

    def __load_grammar(self):
        """
        Load the grammar from the grammar.txt file.
        """
        with open(os.path.join(os.path.dirname(__file__), "grammar.txt"), "r") as f:
            self.grammar = f.read()

    def parse_line(self, line):
        """
        Parse a single line of rules.

        Returns:
            list[Rule]: A list of parsed rules.
        """
        if self.grammar is None:
            self.__load_grammar()

        rules = []

        line = line.strip()
        if line.startswith("#") or len(line) == 0:
            return []

        parse_trees = RuleTransformer().transform(self.parser.parse(line))

        for parse_tree in parse_trees:
            for child in parse_tree.children:
                if isinstance(child, Rule):
                    child.id = self.rule_id_counter
                    self.rule_id_counter += 1
                    rules.append(child)

        return rules
