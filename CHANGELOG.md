# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2022-02-09

### Added

* `GeneralMicrosimulation` alias for `Microsimulation`.

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
