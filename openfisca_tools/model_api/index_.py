from typing import List, Union
import numpy as np
from openfisca_core.parameters import Parameter
from numpy.typing import ArrayLike


def index_(
    into: Parameter,
    indices: Union[ArrayLike, List[ArrayLike]],
    where: ArrayLike,
    fill: float = 0,
) -> ArrayLike:
    """Indexes into a object, but only when a condition is true. This improves
    performance over `np.where`, which will index all values and then filter the result.

    Args:
        into (Parameter): The parameter to index into.
        indices (Union[ArrayLike, List[ArrayLike]]): The full, un-filtered index array. Can be a list of arrays
            for sequential indexing.
        where (ArrayLike): A filter for indexing.
        fill (float, optional): The value to fill where `index_where` is False. Defaults to 0.

    Returns:
        ArrayLike: The indexed result.
    """
    if where.sum() == 0:
        return np.ones(where.shape) * fill

    if isinstance(indices, list):
        result = np.empty_like(indices[0])
        intermediate_result = into
        for i in range(len(indices)):
            intermediate_result = intermediate_result[indices[i][where]]
        result[where] = intermediate_result
    else:
        result = np.empty_like(indices)
        result[where] = into[indices[where]]
    result[~where] = fill
    return result.astype(float)
