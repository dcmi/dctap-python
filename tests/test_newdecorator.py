"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
from dctap.defaults import dctap_defaults, CONFIGYAML
from dctap.exceptions import MissingDecoratorError, KwargError
import dctap



@pytest.mark.skip(reason="Earlier version of decorator.")
def dctap_defaults(hardwired_shapeclass=None, hardwired_stateclass=None, hardwired_configfile=None, hardwired_yamldoc=None):
    """Passes hard-wired default argument values to decorated function."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["hardwired_shapeclass"] = TAPShape
            kwargs["hardwired_stateclass"] = TAPStatementTemplate
            kwargs["hardwired_configfile"] = "dctap.yaml"
            kwargs["hardwired_yamldoc"] = CONFIGYAML
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                raise TypeError(f"{name}() got unexpected kwarg from @{deco}") from te
        return wrapper
    return decorator


@pytest.mark.skip(reason="Earlier version of decorator.")
def test_dctap_defaults_decorator_defines_default_arguments():
    """Default argument values are hard-wired into the decorator itself."""
    @dctap_defaults()
    def some_func(hardwired_shapeclass=None, hardwired_stateclass=None, hardwired_configfile=None, hardwired_yamldoc=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["hardwired_shapeclass"] == TAPShape
    assert actual_values["hardwired_stateclass"] == TAPStatementTemplate
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"]

@pytest.mark.skip(reason="Earlier version of decorator.")
def config_defaults(hardwired_shapeclass=None, hardwired_stateclass=None, hardwired_configfile=None, hardwired_yamldoc=None):
    """Return dict of keyword arguments for passing to get_config()."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs["hardwired_shapeclass"] = kwargs.get("hardwired_shapeclass", hardwired_shapeclass)
            kwargs["hardwired_stateclass"] = kwargs.get("hardwired_stateclass", hardwired_stateclass)
            kwargs["hardwired_configfile"] = kwargs.get("hardwired_configfile", hardwired_configfile)
            kwargs["hardwired_yamldoc"] = kwargs.get("hardwired_yamldoc", hardwired_yamldoc)
            return func(*args, **kwargs)
        return wrapper
    return decorator

