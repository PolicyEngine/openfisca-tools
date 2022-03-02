def test_vary_variable():
    """Tests that a variable passed to `IndividualSim.vary` returns a correct array."""

    from openfisca_us import IndividualSim

    sim = IndividualSim(year=2022)
    sim.add_person(name="person", age=30)
    sim.add_spm_unit(name="spm_unit", members=["person"])
    sim.vary(
        "employment_income",
        min=0,
        max=2_000 * 12,
        step=200 * 12,
    )
    results = sim.calc("snap")
    assert (
        results[0][-1] < results[0][0]
    ), "The last value should be lesser than the first (as earnings decrease benefit generosity)."
    assert results.shape == (
        1,
        11,
    ), "Incorrect shape of results: expected (1 = number of SPM units, 90 = number of variable steps)"
