"""
Tests for
- TAPStatementTemplate._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer
- Called by sc.normalize()
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

def test_valueConstraintType_minmaxlength_parse_must_be_integer():
    """valueConstraint minLength / maxLength must be integer."""
    config_dict = get_config()
    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4"
    assert sc.valueConstraint == "4"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.valueConstraint == 4
    assert not sc.state_warns  # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...
    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4"
    assert sc.valueConstraint == "4"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.valueConstraint == 4
    assert not sc.state_warns  # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

def test_valueConstraintType_minmaxlength_parse_must_not_be_float():
    """If valueConstraint minLength / maxLength is float, passed through as string."""
    config_dict = get_config()
    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4.123"
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.state_warns.get("valueConstraint")
    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4.123"
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minmaxlength_parse_must_not_be_string():
    """If minLength / maxLength is non-numeric string, passed through untouched."""
    config_dict = get_config()
    # minLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "tom@tombaker.org"
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")
    # maxLength
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "tom@tombaker.org"
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minlength_parse_integer_may_be_negative_edge_case():
    """If minLength is a negative integer, issues warning."""
    config_dict = get_config()
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "-4"
    assert sc.valueConstraint == "-4"
    sc._valueConstraintType_minmaxlength_warn_if_not_nonnegative_integer()
    assert sc.valueConstraint == -4
    assert sc.state_warns  # Here: there are warnings...
    assert sc.state_warns.get("valueConstraint")  # specifically, a warning for...
