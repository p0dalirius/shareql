#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : condition.py
# Author             : Remi Gascou (@podalirius_)
# Date created       : 02 Sep 2025


from shareql.ast.boolop import BoolOp
from shareql.ast.condition import Condition
from shareql.ast.notop import NotOp


def evaluate_condition(
    condition: [Condition | BoolOp | NotOp], fields: dict[str, any]
) -> bool:
    """
    Evaluate the condition against the target object.

    Args:
        condition: The condition to evaluate
        fields: The fields to evaluate the condition against

    Returns:
        The result of the condition
    """

    if isinstance(condition, Condition):
        return _evaluate_single_condition(condition, fields)
    elif isinstance(condition, BoolOp):
        return _evaluate_bool_operation(condition, fields)
    elif isinstance(condition, NotOp):
        return not evaluate_condition(condition.expr, fields)
    else:
        raise ValueError(f"Unsupported condition type: {type(condition)}")


def _evaluate_single_condition(condition: Condition, fields: dict[str, any]) -> bool:
    """
    Evaluate a single condition against the fields.

    Args:
        condition: The condition to evaluate
        fields: The fields to evaluate the condition against

    Returns:
        The result of the condition
    """

    field_value = fields.get(condition.field)
    condition_value = _extract_value(condition.value)

    if field_value is None:
        return False

    operator = condition.operator

    if operator == "==":
        return field_value == condition_value
    elif operator == "!=":
        return field_value != condition_value
    elif operator == ">":
        return field_value > condition_value
    elif operator == ">=":
        return field_value >= condition_value
    elif operator == "<":
        return field_value < condition_value
    elif operator == "<=":
        return field_value <= condition_value
    elif operator == "CONTAINS":
        return condition_value in str(field_value)
    elif operator == "STARTSWITH":
        return str(field_value).startswith(str(condition_value))
    elif operator == "ENDSWITH":
        return str(field_value).endswith(str(condition_value))
    elif operator == "IN":
        # For IN operator, condition_value should be a list
        if isinstance(condition_value, list):
            return field_value in condition_value
        else:
            return field_value == condition_value
    elif operator == "MATCHES":
        # For MATCHES operator, condition_value should be a regex pattern
        import re

        if isinstance(condition_value, tuple) and condition_value[0] == "REGEX":
            pattern = condition_value[1]
            return bool(re.search(pattern, str(field_value)))
        else:
            # Treat as simple string match
            return str(field_value) == str(condition_value)
    else:
        raise ValueError(f"Unsupported operator: {operator}")


def _evaluate_bool_operation(bool_op: BoolOp, fields: dict[str, any]) -> bool:
    """
    Evaluate a boolean operation (AND, OR, XOR).

    Args:
        bool_op: The boolean operation
        fields: The fields to evaluate the condition against

    Returns:
        The result of the boolean operation
    """

    left_result = evaluate_condition(bool_op.left, fields)
    right_result = evaluate_condition(bool_op.right, fields)

    if bool_op.op == "AND":
        return left_result and right_result
    elif bool_op.op == "OR":
        return left_result or right_result
    elif bool_op.op == "XOR":
        return left_result != right_result
    else:
        raise ValueError(f"Unsupported boolean operation: {bool_op.op}")


def _extract_value(value) -> any:
    """
    Extract the actual value from Tree/Token objects or return the value as-is.

    Args:
        value: The value to extract

    Returns:
        The extracted value
    """

    # Handle Tree objects (from lark parsing)
    if hasattr(value, "children") and hasattr(value, "data"):
        # Tree object - extract from children
        if value.children:
            return value.children[0]
        else:
            return None

    # Handle Token objects (from lark parsing)
    if hasattr(value, "value"):
        return value.value

    # Handle tuple values (like REGEX)
    if isinstance(value, tuple):
        return value

    # Handle list values
    if isinstance(value, list):
        return value

    # Return the value as-is for primitive types
    return value
