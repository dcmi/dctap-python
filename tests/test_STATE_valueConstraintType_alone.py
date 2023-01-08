"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import pytest
from dctap.tapclasses import TAPStatementTemplate


def test_valueconstrainttype_warn_if_used_without_valueconstraint():
    """If valueConstraintType has value, but valueConstraint not, record a warning."""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc.valueConstraint = ""
    sc._valueConstraintType_warn_if_used_without_valueConstraint()
    warning = "Value constraint type 'pattern' has no corresponding value constraint."
    assert len(sc.state_warns) == 1
    assert sc.state_warns.get("valueConstraint") == warning
