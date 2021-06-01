"""Exception classes for dctap."""


class DctapError(SystemExit):
    """Exceptions related to Dctap generally."""


class ConfigError(DctapError):
    """Exceptions related to configuration."""


class CSVRowError(DctapError):
    """Exceptions related to a single CSVRow."""


class UristemValueError(DctapError):
    """Exceptions related to UriStem value."""


class CsvError(DctapError):
    """Exceptions related to an entire CSV-derived object."""


class BadRegexError(SystemExit):
    """String does not compile as regular expression."""


class BadYamlError(SystemExit):
    """YAML does not parse."""


class NotUTF8Error(SystemExit):
    """File is not UTF8-encoded."""


class ConfigWarning(Warning):
    """Warning regarding configuration (does not stop execution)."""
