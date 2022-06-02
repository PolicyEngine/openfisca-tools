from openfisca_tools.model_api import add
from openfisca_core.parameters import ParameterNodeAtInstant
from openfisca_core.populations import Population
from openfisca_core.periods import Period
from numpy.typing import ArrayLike
import numpy as np
import pandas as pd


def sum_list_parameter(
    parameter: ParameterNodeAtInstant,
    indices: ArrayLike,
    population: Population,
    period: Period,
) -> ArrayLike:
    """Sums lists of variables, indexing into a breakdown parameter.

    Args:
        parameter (ParameterNodeAtInstant): The parameter to index into.
        indices (ArrayLike): The indices (e.g. the state).
        population (Population): The population to add variables from.
        period (Period): The time period to add variables in.

    Returns:
        ArrayLike: The resultant sums.
    """
    unique_indices = np.unique(indices)
    unique_elements = list(
        set(sum([parameter._children[index] for index in unique_indices], []))
    )
    if len(unique_elements) == 0:
        return np.zeros(len(indices))
    indexed_parameter_contains_element = pd.DataFrame(
        {
            index: {
                element: add(population, period, [element])
                if element in parameter[index]
                else np.zeros(population.count)
            }
            for element in unique_elements
            for index in unique_indices
        }
    )
    series_of_lists = indexed_parameter_contains_element.sum()
    matrix = np.array(
        pd.DataFrame.from_dict(
            dict(zip(series_of_lists.index, series_of_lists.values))
        ).T
    )
    index_to_i = pd.Series(
        index=unique_indices, data=np.arange(len(unique_indices))
    )
    first_index = index_to_i[indices].values
    second_index = np.arange(len(first_index))
    return matrix[first_index, second_index]
