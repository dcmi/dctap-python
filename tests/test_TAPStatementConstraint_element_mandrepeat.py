"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementConstraint

def test_mandatory_and_repeatable_are_true_given_supported_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "true"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is True
    assert sc.repeatable is None


def test_mandatory_and_repeatable_are_true_given_uppercase_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "TRUE"
    sc.repeatable = "TRUE"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is True
    assert sc.repeatable is True


def test_mandatory_and_repeatable_are_true_given_numerical_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "1"
    sc.repeatable = "1"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is True
    assert sc.repeatable is True


def test_mandatory_and_repeatable_raise_warnings_given_unsupported_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "WAHR"
    sc.repeatable = "WAHR"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert len(sc.statement_warnings) == 2
    assert sc.mandatory is None
    assert sc.repeatable is None


def test_mandatory_and_repeatable_are_none_in_absence_of_any_declared_value():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    assert sc.mandatory is None
    assert sc.repeatable is None

