"""Exception classes for dctap."""


class DctapError(SystemExit):
    """Exceptions related to Dctap generally."""


class ConfigError(DctapError):
    """Exceptions related to configuration."""


class NoDataError(DctapError):
    """Exception raised if there is no (TAP) data to process."""
