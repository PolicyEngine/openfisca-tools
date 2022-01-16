def test_parameter_homogenization():
    from openfisca_core.parameters import ParameterNode

    # Create the parameter

    root = ParameterNode(
        data={
            "value_by_country_and_region": {
                "ENGLAND": {
                    "NORTH_EAST": {
                        "2021-01-01": 1,
                    }
                },
                "metadata": {
                    "breakdown": ["country", "region"],
                },
            }
        }
    )

    from openfisca_core.model_api import Enum, Variable, ETERNITY
    from openfisca_core.entities import Entity

    Person = Entity("person", "people", "Person", "A person")

    class Country(Enum):
        ENGLAND = "England"
        SCOTLAND = "Scotland"
        WALES = "Wales"
        NORTHERN_IRELAND = "Northern Ireland"

    class country(Variable):
        value_type = Enum
        entity = Person
        definition_period = ETERNITY
        possible_values = Country
        default_value = Country.ENGLAND

    class Region(Enum):
        NORTH_EAST = "North East"
        NORTH_WEST = "North West"
        SOUTH_EAST = "South East"
        SOUTH_WEST = "South West"
        LONDON = "London"
        EAST_OF_ENGLAND = "East of England"
        WALES = "Wales"
        SCOTLAND = "Scotland"
        WEST_MIDLANDS = "West Midlands"
        NORTHERN_IRELAND = "Northern Ireland"
        EAST_MIDLANDS = "East Midlands"
        YORKSHIRE = "Yorkshire and The Humber"

    class region(Variable):
        value_type = Enum
        entity = Person
        definition_period = ETERNITY
        possible_values = Region
        default_value = Region.NORTH_EAST

    from openfisca_tools.parameters import homogenize_parameter_structures
    from openfisca_core.taxbenefitsystems import TaxBenefitSystem

    system = TaxBenefitSystem([Person])
    system.add_variables(country, region)
    system.parameters = root

    homogenized = homogenize_parameter_structures(
        system.parameters, system.variables, default_value=0
    )

    print(system.parameters.value_by_country_and_region)

    assert (
        system.parameters.value_by_country_and_region.ENGLAND.SOUTH_EAST(
            "2021-01-01"
        )
        == 0
    )
    assert (
        system.parameters.value_by_country_and_region.SCOTLAND.SCOTLAND(
            "2021-01-01"
        )
        == 0
    )
    assert (
        system.parameters.value_by_country_and_region.ENGLAND.NORTH_EAST(
            "2021-01-01"
        )
        == 1
    )
