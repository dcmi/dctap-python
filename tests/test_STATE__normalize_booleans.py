"""Test for elements mandatory and repeatable."""

import pytest
from textwrap import dedent
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.inspect import pprint_tapshapes

def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementTemplate()
    sc.mandatory = "true"
    sc.repeatable = "FALSE"
    sc._normalize_booleans()
    assert sc.mandatory is "true"
    assert sc.repeatable is "false"

def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementTemplate()
    sc.mandatory = "1"
    sc.repeatable = "0"
    sc._normalize_booleans()
    assert sc.mandatory is "true"
    assert sc.repeatable is "false"

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
    sc.repeatable = "WAHR"
    sc._normalize_booleans()
    assert len(sc.state_warns) == 2
    assert sc.mandatory is "WAHR"
    assert sc.repeatable is "WAHR"
