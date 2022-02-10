import logging
from openfisca_core.model_api import (
    DAY,
    MONTH,
    YEAR,
    ETERNITY,
    Variable as CoreVariable,
    Reform,
    max_,
    min_,
)
from openfisca_core.populations import Population
from openfisca_core.entities import Entity
from typing import Callable, List, Tuple, Type, Union
import numpy as np
from numpy.typing import ArrayLike
from pandas import Period
from itertools import product

ReformType = Union[Reform, Tuple[Reform]]

allowed_variable_attributes = ("metadata", "quantity_type")

STOCK = "Stock"
FLOW = "Flow"


class Variable(CoreVariable):
    quantity_type: str = FLOW

    def __init__(self, baseline_variable=None):
        try:
            CoreVariable.__init__(self, baseline_variable=baseline_variable)
        except ValueError as e:
            if all(
                [
                    attribute not in str(e)
                    for attribute in allowed_variable_attributes
                ]
            ):
                raise e

        self.is_neutralized = False


np.random.seed(0)


def for_each_variable(
    entity: Population,
    period: Period,
    variables: List[str],
    agg_func: str = "add",
    group_agg_func: str = "add",
    options: List[str] = None,
) -> ArrayLike:
    """Applies operations to lists of variables.

    Args:
        entity (Population): The entity population, as passed in formulas.
        period (Period): The period, as pass in formulas.
        variables (List[str]): A list of variable names.
        agg_func (str, optional): The operation to apply to combine variable results. Defaults to "add".
        group_agg_func (str, optional): The operation to apply to transform values to the target entity level. Defaults to "add".
        options (List[str], optional): Options to pass to the `entity(variable, period)` call. Defaults to None.

    Raises:
        ValueError: If any target variable is not at or below the target entity level.

    Returns:
        ArrayLike: The result of the operation.
    """
    result = None
    agg_func = dict(
        add=lambda x, y: x + y, multiply=lambda x, y: x * y, max=max_, min=min_
    )[agg_func]
    if not entity.entity.is_person:
        group_agg_func = dict(
            add=entity.sum, all=entity.all, max=entity.max, min=entity.min
        )
    for variable in variables:
        variable_entity = entity.entity.get_variable(variable).entity
        if variable_entity.key == entity.entity.key:
            values = entity(variable, period, options=options)
        else:
            try:
                values = group_agg_func(
                    entity.members(variable, period, options=options)
                )
            except:
                raise ValueError(
                    f"Variable {variable} is not defined for {entity.label} or {entity.label} members."
                )
        if result is None:
            result = values
        else:
            result = agg_func(result, values)
    return result


def add(
    entity: Population,
    period: Period,
    variables: List[str],
    options: List[str] = None,
):
    """Sums a list of variables.

    Args:
        entity (Population): The entity population, as passed in formulas.
        period (Period): The period, as pass in formulas.
        variables (List[str]): A list of variable names.
        options (List[str], optional): Options to pass to the `entity(variable, period)` call. Defaults to None.

    Raises:
        ValueError: If any target variable is not at or below the target entity level.

    Returns:
        ArrayLike: The result of the operation.
    """
    return for_each_variable(
        entity, period, variables, agg_func="add", options=options
    )


def aggr(entity, period, variables, options=None):
    """Sums a list of variables belonging to entity members.

    Args:
        entity (Population): The entity population, as passed in formulas.
        period (Period): The period, as pass in formulas.
        variables (List[str]): A list of variable names.
        options (List[str], optional): Options to pass to the `entity(variable, period)` call. Defaults to None.

    Raises:
        ValueError: If any target variable is not below the target entity level.

    Returns:
        ArrayLike: The result of the operation.
    """
    return for_each_variable(
        entity,
        period,
        variables,
        agg_func="add",
        group_agg_func="add",
        options=options,
    )


def and_(
    entity: Population,
    period: Period,
    variables: List[str],
    options: List[str] = None,
):
    """Performs a logical and operation on a list of variables.

    Args:
        entity (Population): The entity population, as passed in formulas.
        period (Period): The period, as pass in formulas.
        variables (List[str]): A list of variable names.
        options (List[str], optional): Options to pass to the `entity(variable, period)` call. Defaults to None.

    Raises:
        ValueError: If any target variable is not at the target entity level.

    Returns:
        ArrayLike: The result of the operation.
    """
    return for_each_variable(
        entity, period, variables, agg_func="multiply", options=options
    )


or_ = add
any_ = or_

select = np.select


clip = np.clip
inf = np.inf

WEEKS_IN_YEAR = 52
MONTHS_IN_YEAR = 12


def amount_over(amount: ArrayLike, threshold: float) -> ArrayLike:
    """Calculates the amounts over a threshold.

    Args:
        amount (ArrayLike): The amount to calculate for.
        threshold_1 (float): The threshold.

    Returns:
        ArrayLike: The amounts over the threshold.
    """
    logging.warning(
        "amount_over(x, y) is deprecated, use max_(x - y, 0) instead."
    )
    return max_(0, amount - threshold)


def amount_between(
    amount: ArrayLike, threshold_1: float, threshold_2: float
) -> ArrayLike:
    """Calculates the amounts between two thresholds.

    Args:
        amount (ArrayLike): The amount to calculate for.
        threshold_1 (float): The lower threshold.
        threshold_2 (float): The upper threshold.

    Returns:
        ArrayLike: The amounts between the thresholds.
    """
    return clip(amount, threshold_1, threshold_2) - threshold_1


def random(entity, reset=True):
    x = np.random.rand(entity.count)
    if reset:
        np.random.seed(0)
    return x


def is_in(values: ArrayLike, *targets: list) -> ArrayLike:
    """Returns true if the value is in the list of targets.

    Args:
        values (ArrayLike): The values to test.

    Returns:
        ArrayLike: True if the value is in the list of targets.
    """
    if (len(targets) == 1) and isinstance(targets[0], list):
        targets = targets[0]
    return np.any([values == target for target in targets], axis=0)


def between(
    values: ArrayLike, lower: float, upper: float, inclusive: bool = True
) -> ArrayLike:
    """Returns true if values are between lower and upper.

    Args:
        values (ArrayLike): The input array.
        lower (float): The lower bound.
        upper (float): The upper bound.
        inclusive (bool, optional): Whether to include or exclude the bounds. Defaults to True.

    Returns:
        ArrayLike: The resulting array.
    """
    if inclusive:
        return (values >= lower) & (values <= upper)
    else:
        return (values > lower) & (values < upper)


def uprated(by: str = None, start_year: int = 2015) -> Callable:
    """Attaches a formula applying an uprating factor to input variables (going back as far as 2015).

    Args:
        by (str, optional): The name of the parameter (under parameters.uprating). Defaults to None (no uprating applied).

    Returns:
        Callable: A class decorator.
    """

    def uprater(variable: Type[Variable]) -> type:
        if hasattr(variable, f"formula_{start_year}"):
            return variable

        formula = variable.formula if hasattr(variable, "formula") else None

        def formula_start_year(entity, period, parameters):
            if by is None:
                return entity(variable.__name__, period.last_year)
            else:
                uprating = (
                    parameters(period).uprating[by]
                    / parameters(period.last_year).uprating[by]
                )
                old = entity(variable.__name__, period.last_year)
                if (formula is not None) and (all(old) == 0):
                    # If no values have been inputted, don't uprate and
                    # instead use the previous formula on the current period.
                    return formula(entity, period, parameters)
                return uprating * old

        formula_start_year.__name__ = f"formula_{start_year}"
        setattr(variable, formula_start_year.__name__, formula_start_year)
        return variable

    return uprater


def carried_over(variable: type) -> type:
    return uprated()(variable)


def sum_of_variables(variables: Union[List[str], str]) -> Callable:
    """Returns a function that sums the values of a list of variables.

    Args:
        variables (Union[List[str], str]): A list of variable names.

    Returns:
        Callable: A function that sums the values of the variables.
    """

    def sum_of_variables(entity, period, parameters):
        if isinstance(variables, str):
            # A string parameter name is passed
            node = parameters(period)
            for name in variables.split("."):
                node = getattr(node, name)
            variable_names = node
        else:
            variable_names = variables
        return add(entity, period, variable_names)

    return sum_of_variables
