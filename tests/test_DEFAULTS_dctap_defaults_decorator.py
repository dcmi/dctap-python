"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
import dctap
from dctap.defaults import dctap_defaults



##############################
# Reference
##############################

@pytest.mark.skip(reason="")
def test_config_defaults_decorator_need_not_pass_all_required_arguments():
    """Decorator need only pass args required (extra args raised exception!)."""
    @config_defaults(
        hardwired_shapeclass="TAPShape",
        hardwired_stateclass="TAPStatementTemplate",
        hardwired_configfile="dctap.yaml",
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        hardwired_stateclass=None,
        hardwired_configfile=None,
        hardwired_yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAPShape"
    assert actual_values["hardwired_stateclass"] == "TAPStatementTemplate"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == None


@pytest.mark.skip(reason="")
def test_config_defaults():
    """Decorator passes arguments correctly when function called without arguments."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        hardwired_stateclass="TAP statement template",
        hardwired_configfile="dctap.yaml",
        hardwired_yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        hardwired_stateclass=None,
        hardwired_configfile=None,
        hardwired_yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["hardwired_stateclass"] == "TAP statement template"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


@pytest.mark.skip(reason="")
def test_config_defaults_when_passed_constants():
    """Decorator can access constants and variables from global scope."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        hardwired_shapeclass=A,
        hardwired_stateclass=B,
        hardwired_configfile=C,
        hardwired_yamldoc=E
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        hardwired_stateclass=None,
        hardwired_configfile=None,
        hardwired_yamldoc=None,
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["hardwired_stateclass"] == "TAP statement template"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


@pytest.mark.skip(reason="")
def test_config_defaults_where_some_arguments_override_defaults():
    """Decorated function called with keyword arguments that override defaults."""
    A = "TAP shape"
    B = "TAP statement template"
    C = "dctap.yaml"
    D = ".dctaprc"
    E = """prefixes:\n "ex:": "http://example.org/"\n"""

    @config_defaults(
        hardwired_shapeclass=A,
        hardwired_stateclass=B,
        hardwired_configfile=C,
        hardwired_yamldoc=E
    )
    def func_to_be_decorated(
        hardwired_shapeclass=None,
        hardwired_stateclass=None,
        hardwired_configfile=None,
        hardwired_yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        return values_from_arguments

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["hardwired_stateclass"] == "TAP statement template"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


@pytest.mark.skip(reason="")
def test_when_keyword_arguments_dict_passed_as_kwargs():
    """Args from decorator collect in dict "kwargs" - irrelevant but interesting."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        hardwired_stateclass="TAP statement template",
        hardwired_configfile="dctap.yaml",
        hardwired_yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def func_to_be_decorated(**kwargs):
        """Arguments passed from decorator to function, collected in dict, returned."""
        return kwargs

    actual_values = func_to_be_decorated()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["hardwired_stateclass"] == "TAP statement template"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""


@pytest.mark.skip(reason="")
def test_config_defaults_decorator_needs_not_support_all_args_of_decorated_function():
    """Functions can have args not passed by decorator."""
    @config_defaults(
        hardwired_shapeclass="TAP shape",
        hardwired_stateclass="TAP statement template",
        hardwired_configfile="dctap.yaml",
        hardwired_yamldoc="""prefixes:\n "ex:": "http://example.org/"\n"""
    )
    def some_func(
        hardwired_shapeclass=None, 
        hardwired_stateclass=None, 
        hardwired_configfile=None, 
        hardwired_yamldoc=None,
        foobar="ARGUMENT UNSUPPORTED BY DECORATOR",
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    actual_values = some_func()
    assert actual_values["hardwired_shapeclass"] == "TAP shape"
    assert actual_values["hardwired_stateclass"] == "TAP statement template"
    assert actual_values["hardwired_configfile"] == "dctap.yaml"
    assert actual_values["hardwired_yamldoc"] == """prefixes:\n "ex:": "http://example.org/"\n"""
    assert actual_values["foobar"] == "ARGUMENT UNSUPPORTED BY DECORATOR"

@pytest.mark.skip(reason="")
def test_dctap_defaults_function_must_support_all_args_passed_by_decorator(capsys):
    """Decorated function must support all arguments passed by decorator."""
    @config_defaults()
    def some_func(
        hardwired_shapeclass=None, 
        hardwired_stateclass=None, 
        hardwired_configfile=None, 
        yamlfile=None,
        foobar="ARGUMENT UNSUPPORTED BY DECORATOR",
    ):
        """@@@"""
        values_from_arguments = {}
        values_from_arguments["hardwired_shapeclass"] = hardwired_shapeclass
        values_from_arguments["hardwired_stateclass"] = hardwired_stateclass
        values_from_arguments["hardwired_configfile"] = hardwired_configfile
        values_from_arguments["hardwired_yamldoc"] = hardwired_yamldoc
        values_from_arguments["foobar"] = foobar
        return values_from_arguments

    with pytest.raises(TypeError) as te:
        actual_values = some_func()
        assert str(te.value) == "TypeError: some_func() got unexpected kwarg from @dctap_defaults"


def test_decorator_default_classes_plus_default_configfile_passed_to_kwargs():
    """Decorator passes kwargs to function that (ideally) captures them in **kwargs."""
    @dctap_defaults()
    def some_func(foobar=None, **kwargs):
        values_from_arguments = {}
        if foobar:
            values_from_arguments["foobar"] = foobar
        for (key, value) in kwargs.items():
            values_from_arguments[key] = value
        return values_from_arguments

    actual_values = some_func(foobar="baz")
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
    assert actual_values["configfile"] == "dctap.yaml"
    assert actual_values["foobar"] == "baz"


def test_decorated_function_cannot_be_called_with_args_that_override_decorator():
    """
    Kwargs can be enumerated, not collected in **kwargs
    - but function can be called with keyword arguments that clash with decorator
    - decorator catches this and raises an error
    """
    @dctap_defaults()
    def some_func(shapeclass=None, stateclass=None, configfile=None, yamldoc=None):
        """Enumerates kwargs, not collecting them in **kwargs."""
        values_from_arguments = {}
        values_from_arguments["shapeclass"] = shapeclass
        values_from_arguments["stateclass"] = stateclass
        values_from_arguments["configfile"] = configfile
        values_from_arguments["yamldoc"] = yamldoc
        return values_from_arguments

    with pytest.raises(TypeError):
        actual_values = some_func(shapeclass="baz")

