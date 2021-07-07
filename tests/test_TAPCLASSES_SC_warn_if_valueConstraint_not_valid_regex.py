"""Tests for private functions called by TAPStatementConstraint.validate()."""

import pytest
from dctap.tapclasses import TAPStatementConstraint


def test_valueConstraintType_pattern_is_valid_regex():
    """For valueConstraintType pattern, valueConstraint must be valid regex."""
    sc = TAPStatementConstraint()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc.valueConstraint = "approved_*"
    sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
    assert sc.valueConstraint
    sc.valueConstraint = "/approved_*/"
    sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
    assert sc.valueConstraint == "/approved_*/"
    sc.valueConstraint = "^2020 August"
    sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
    assert sc.valueConstraint
    sc.valueConstraint = "'confidential'"
    sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
    assert sc.valueConstraint == "'confidential'"


def test_valueConstraintType_pattern_warn_if_not_valid_regex():
    """For valueConstraintType pattern, warns if valueConstraint not valid regex."""
    sc = TAPStatementConstraint()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc.valueConstraint="approved_(*"
    sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
    assert len(sc.sc_warnings) == 1


