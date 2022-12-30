"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
from dctap.defaults import dctap_defaults
from dctap.tapclasses import TAPShape, TAPStatementTemplate

def default_shapeclass(stateclass=None):
    """Passes hard-wired default DCTAP class argument values to decorated function."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["shapeclass"] = TAPShape
            kwargs["stateclass"] = TAPStatementTemplate
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                raise TypeError(f"@{deco} passed unexpected kwarg to {name}()") from te
        return wrapper
    return decorator

def default_stateclass(stateclass=None):
    """Passes hard-wired default DCTAP class argument values to decorated function."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["shapeclass"] = TAPShape
            kwargs["stateclass"] = TAPStatementTemplate
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                raise TypeError(f"@{deco} passed unexpected kwarg to {name}()") from te
        return wrapper
    return decorator

def default_configfile(configfile=None):
    """Passes hard-wired default configfile argument to decorated function."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["configfile"] = "dctap.yaml"
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                raise TypeError(f"@{deco} passed unexpected kwarg to {name}()") from te
        return wrapper
    return decorator

def test_decorator_default_classes():
    """Default argument values are hard-wired into the decorator itself."""
    @default_shapeclass()
    @default_stateclass()
    def some_func(shapeclass=None, stateclass=None, configfile=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shapeclass"] == TAPShape
    assert actual_values["stateclass"] == TAPStatementTemplate
    assert actual_values["configfile"] == None

def test_decorator_default_classes_plus_default_configfile():
    """Default argument values are hard-wired into the decorator itself."""
    @default_configfile()
    @default_stateclass()
    def some_func(shapeclass=None, stateclass=None, configfile=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shapeclass"] == TAPShape
    assert actual_values["stateclass"] == TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"

def test_decorator_default_classes_plus_default_configfile_passed_to_kwargs():
    """Decorator passes keyword arguments to function that captures in kwargs."""
    @default_configfile()
    @default_stateclass()
    def some_func(**kwargs):
        """@@@"""
        values_from_arguments = {}
        for (key, value) in kwargs.items():
            values_from_arguments[key] = value
            values_from_arguments[key] = value
            values_from_arguments[key] = value
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shapeclass"] == TAPShape
    assert actual_values["stateclass"] == TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"


@pytest.mark.skip
def test_decorated_function_cannot_be_called_with_args_that_override_decorator():
    """Decorated function cannot be called with args that override decorator."""
    @dctap_defaults()
    def some_func(shapeclass=None, stateclass=None, configfile=None, yamldoc=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = some_func(yamldoc="QUUX")
    assert actual_values["yamldoc"] != "QUUX"

