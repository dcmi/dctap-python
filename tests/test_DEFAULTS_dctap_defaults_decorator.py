"""defaults.dctap_defaults - a decorator for passing package defaults"""

import os
import pytest
from functools import wraps
from pathlib import Path
import dctap
from dctap.defaults import dctap_defaults
from dctap.exceptions import ConfigError, DecoratorError


def test_decorator_default_classes_plus_default_configfile_passed_to_kwargs():
    """Function call reads arguments named in signature, captures rest in **kwargs."""

    @dctap_defaults()
    def some_func(config_filename=None, config_yamldoc=None, **kwargs):
        # How expected kwargs would normally be captured for use in function.
        # Need only capture variables actually needed.
        shapeclass = kwargs["shapeclass"]
        stateclass = kwargs["stateclass"]
        configfile = kwargs["configfile"]
        configyaml = kwargs["configyaml"]
        if config_filename and config_yamldoc:
            raise ConfigError("Cannot specify both config_filename and config_yamldoc.")

        # For the purpose of this test:
        values_passed_to_function = {}
        values_passed_to_function["config_filename"] = config_filename
        values_passed_to_function["config_yamldoc"] = config_yamldoc
        for (key, value) in kwargs.items():
            values_passed_to_function[key] = value
        return values_passed_to_function

    actual_values = some_func(config_filename="my_configfile.yaml")
    assert actual_values["shapeclass"] == dctap.tapclasses.TAPShape
    assert actual_values["stateclass"] == dctap.tapclasses.TAPStatementTemplate
    assert actual_values["configfile"] == dctap.defaults.CONFIGFILE
    assert actual_values["configyaml"] == dctap.defaults.CONFIGYAML
    assert actual_values["config_filename"] == "my_configfile.yaml"
    assert actual_values["config_yamldoc"] is None


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

    with pytest.raises(DecoratorError):
        actual_values = some_func(shapeclass="baz")
