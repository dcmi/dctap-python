"""
Tests for
- TAPStatementTemplate._valueConstraintType_minlength_parse
- TAPStatementTemplate._valueConstraintType_maxlength_parse
- Called by sc.normalize()
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()

def test_valueConstraintType_minlength_parse_must_be_integer():
    """valueConstraint minLength must be integer."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4"
    sc._valueConstraintType_minlength_parse()
    assert sc.valueConstraint == 4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

def test_valueConstraintType_minlength_parse_must_be_integer_actually_float():
    """
    Here: valueConstraint minLength not an integer, rather: a float.
    - Note: offending string is passed through.
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_minlength_parse()
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minlength_parse_must_be_integer_actually_string():
    """
    Here: valueConstraint minLength not an integer, rather: a string.
    - Note: offending string is passed through.
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

##########################
def test_valueConstraintType_minmaxlength_parse_must_be_integer():
    """valueConstraint maxLength must be integer."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4"
    sc._valueConstraintType_maxlength_parse()
    assert sc.valueConstraint == 4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

def test_valueConstraintType_maxlength_parse_must_be_integer_actually_float():
    """
    Here: valueConstraint maxLength not an integer, rather: a float.
    - Note: offending string is passed through.
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_maxlength_parse()
    assert sc.valueConstraint == "4.123"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

def test_valueConstraintType_maxlength_parse_must_be_integer_actually_string():
    """
    Here: valueConstraint maxLength not an integer, rather: a string.
    - Note: offending string is passed through.
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_maxlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minlength_parse_integer_may_be_negative():
    """
    valueConstraint minLength may be negative integer.
    2022-12-03: Seems like an edge case; tolerating for now.
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "-4"
    sc._valueConstraintType_minlength_parse()
    assert sc.valueConstraint == -4
    sc._valueConstraintType_minmaxlength_warn_if_not_integer()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

@pytest.mark.skip
def test_valueConstraintType_minlength_parse_also_floats_not():
    """Value of valueConstraint does not coerce to a float."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minlength_warn_if_value_not_numeric()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

@pytest.mark.skip
def test_valueConstraintType_maxlength_parse_also_floats():
    """Value of valueConstraint can be a float."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_maxlength_parse()
    assert sc.valueConstraint == 4.123
    assert not sc.state_warns.get("valueConstraint")

@pytest.mark.skip
def test_valueConstraintType_maxlength_parse_also_floats_not():
    """Value of valueConstraint does not coerce to a float."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dc:identifier"
    sc.valueConstraintType = "maxlength"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_maxlength_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_maxlength_warn_if_value_not_numeric()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")
