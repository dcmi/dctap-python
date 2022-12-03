"""
Tests for
- TAPStatementTemplate._valueConstraintType_minmaxlength_parse
- Called by sc.normalize()
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()

def test_valueConstraintType_minmaxlength_parse_must_be_integer():
    """valueConstraint minLength / maxLength must be integer."""

    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == 4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == 4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...


def test_valueConstraintType_minmaxlength_parse_must_not_be_float():
    """If valueConstraint minLength / maxLength is float, passed through as string."""

    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minmaxlength_parse_must_not_be_string():
    """If minLength / maxLength is non-numeric string, passed through untouched."""

    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minlength_parse_integer_may_be_negative_edge_case():
    """Edge case: minLength as negative integer. Test for this and issue warning?"""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "-4"
    sc._valueConstraintType_minmaxlength_parse()
    assert sc.valueConstraint == -4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...
