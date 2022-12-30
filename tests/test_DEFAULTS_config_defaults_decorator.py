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
    def some_func(shape_class=None, state_class=None, configfile=None, yamldoc=None):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shape_class"] == TAPShape
    assert actual_values["state_class"] == TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


def test_decorator_needs_not_support_all_args_of_decorated_function():
    """Decorator needs not support all arguments of functions to be decorated."""
    @dctap_defaults()
    def some_func(
        shape_class=None, 
        state_class=None, 
        configfile=None, 
        yamldoc=None,
        foobar="ARGUMENT UNSUPPORTED BY DECORATOR",
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["shape_class"] == TAPShape
    assert actual_values["state_class"] == TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""
    assert actual_values["foobar"] == "ARGUMENT UNSUPPORTED BY DECORATOR"


def test_dctap_defaults_function_must_support_all_args_passed_by_decorator(capsys):
    """However, decorated function must support all arguments passed by decorator."""
    @dctap_defaults()
    def some_func(
        shape_class=None, 
        state_class=None, 
        configfile=None, 
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["shape_class"] = shape_class
        values_from_arguments["state_class"] = state_class
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    with pytest.raises(TypeError) as te:
        actual_values = some_func()
        assert str(te.value) == "TypeError: some_func() got unexpected kwarg from @dctap_defaults"
