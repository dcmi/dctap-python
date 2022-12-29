"""config.config_defaults - a decorator for passing defaults to get_config."""

import os
import pytest
from pathlib import Path
from dctap.config import config_defaults



def test_config_defaults():
    """Decorator passes arguments correctly when function called without arguments."""
    @config_defaults(
        shape_class="TAP shape",
        state_class="TAP statement template",
        configfile1="dctap.yaml",
        configfile2=".dctaprc",
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile1=None,
        configfile2=None,
        yamldoc=None,
    ):
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile1"] = configfile1
        values_from_arguments["configfile2"] = configfile2
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()

    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile1"] == "dctap.yaml"
    assert actual_values["configfile2"] == ".dctaprc"
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
        configfile1=C,
        configfile2=D,
        yamldoc=E
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile1=None,
        configfile2=None,
        yamldoc=None,
    ):
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile1"] = configfile1
        values_from_arguments["configfile2"] = configfile2
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()

    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile1"] == "dctap.yaml"
    assert actual_values["configfile2"] == ".dctaprc"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_config_defaults_where_some_arguments_override_defaults():
    """Decorated function called with keyword variables that override defaults."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        shape_class=A,
        state_class=B,
        configfile1=C,
        configfile2=D,
        yamldoc=E
    )
    def func_to_be_decorated(
        shape_class=None,
        state_class=None,
        configfile1=None,
        configfile2=None,
        yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    ):
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile1"] = configfile1
        values_from_arguments["configfile2"] = configfile2
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()

    assert actual_values["shape_class"] == "TAP shape"
    assert actual_values["state_class"] == "TAP statement template"
    assert actual_values["configfile1"] == "dctap.yaml"
    assert actual_values["configfile2"] == ".dctaprc"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


