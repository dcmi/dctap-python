"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import pytest
from dctap.tapclasses import TAPStatementTemplate


def test_warn_if_valueNodeType_literal_used_with_any_value_shape():
    """@@@"""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueNodeType = "literal"
    sc.valueShape = "Person"
    sc._valueDataType_warn_if_valueNodeType_literal_used_with_any_valueShape()
    assert len(sc.state_warns) == 1

def test_warn_if_valueConstraintType_pattern_used_with_any_value_shape():
    """Regular expressions cannot conform to value shapes."""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc.valueShape = "Person"
    sc._valueConstraintType_pattern_warn_if_used_with_value_shape()
    assert len(sc.state_warns) == 1

def test_warn_if_valueDataType_used_with_any_value_shape():
    """@@@"""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueDataType = "xsd:date"
    sc.valueShape = "Person"
    sc._valueDataType_warn_if_used_with_valueShape()
    assert len(sc.state_warns) == 1

