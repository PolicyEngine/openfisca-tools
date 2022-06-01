from openfisca_core.populations import Population
from openfisca_core.periods import Period
from openfisca_core.parameters import ParameterNodeAtInstant
from typing import Callable
from numpy.typing import ArrayLike

ZERO_FORMULA = lambda population, period, parameters: 0

def override_population_with_mask(population: Population, mask: ArrayLike[bool]):
    def mask_result_of_call_function(call_fn: Callable):
        def new_fn(*args, **kwargs):
            return call_fn(*args, **kwargs)[mask]
    
    population.__call__ = mask_result_of_call_function(population.__call__)

    def mask_result_of_getattr_result_call(getattr_fn: Callable):
        def new_getattr_fn(*args, **kwargs):
            projector = getattr_fn(*args, **kwargs)
            projector.__call__ = mask_result_of_call_function(projector.__call__)
            return projector

    population.__getattr__ = mask_result_of_getattr_result_call

    return population


def piecewise_formula(
    condition: Callable[[Population, Period, ParameterNodeAtInstant], ArrayLike[bool]],
    formula_if_true: Callable[[Population, Period, ParameterNodeAtInstant], ArrayLike],
    formula_if_false: Callable[[Population, Period, ParameterNodeAtInstant], ArrayLike] = ZERO_FORMULA,
) -> Callable[[Population, Period, ParameterNodeAtInstant], ArrayLike]:
    def formula(population, period, parameters):
        condition = condition(population, period, parameters)
        true_population = override_population_with_mask(population, condition)
        false_population = override_population_with_mask(population, ~condition)
        result_for_true_members = formula_if_true(true_population, period, parameters)
        result_for_false_members = formula_if_false(false_population, period, parameters)
        