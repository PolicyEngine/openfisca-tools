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
            mask_values = entity(mask, period)
        else:
            mask_values = mask

        def entity_call(self, variable, period):
            full_result = Variable(entity, period, parameters)
            return full_result[mask_values]

        setattr(entity, "__call__", entity_call)

        result = np.full(mask_values.shape, default_value)
        result[mask_values] = formula(entity, period, parameters)

        return result
    
    return partially_executed_formula
