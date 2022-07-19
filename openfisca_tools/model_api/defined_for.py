import numpy as np
from openfisca_core.entities import Entity
from openfisca_core.populations import Population, GroupPopulation
from openfisca_core.variables import Variable
from numpy.typing import ArrayLike
from typing import Any, Callable


def make_partially_executed_formula(
    formula: Callable, mask: ArrayLike, default_value: Any = 0
) -> Callable:
    # Edge cases that need to be covered:
    # * entity(variable, period)
    # * entity.members(variable, period)
    # * entity.parent_entity(variable, period)

    def partially_executed_formula(entity, period, parameters):
        if isinstance(mask, str):
            mask = entity(mask, period)

        def entity_call(self, variable, period):
            full_result = Variable(entity, period, parameters)
            return full_result[mask]

        setattr(entity, "__call__", entity_call)

        result = np.full(mask.shape, default_value)
        result[mask] = formula(entity, period, parameters)

        return result
