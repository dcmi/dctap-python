# Changelog
Starting with version 0.3.2, notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Keywords used: Added, Changed, Deprecated, Removed, Fixed, Security.

## [Unreleased]
- Added examples section to default help display when command run without arguments.

## [0.3.2] - 2021-07-22
- Added examples and explanation to Readthedocs.
- Fixed csvreader.py: "extra" elements passed through to output with original upper/lowercase.
- Added (optional) warnings to stderr not just for text output, but for JSON and YAML.
- Added (optional) warning when a header is not recognized.
