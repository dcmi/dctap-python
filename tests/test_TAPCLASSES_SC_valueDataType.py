"""Tests for private functions called by TAPStatementConstraint.normalize()."""

import pytest
from dctap.tapclasses import TAPStatementConstraint


def test_warn_if_valueDataType_literal_used_with_valueShape():
    sc = TAPStatementConstraint()
    sc.propertyID = ":status"
    sc.valueDataType = "Literal"
    sc.valueShape = "Person"
    sc._valueDataType_warn_if_literal_used_with_any_valueShape()
    assert len(sc.sc_warnings) == 1
