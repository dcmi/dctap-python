"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
from dctap.defaults import dctap_defaults
from dctap.tapclasses import TAPShape, TAPStatementTemplate

def test_dctap_defaults_decorator_defines_default_arguments():
    """Default argument values are hard-wired into the decorator itself."""
    @dctap_defaults()
    def some_func(hardwired_shapeclass=None, state_class=None, configfile=None, yamldoc=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["hardwired_shapeclass"] == TAPShape
    assert actual_values["state_class"] == TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"]


def test_decorated_function_cannot_be_called_with_args_that_override_decorator():
    """Decorated function cannot be called with args that override decorator."""
    @dctap_defaults()
    def some_func(hardwired_shapeclass=None, state_class=None, configfile=None, yamldoc=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = some_func(yamldoc="QUUX")
    assert actual_values["yamldoc"] != "QUUX"


##############################
# Reference
##############################

def config_defaults(hardwired_shapeclass=None, state_class=None, configfile=None, yamldoc=None):
    """Return dict of keyword arguments for passing to get_config()."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs["hardwired_shapeclass"] = kwargs.get("hardwired_shapeclass", hardwired_shapeclass)
            kwargs["state_class"] = kwargs.get("state_class", state_class)
            kwargs["configfile"] = kwargs.get("configfile", configfile)
            kwargs["yamldoc"] = kwargs.get("yamldoc", yamldoc)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def test_config_defaults_decorator_need_not_pass_all_required_arguments():
    """Decorator need only pass args required (extra args raised exception!)."""
    @config_defaults(
        hardwired_shapeclass="TAPShape",
        state_class="TAPStatementTemplate",
        configfile="dctap.yaml",
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAPShape"
    assert actual_values["state_class"] == "TAPStatementTemplate"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == None


def test_config_defaults():
    """Decorator passes arguments correctly when function called without arguments."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        state_class="TAP statement template",
        configfile="dctap.yaml",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_config_defaults_when_passed_constants():
    """Decorator can access constants and variables from global scope."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        hardwired_shapeclass=A,
        state_class=B,
        configfile=C,
        yamldoc=E
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_config_defaults_where_some_arguments_override_defaults():
    """Decorated function called with keyword arguments that override defaults."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        hardwired_shapeclass=A,
        state_class=B,
        configfile=C,
        yamldoc=E
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        state_class=None,
        configfile=None,
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_when_keyword_arguments_dict_passed_as_kwargs():
    """Args from decorator collect in dict "kwargs" - irrelevant but interesting."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        state_class="TAP statement template",
        configfile="dctap.yaml",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(**kwargs):
        """Arguments passed from decorator to function, collected in dict, returned."""
        return kwargs

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_config_defaults_decorator_needs_not_support_all_args_of_decorated_function():
    """Functions can have args not passed by decorator."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        state_class="TAP statement template",
        configfile="dctap.yaml",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def some_func(
        hardwired_shapeclass=None, 
        state_class=None, 
        configfile=None, 
        yamldoc=None,
        foobar="ARGUMENT UNSUPPORTED BY DECORATOR",
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""
    assert actual_values["foobar"] == "ARGUMENT UNSUPPORTED BY DECORATOR"

def test_dctap_defaults_function_must_support_all_args_passed_by_decorator(capsys):
    """Decorated function must support all arguments passed by decorator."""
    @config_defaults()
    def some_func(
        hardwired_shapeclass=None, 
        state_class=None, 
        configfile=None, 
        yamlfile=None,
        foobar="ARGUMENT UNSUPPORTED BY DECORATOR",
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    with pytest.raises(TypeError) as te:
        actual_values = some_func()
        assert str(te.value) == "TypeError: some_func() got unexpected kwarg from @dctap_defaults"

