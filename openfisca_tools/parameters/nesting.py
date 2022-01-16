from openfisca_core.model_api import Enum
from tkinter import Variable
from typing import Any, Dict, List, Type
from openfisca_core.parameters import ParameterNode, Parameter
import logging


def homogenize_parameter_structures(
    root: ParameterNode, variables: Dict[str, Variable], default_value: Any = 0
) -> ParameterNode:
    for node in root.get_descendants():
        if isinstance(node, ParameterNode):
            breakdown = get_breakdown_variables(node)
            node = homogenize_parameter_node(
                node, breakdown, variables, default_value
            )
    return root


def get_breakdown_variables(node: ParameterNode) -> List[str]:
    """
    Returns the list of variables that are used to break down the parameter.
    """
    breakdown = node.metadata.get("breakdown")
    if breakdown is not None:
        if isinstance(breakdown, str):
            # Single element, cast to list.
            breakdown = [breakdown]
        elif not isinstance(breakdown, list):
            # Not a list, skip process and warn.
            logging.warn(
                f"Invalid breakdown metadata for parameter {node.name}: {type(breakdown)}"
            )
            return None
        return breakdown
    else:
        return None


def homogenize_parameter_node(
    node: ParameterNode,
    breakdown: List[str],
    variables: Dict[str, Variable],
    default_value: Any,
) -> ParameterNode:
    if breakdown is None:
        return node
    first_breakdown = breakdown[0]
    possible_values = list(
        map(lambda enum: enum.name, variables[first_breakdown].possible_values)
    )
    if isinstance(node, Parameter):
        node = ParameterNode(node.name, data={
            child: {"2000-01-01": default_value} for child in possible_values
        })
    missing_values = set(possible_values) - set(node.children)
    further_breakdown = len(breakdown) > 1
    for value in missing_values:
        node.add_child(
            value,
            Parameter(value, {"2000-01-01": default_value}),
        )
    for child in node.children:
        print(f"Recursing into {child}, further breakdown: {further_breakdown}")
        if child not in possible_values:
            logging.warn(
                f"Parameter {node.name} has a child {child} that is not in the possible values of {first_breakdown}, ignoring."
            )
        if further_breakdown:
            node = homogenize_parameter_node(
                node.children[child], breakdown[1:], variables, default_value
            )
    return node
