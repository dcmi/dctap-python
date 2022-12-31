"""Exception classes for dctap."""


class DctapError(SystemExit):
    """Exceptions related to Dctap generally."""


class ConfigError(DctapError):
    """Exceptions related to configuration."""


class MissingDecoratorError(DctapError):
    """Exceptions raised where decorators should have been used."""


class KwargError(DctapError):
    """Exceptions related to keyword arguments used in function calls."""
