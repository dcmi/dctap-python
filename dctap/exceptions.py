"""Exception classes for dctap."""


class DctapError(SystemExit):
    """Exceptions related to Dctap generally."""


class ConfigError(DctapError):
    """Exceptions related to configuration."""
