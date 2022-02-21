def test_parameter_interpolation():
    """
    Test that a parameter with two values can be interpolated.
    """
    from openfisca_core.parameters import ParameterNode

    # Create the parameter

    root = ParameterNode(
        data={
            "a": {
                "description": "Parent",
                "b": {
                    "description": "b",
                    "values": {
                        "2010-01-01": 1,
                    },
                },
                "c": {
                    "d": {
                        "e": {
                            "values": {
                                "2010-01-01": 2,
                            }
                        }
                    },
                },
                "metadata": {
                    "propagate_metadata_to_children": True,
                    "example_field": "example_value",
                },
            }
        }
    )

    from openfisca_tools.parameters import propagate_parameter_metadata

    propagated = propagate_parameter_metadata(root)

    assert (
        "example_field" in propagated.a.b.metadata
    ), "Metadata not passed down to direct child"
    assert (
        "example_field" in propagated.a.c.d.e.metadata
    ), "Metadata not passed down to descendent"