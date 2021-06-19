"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementConstraint

def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "true"
    sc.repeatable = "TRUE"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is True
    assert sc.repeatable is True


def test_mandatory_and_repeatable_are_true_given_numerical_boolean_values():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "1"
    sc.repeatable = "1"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is True
    assert sc.repeatable is True


def test_mandatory_and_repeatable_default_to_none():
    """The Boolean elements default to None if no value is declared."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is None
    assert sc.repeatable is None

