from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.model_api import *
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_tools.model_api.piecewise_formulas import piecewise_formula

def test_piecewise_formula():
    from openfisca_us.entities import entities
    Person = entities[-1]
    system = TaxBenefitSystem(entities)

    def is_child(person, period, parameters):
        return person("is_child", period)
    
    def five(person, period, parameters):
        return 5

    class some_variable(Variable):
        value_type = float
        entity = Person
        definition_period = YEAR

        formula = piecewise_formula(
            is_child,
            five,
        )

    system.add_variables(some_variable)

    data = {
        "people": {
            "person": {},
        }
    }

    simulation_builder = SimulationBuilder()
    simulation = simulation_builder.build_from_entities(system, data)

    assert simulation.calculate("some_variable") != 5
