"""Test for elements mandatory and repeatable."""

import pytest
from textwrap import dedent
from dctap.config import get_config
from dctap.tapclasses import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_tapshapes


def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "true"
    sc.repeatable = "TRUE"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory is "true"
    assert sc.repeatable is "true"

def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "1"
    sc.repeatable = "0"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory is "true"
    assert sc.repeatable is "false"

def test_mandatory_and_repeatable_default_to_empty_strings():
    """The Boolean elements remain empty strings if no value is declared."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory == ""
    assert sc.repeatable == ""

def test_mandatory_and_repeatable_raise_warn_unsupported_boolean_values():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "dc:creator"
    sc.mandatory = "WAHR"
    sc.repeatable = "WAHR"
    sc._normalize_booleans_mandatory_repeatable()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    print(f"Mandatory: {sc.mandatory}")
    print(f"Repeatable: {sc.repeatable}")
    assert len(sc.sc_warnings) == 2
    assert sc.mandatory is "WAHR"
    assert sc.repeatable is "WAHR"
