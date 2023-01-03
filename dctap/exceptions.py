"""Exception classes for dctap."""


class DctapError(SystemExit):
    """Exceptions related to Dctap generally."""


class ConfigError(DctapError):
    """Exceptions related to configuration."""


class DecoratorError(DctapError):
    """Exceptions raised about use of decorator."""


class KwargError(DctapError):
    """Exceptions related to keyword arguments used in function calls."""


class BadYamlError(DctapError):
    """Exceptions related to badly formed YAML strings."""
