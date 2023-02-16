# Changelog

Documents notable changes to this project starting with version 0.3.2.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Keywords: Added, Changed, Deprecated, Removed, Fixed, Security.

## Under consideration

- Better documentation of function arguments in docstrings and their inclusion in [project documentation](https://tapshex.readthedocs.io/en/latest/).
- Create dictionary of valid values for elements and value constraint types, many of which are currently hard-wired in the shape and statement template classes, for folding into `config_dict` in order to facilitate customization when the classes imported and sub-classed in other packages.
- Possibly remove and replace the arguably over-elaborate "loggers" (`loggers.py`).

## [0.4.5] - 2023-02-16

- Computation of element aliases excludes privates.

## [0.4.4] - 2023-02-08

- Csvreader now looks for prefixes used in value constraints.
- Added unit tests.

## [0.4.3] - 2023-01-28

- Make `csvreader._get_rows` more robust by testing for edge cases.

## [0.4.2] - 2023-01-24

- Function dctap.csvreader now can also take a CSV string as input (not just an open file object).

## [0.4.1] - 2023-01-20

- Change imports from relative to absolute, `from .exceptions...` to `from dctap.exceptions`.
- Pylint, black.
- Added unit tests.

## [0.4.0] - 2023-01-09

For this release, unit tests (and their docstrings) were updated. The command-line utility was slightly simplified. Function parameters, variables, and error messages were changed for the sake of consistency and clarity and to facilitate the reconfiguration of classes and functions in this package with different defaults when imported into other packages.

#### Added

- `dctap.utils.load_yaml_to_dict`, reads a YAML string or file and returns a Python dictionary.

#### Removed

- Removed from the command-line utility the option `dctap init --hidden`, which had generated `.dctaprc`. Users who want to have a "hidden" config file can rename `dctap.yaml` by hand and point to it with `dctap read --config PATH` or with `get_config(nondefault_configfile_name=PATH)`.
- Removed from `dctap.inspect.pprint_tapshapes` the parameters `shape_class` and `state_class`, no longer needed.
- Removed the utility `dctap.utils.strip_enclosing_angle_brackets`, not used (ie, no evidence that anyone records URIs in a TAP enclosed with angle brackets).

#### Changed

- Changed arguments of `dctap.config.get_config`:
  - 0.3.15: One optional parameter `configfile_name`. Three to which (overridable) defaults are passed: `config_yamldoc`, `shape_class`, `state_class`.
  - 0.4.0: Two optional parameters: `nondefault_configyaml_str`, `nondefault_configfile_name`. Four to which (overridable) defaults are passed: `default_configyaml_str`, `default_configfile_name`, `default_shape_class`, `default_state_class`.
    - Why: Clarity of intention. Facilitates configuration with other defaults when imported by other packages downstream. Passing a non-default YAML string is useful for unit tests and possibly also for advanced users.
- Changed arguments of `dctap.config.write_configfile`:
  - 0.3.15: Two parameters to which (overridable) defaults are passed: `configfile_name`, `config_yamldoc`.
  - 0.4.0: One optional parameter `nondefault_configyaml_str`. Two to which (overridable) defaults are passed: `default_configfile_name`, `default_configyaml_str`.
- Changed `dctap.config.get_stems` and `dctap.config.get_shems` into "private" functions `_get_stems` and `_get_shems`, which are called by only one function, `dctap.config.get_config`.
- Changed parameters of various other internal, "private" functions called by `get_config`.
- Simplified `dctap.utils.is_uri_or_prefixed_uri` and renamed to `dctap.utils.looks_like_uri_or_curie`.

## [0.3.15] - 2022-12-26

- Improve efficiency/readability of normalization functions, eg for Boolean values.

## [0.3.14] - 2022-12-23

- csvreader now called with keyword args for state_class and shape_class.

## [0.3.13] - 2022-12-22

- csvreader outputs just one shapes dictionary, now includes "warnings".
- JSON and YAML outputs now include "warnings" section.
- Documentation updated.

## [0.3.12] - 2022-12-22

- JSON and YAML outputs now include "namespaces" section.

## [0.3.11] - 2022-12-11

- Make imports within dctap relative again.

## [0.3.10] - 2022-12-11

- Configuration options: list_element and list_item_separator changed to picklist...

## [0.3.9] - 2022-12-10

- Support and documentation for extra element aliases

## [0.3.8] - 2022-12-08

- Tweaked terminology used in glossary following discussion in DCTAP WG.

## [0.3.7] - 2022-12-08

- Improved documentation.

## [0.3.6] - 2022-12-04

- Added support and documentation for value constraint types MinLength and MinInclusive.

## [Unreleased]

- Added improvements to README.rst.

## [0.3.3] - 2021-07-27

- Added examples section to default help display when command run without arguments.
- Added CHANGELOG.md.

## [0.3.2] - 2021-07-22

- Added examples and explanation to Readthedocs.
- Fixed so that "extra" elements passed through to output with original upper/lowercase.
- Added (optional) warnings to stderr not just for text output, but for JSON and YAML.
- Added (optional) warning when header not recognized as DCTAP element or a configured extra.
