def test_vary_parameter():
    """Tests that a parameter passed to `IndividualSim.vary` returns a correct array."""

    from openfisca_us import IndividualSim

    sim = IndividualSim(year=2022)
    sim.add_person(name="person", age=30)
    sim.add_spm_unit(name="spm_unit", members=["person"])
    sim.vary(
        parameter="usda.snap.max_allotment.main.CONTIGUOUS_US.1",
        min=0,
        max=500,
        step=250,
    )
    results = sim.calc("snap_normal_allotment")
    assert results.shape == (
        3,
        1,
    ), "Incorrect shape of results: expected (3 = number of reform steps, 1 = number of SPM units"
    assert (
        results[-1][0] > results[0][0]
    ), "The last value should be greater than the first (as the reform increases benefit generosity)."


test_vary_parameter()
