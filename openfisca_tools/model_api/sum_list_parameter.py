from openfisca_core.parameters import ParameterNode
from openfisca_core.populations import Population
from openfisca_core.periods import Period
from numpy.typing import ArrayLike

def sum_list_parameter(
    parameter: ParameterNode,
    indices: ArrayLike,
    population: Population,
    period: Period,
) -> ArrayLike:
    """Sums lists of variables, indexing into a breakdown parameter.

    Args:
        parameter (ParameterNode): The parameter to index into.
        indices (ArrayLike): The indices (e.g. the state).
        population (Population): The population to add variables from.
        period (Period): The time period to add variables in.

    Returns:
        ArrayLike: The resultant sums.
    """