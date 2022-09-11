from openfisca_core.reforms import Reform
from openfisca_core.parameters import Parameter, ParameterNode, ParameterScale
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from datetime import datetime

from openfisca_tools.reforms import get_parameter


def use_current_parameters(date: str = None) -> Reform:
    """Backdates parameters at a given instant to the start of the year.

    Args:
        date (str, optional): The given instant. Defaults to now.

    Returns:
        Reform: The reform backdating parameters.
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    year = date.year
    date = datetime.strftime(date, "%Y-%m-%d")

    def modify_parameters(parameters: ParameterNode):
        for child in parameters.get_descendants():
            if isinstance(child, Parameter):
                current_value = child(date)
                child.update(period=f"year:{year}:1", value=current_value)
            elif isinstance(child, ParameterScale):
                for bracket in child.brackets:
                    if "rate" in bracket.children:
                        current_rate = bracket.rate(date)
                        bracket.rate.update(
                            period=f"year:{year}:1", value=current_rate
                        )
                    if "threshold" in bracket.children:
                        current_threshold = bracket.threshold(date)
                        bracket.threshold.update(
                            period=f"year:{year}:1",
                            value=current_threshold,
                        )
        try:
            parameters.reforms.policy_date.update(
                value=int(datetime.now().strftime("%Y%m%d")),
                period=f"year:{year}:1",
            )
        except:
            pass
        return parameters

    class reform(Reform):
        def apply(self):
            for variable in self.variables:
                if (
                    hasattr(variable, "metadata")
                    and variable.metadata.get("uprating") is not None
                ):
                    uprating_parameter = variable.metadata.get("uprating")
                    parameter = get_parameter(
                        self.parameters, uprating_parameter
                    )
                    start_value = parameter(f"{year}-01-01")
                    end_value = parameter(date)
                    multiplier = end_value / start_value
                    variable.metadata["multiplier"] = multiplier

            self.modify_parameters(modify_parameters)

    return reform
