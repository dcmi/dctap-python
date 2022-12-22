# Changelog
Starting with version 0.3.2, notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Keywords used: Added, Changed, Deprecated, Removed, Fixed, Security.

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
