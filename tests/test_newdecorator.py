"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
from dctap.defaults import dctap_defaults, CONFIGYAML
import dctap

def default_shapeclass():
    """Passes dctap-python shape class as argument to decorated function."""
    def decorator(func):
        """Takes function as argument and assigns a value to one of its arguments."""
        @wraps(func)
        def wrapper(**kwargs):
            """Takes kwargs dict of decorated function and returns with changes."""
            kwargs["shapeclass"] = dctap.tapclasses.TAPShape
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                message = f"@{deco} passed unexpected kwarg 'shapeclass' to {name}()."
                raise TypeError(message) from te
        return wrapper
    return decorator

def default_stateclass():
    """Passes dctap-python statement template class to decorated function."""
    def decorator(func):
        """Takes function as argument and assigns a value to one of its arguments."""
        @wraps(func)
        def wrapper(**kwargs):
            """Takes kwargs dict of decorated function and returns with changes."""
            kwargs["stateclass"] = dctap.tapclasses.TAPStatementTemplate
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                message = f"@{deco} passed unexpected kwarg 'shapeclass' to {name}()."
                raise TypeError(message) from te
        return wrapper
    return decorator

def default_configfile():
    """Passes dctap-python default configuration file name to decorated function."""
    def decorator(func):
        """Takes function as argument and assigns a value to one of its arguments."""
        @wraps(func)
        def wrapper(**kwargs):
            """Takes kwargs dict of decorated function and returns with changes."""
            kwargs["configfile"] = "dctap.yaml"
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                message = f"@{deco} passed unexpected kwarg 'configfile' to {name}()."
                raise TypeError(message) from te
        return wrapper
    return decorator

def default_configyaml():
    """Passes dctap-python default configuration YAML to decorated function."""
    def decorator(func):
        """Takes function as argument and assigns a value to one of its arguments."""
        @wraps(func)
        def wrapper(**kwargs):
            """Takes kwargs dict of decorated function and returns with changes."""
            kwargs["configyaml"] = dctap.defaults.CONFIGYAML
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                message = f"@{deco} passed unexpected kwarg 'configfile' to {name}()."
                raise TypeError(message) from te
        return wrapper
    return decorator

def test_two_decorators_for_function_with_three_arguments():
    """Two decorators: shapeclass, stateclass."""
    @default_shapeclass()
    @default_stateclass()
    def some_func(shapeclass=None, stateclass=None, configfile=None):
        """Trivial function for testing decorators."""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
    assert actual_values["configfile"] == None

def test_four_decorators():
    """Four decorators: shapeclass, stateclass, configfile, configyaml."""
    @default_shapeclass()
    @default_stateclass()
    @default_configfile()
    @default_configyaml()
    def some_func(shapeclass=None, stateclass=None, configfile=None, configyaml=None):
        """Trivial function for testing decorators."""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        values_from_arguments["configyaml"] = configyaml
        return values_from_arguments
    actual_values = some_func()
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"

@pytest.mark.skip
def test_required_defaults():
    """Exit if any required default argument lacks a value."""
    @default_shapeclass()
    @default_stateclass()
    @default_configfile()
    def some_func(shapeclass=None, stateclass=None, configfile=None):
        """Trivial function for testing decorators."""
        for arg in ["shapeclass", "stateclass", "configfile", "configyaml"]:
            if arg not in locals():
                print("wtf")
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        return values_from_arguments
    actual_values = some_func()
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"

def test_decorator_default_classes_plus_default_configfile_passed_to_kwargs():
    """Decorator passes keyword arguments to function that captures in kwargs."""
    @default_configfile()
    @default_shapeclass()
    @default_stateclass()
    def some_func(**kwargs):
        """@@@"""
        values_from_arguments = {}
        for (key, value) in kwargs.items():
            values_from_arguments[key] = value
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
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

