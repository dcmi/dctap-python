# Changelog

Documents notable changes to this project since version 0.3.2.

The format is based on [Keep a Changelog]( https://keepachangelog.com/en/1.0.0/ ),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Keywords used: Added, Changed, Deprecated, Removed, Fixed, Security.

## Unreleased (or under consideration)

- Possibly take more "hard-wired" defaults out of function bodies and move them into `@dctap_defaults`, such as `default_shape_name` and `picklist_item_separator`, and maybe even `prefixes`.
- Better documentation of function arguments in docstrings and their inclusion in [project documentation](https://tapshex.readthedocs.io/en/latest/).

## [0.4.0] - 2023-01-03

### Added

- A new decorator, `@dctap_defaults`, serves as a single source of default settings for the package. It currently holds defaults for the shape class, statement template class, a default YAML text holding common namespace prefixes, and the name of the configuration file (`dctap.yaml`). The intended use of the decorator is to pass keyword arguments to a function that will collect them in a `**kwargs` argument. Attempts to call a decorator function by trying to pass a decorator-internal variable explicitly will trigger an exception. Creation of this decorator was motivated by a desire to make it easier for other projects downstream to create

### Removed
- `dctap init` no longer has an option to generate a "Hidden" configuration file ".dctaprc". Note that users can still rename "dctap.yaml" to ".dctaprc" (or anything else) by hand and point to it with `dctap read` or with various functions).

### Changed
- Arguments of `dctap.config.get_config`:
  - 0.3.15: `configfile_name`, `config_yamldoc`, `shape_class`, `state_class`
  - 0.4.0: `config_yamlfile`, `config_yamlstring`, `**kwargs` (which receives `configfile` and `configyaml` from decorator `@dctap_defaults`).

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
