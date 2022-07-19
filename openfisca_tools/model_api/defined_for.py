import numpy as np
from openfisca_core.entities import Entity
from openfisca_core.populations import Population, GroupPopulation
from openfisca_core.variables import Variable
from numpy.typing import ArrayLike
from typing import Any, Callable

class PopulationSubset:
    def __init__(self, population: Population, mask: ArrayLike):
        self.population = population
        self.mask = mask

    def __call__(self, variable, period):
        return self.population(variable, period)[self.mask]


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

        entity = PopulationSubset(entity, mask_values)

        formula_result = formula(entity, period, parameters)
        result = np.ones_like(mask_values, dtype=formula_result.dtype) * default_value
        result[mask_values] = formula_result

        entity = entity.population

        return result
    
    return partially_executed_formula
