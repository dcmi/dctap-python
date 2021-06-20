"""Tests for private functions called by TAPStatementConstraint.validate()."""

import pytest
from dctap.tapclasses import TAPStatementConstraint


def test_valueConstraintType_picklist_parse():
    """If valueConstraintType picklist, valueConstraint parsed on whitespace."""
    sc = TAPStatementConstraint()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "picklist"
    sc.valueConstraint = "one two three"
    sc._valueConstraintType_picklist_parse()
    assert sc.valueConstraint == ["one", "two", "three"]


def test_valueConstraintType_picklist_parse_case_insensitive():
    """Value constraint types are processed as case-insensitive."""
    sc = TAPStatementConstraint()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "PICKLIST"
    sc.valueConstraint = "one two          three" # extra whitespace
    sc._valueConstraintType_picklist_parse()
    assert sc.valueConstraint == ["one", "two", "three"]


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


def test_valueConstraintType_warn_if_used_without_valueConstraint():
    sc = TAPStatementConstraint()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc._valueConstraintType_warn_if_used_without_valueConstraint()
    assert len(sc.sc_warnings) == 1
