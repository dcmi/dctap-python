"""
Tests for 
- TAPStatementTemplate._valueConstraintType_minmaxinclusive_parse
- Called by sc.normalize()

2022-09-21 definition: "A number to define lower and upper bounds of a numeric
value. 'Inclusive' means that the numbers listed will be included in the
bounds, i.e. '3-5' includes 3, 4, 5."
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()

def test_valueConstraintType_minmaxinclusive_parse():
    """If valueConstraintType minInclusive, valueConstraint must be numeric."""
    # minInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "4.0"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == 4.0
    assert str(sc.valueConstraint) != str(4)
    sc._valueConstraintType_minmaxinclusive_warn_if_value_not_numeric()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

    # maxInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "maxinclusive"
    sc.valueConstraint = "4.0"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == 4.0
    assert str(sc.valueConstraint) != str(4)
    sc._valueConstraintType_minmaxinclusive_warn_if_value_not_numeric()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...


def test_valueConstraintType_minmaxinclusive_parse_also_floats():
    """Value of valueConstraint greater than, or equal to, given float."""
    # minInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == 4.123
    assert not sc.state_warns.get("valueConstraint")

    # maxInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "maxinclusive"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == 4.123
    assert not sc.state_warns.get("valueConstraint")

def test_valueConstraintType_minmaxinclusive_parse_also_floats_not():
    """Value of valueConstraint does not coerce to a float."""
    # minInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxinclusive_warn_if_value_not_numeric()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

    # maxInclusive
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "maxinclusive"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_minmaxinclusive_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_minmaxinclusive_warn_if_value_not_numeric()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")
