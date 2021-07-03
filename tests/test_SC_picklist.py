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


