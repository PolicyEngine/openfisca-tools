import numpy as np
from openfisca_core.entities import Entity
from openfisca_core.populations import Population, GroupPopulation
from openfisca_core.variables import Variable
from openfisca_core.projectors import EntityToPersonProjector, Projector
from numpy.typing import ArrayLike
from typing import Any, Callable


class CallableSubset:
    def __init__(self, callable: Callable, mask: ArrayLike):
        self.callable = callable
        self.mask = mask

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)[self.mask]


class PopulationSubset:
    def __init__(self, population: Population, mask: ArrayLike):
        self.population = population
        self.mask = mask

    def __call__(self, *args, **kwargs):
        return self.population(*args, **kwargs)[self.mask]

    def __getattribute__(self, attribute):
        if attribute in ("population", "mask"):
            return object.__getattribute__(self, attribute)
        original_result = self.population.__getattribute__(attribute)
        if isinstance(original_result, EntityToPersonProjector):
            # e.g. person.household
            return PopulationSubset(original_result, self.mask)
        elif attribute in (
            "sum",
            "min",
            "max",
            "nb_persons",
        ):
            return CallableSubset(original_result, self.mask)
        return original_result


def make_partially_executed_formula(
    formula: Callable, mask: ArrayLike, default_value: Any = 0
) -> Callable:
    # Edge cases that need to be covered:
    # * entity(variable, period)
    # * entity.members(variable, period)
    # * entity.parent_entity(variable, period)

    def partially_executed_formula(entity, period, parameters):
        if isinstance(mask, str):
            mask_entity = entity.simulation.tax_benefit_system.variables[
                mask
            ].entity.key
            if entity.entity.key != mask_entity:
                mask_values = getattr(entity, mask_entity)(mask, period)
            else:
                mask_values = entity(mask, period)
        else:
            mask_values = mask

        subset_entity = PopulationSubset(entity, mask_values)

        formula_result = formula(subset_entity, period, parameters)
        formula_result = np.array(formula_result)
        result = (
            np.ones_like(mask_values, dtype=formula_result.dtype)
            * default_value
        )
        result[mask_values] = formula_result

        entity = subset_entity.population

        return result

    return partially_executed_formula
