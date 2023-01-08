"""Test for elements mandatory and repeatable."""

from textwrap import dedent
import pytest
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.inspect import pprint_tapshapes

def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementTemplate()
    sc.mandatory = "true"
    sc.repeatable = "FALSE"
    sc._normalize_booleans()
    assert sc.mandatory == "true"
    assert sc.repeatable == "false"

def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementTemplate()
    sc.mandatory = "1"
    sc.repeatable = "0"
    sc._normalize_booleans()
    assert sc.mandatory == "true"
    assert sc.repeatable == "false"

def test_mandatory_and_repeatable_default_to_empty_strings():
    """The Boolean elements remain empty strings if no value is declared."""
    sc = TAPStatementTemplate()
    sc._normalize_booleans()
    assert sc.mandatory == ""
    assert sc.repeatable == ""

def test_mandatory_and_repeatable_raise_warn_unsupported_boolean_values():
    """Warn about unsupported Boolean values."""
    sc = TAPStatementTemplate()
    sc.mandatory = "WAHR"
    sc.repeatable = "FALSCH"
    sc._normalize_booleans()
    assert len(sc.state_warns) == 2
    assert sc.mandatory == "WAHR"
    assert sc.repeatable == "FALSCH"
    assert sc.state_warns 
    warning_for_true = "'WAHR' is not a supported Boolean value."
    warning_for_false = "'FALSCH' is not a supported Boolean value."
