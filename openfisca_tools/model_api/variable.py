import logging
import pandas as pd
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
from openfisca_core.errors import VariableNotFoundError
from openfisca_core.entities import Entity
from typing import Callable, List, Tuple, Type, Union
import numpy as np
from numpy.typing import ArrayLike
from pandas import Period
from itertools import product

ReformType = Union[Reform, Tuple[Reform]]

allowed_variable_attributes = ("metadata", "quantity_type", "is_eligible")

STOCK = "Stock"
FLOW = "Flow"


class Variable(CoreVariable):
    quantity_type: str = FLOW

    def __init__(self, baseline_variable=None):
        self.is_neutralized = False

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

        attr_dict = self.__class__.__dict__

        if "is_eligible" in attr_dict and "formula" in attr_dict:
            is_eligible = attr_dict["is_eligible"]
            formula = attr_dict["formula"]

            def override_population(population, filter_values):
                def population_caller_override(self, variable, period):
                    return population(variable, period)[filter_values]

                population.__call__ = population_caller_override

                def population_getattr_override(self, attribute):
                    projector = getattr(population, attribute)

                    def projector_caller_override(self, variable, period):
                        return projector(variable, period)[filter_values]

                    projector.__call__ = projector_caller_override

                    return projector

                population.__getattr__ = population_getattr_override

                return population

            def override_formula(formula):
                def new_formula(population, period, parameters):
                    eligible = is_eligible(population, period, parameters)
                    population = override_population(population, eligible)
                    values = formula(population, period, parameters)
                    complete_values = np.ones(
                        eligible.shape) * self.default_value
                    complete_values[eligible] = values
                    return complete_values

                return new_formula

            self.formulas = self.set_formulas(
                {"formula": override_formula(formula)})
