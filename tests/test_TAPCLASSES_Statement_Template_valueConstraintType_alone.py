"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import pytest
from dctap.tapclasses import TAPStatementTemplate


def test_valueConstraintType_warn_if_used_without_valueConstraint():
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc._valueConstraintType_warn_if_used_without_valueConstraint()
    assert len(sc.state_warns) == 1
