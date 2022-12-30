"""config.config_defaults - a decorator for passing defaults to get_config."""

import os
import pytest
from pathlib import Path
from dctap.config import config_defaults

def dctap_defaults(shape_class=None, state_class=None, configfile=None, yamldoc=None):
    """Return dict of keyword arguments for passing to get_config()."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs["shape_class"] = kwargs.get("shape_class", shape_class)
            kwargs["state_class"] = kwargs.get("state_class", state_class)
            kwargs["configfile"] = kwargs.get("configfile", configfile)
            kwargs["yamldoc"] = kwargs.get("yamldoc", yamldoc)
            return func(*args, **kwargs)
        return wrapper
    return decorator



def test_config_defaults_decorator_need_not_pass_all_required_arguments():
    """Decorator need only pass args required (extra args raised exception!)."""
    @config_defaults(
        shape_class="TAPShape",
        state_class="TAPStatementTemplate",
        configfile="dctap.yaml",
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["shape_class"] == "TAPShape"
    assert actual_values["state_class"] == "TAPStatementTemplate"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == None


def test_config_defaults():
    """Decorator passes arguments correctly when function called without arguments."""
    @config_defaults(
        shape_class="TAP shape",
        state_class="TAP statement template",
        configfile="dctap.yaml",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_config_defaults_when_passed_constants():
    """Confirm that decorator can read constants and variables from global scope."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        shape_class=A,
        state_class=B,
        configfile=C,
        yamldoc=E
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile=None,
        yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["shape_class"] == "TAP shape"
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
        shape_class=A,
        state_class=B,
        configfile=C,
        yamldoc=E
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile=None,
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_when_keyword_arguments_dict_passed_as_kwargs():
    """Args from decorator collect in dict "kwargs" - irrelevant but interesting."""
    @config_defaults(
        shape_class="TAP shape",
        state_class="TAP statement template",
        configfile="dctap.yaml",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(**kwargs):
        """Arguments passed from decorator to function, collected in dict, returned."""
        return kwargs

    actual_values = func_to_be_decorated()
    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""
