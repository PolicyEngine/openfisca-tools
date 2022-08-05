# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.13.3] - 2022-08-05

### Added

* Added ability to set dictionary references.

## [0.13.2] - 2022-07-22

### Fixed

* Defined-for logic includes `any` and other group entity transforms.

## [0.13.1] - 2022-07-20

### Fixed

* Bugs in the `defined_for` logic related to group-group entity transforms.

## [0.13.0] - 2022-07-19

### Added

* `defined_for: str`: a `Variable` property that calculates the formula only where the variable `defined_for` is `True`.

## [0.12.0] - 2022-06-22

### Fixed

* `random` now correctly fixes the seed.

## [0.11.0] - 2022-06-02

### Added

* `index_` helper function to speed up conditional parameter indexing.

## [0.10.4] - 2022-05-05

### Fixed

* `add` now throws an error if an invalid entity is given.

## [0.10.3] - 2022-05-05

### Fixed

* `add` maps group-to-group transformations correctly.

## [0.10.2] - 2022-04-25

### Fixed

* Adding a `target` entity to `IndividualSim.calc` now functions correctly when `target` has a different entity type than `variable`.
* Adds `MANIFEST.in` to the repo.

## [0.10.1] - 2022-04-24

### Fixed

* `map_to` is correctly used in `deriv` calls.

## [0.10.0] - 2022-04-18

### Fixed

* Group entities are now created automatically in `IndividualSim`s.

## [0.9.0] - 2022-04-11

### Added

* Datasets can now input variables at multiple time periods.

## [0.8.0] - 2022-04-10

### Added

* OpenFisca data tools previously in UK and US data packages.

## [0.7.3] - 2022-03-28

### Fixed

* All simulation types see a 3-4x speedup in initialisation.

## [0.7.2] - 2022-03-27

### Fixed

* `add` function raises the correct `Exception` class.
* Interpolation only happens once.

## [0.7.1] - 2022-03-22

### Fixed

* Uprating includes parameter scale parameters.

## [0.7.0] - 2022-03-19

### Added

* Self-uprating: where a parameter is uprated using its trend over a given time period.

### Fixed

* Breakdown metadata is not passed down.

## [0.6.0] - 2022-03-02

### Added

* `IndividualSim.vary` now accepts parameters as well as variables.

### Fixed

* Aggregator functions don't inappropriately re-cast irrelevant exceptions.

## [0.5.0] - 2022-02-21

### Added

* Parameter metadata propagation function.

## [0.4.1] - 2022-02-16

### Fixed

* Fixed mistaken import from `turtle` (should be `pandas`).

## [0.4.0] - 2022-02-14

### Added

* `start_instant` property for uprating logic.

## [0.3.1] - 2022-02-11

### Fixed

* Nesting function did not correctly name descendants.

## [0.3.0] - 2022-02-09

### Added

* `GeneralMicrosimulation` alias for `Microsimulation`.
* `between(values, lower, upper)` function for variable formulas.
* `and_`, `or_` and `multiply_` functions for variable formulas.
* `any_` and `any_of_variables` helper functions for variable formulas.

### Changed

* `is_in` and `amount_over` functions deprecated.
* `select` is now an alias for `np.select`.
* `is_in` will work for both `list` and `*args` inputs.
* `household_net_income` used instead of `net_income` for parameter tests.


### Fixed

* Parameter nesting function bug fixes.

## [0.2.3] - 2022-01-26

### Fixed

* Variables with both a formula and an uprating index will now uprate only if there are non-zero values in the last time period.

## [0.2.2] - 2022-01-17

### Fixed

* Incorrect import location for Variable.

## [0.2.1] - 2022-01-17

### Added

* Optional metadata field for stock/flow type for variables.

## [0.2.0] - 2022-01-16

### Added

* Automated parameter nesting - fill missing values in nested parameters.
* Unit test for parameter nesting functions.

## 0.1.9

### Added

* Rounding options for uprating

## 0.1.8

### Added

* Semantic versioning checks

## 0.1.8

### Added

* Consolidated microsimulation and individual simulation interfacts
* Automated testing, interpolation and uprating functions for parameters
* Reform helper functions
