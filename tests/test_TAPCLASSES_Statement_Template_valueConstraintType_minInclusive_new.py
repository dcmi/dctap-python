"""
Tests for TAPStatementTemplate._mininclusive_parse / _maxinclusive_parse
- Called by sc.normalize().

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

def test_valueConstraintType_mininclusive_parse():
    """
    If valueConstraintType is minInclusive:
    - value of valueConstraint must be numeric
    - value of valueConstraint must be greater than, or equal to, given value
    See: https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
    """
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "4.0"
    sc._valueConstraintType_mininclusive_parse()
    assert sc.valueConstraint == 4.0
    assert str(sc.valueConstraint) != str(4)
    sc._valueConstraintType_mininclusive_warn_if_value_not_numeric()
    assert not sc.state_warns                         # Here: no warnings at all, but
    assert not sc.state_warns.get("valueConstraint")  # specifically, no warnings for...

def test_valueConstraintType_mininclusive_parse_also_floats():
    """Value of valueConstraint greater than, or equal to, given float."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "4.123"
    sc._valueConstraintType_mininclusive_parse()
    assert sc.valueConstraint == 4.123
    assert not sc.state_warns.get("valueConstraint")

def test_valueConstraintType_mininclusive_parse_also_floats_not():
    """Value of valueConstraint does not coerce to a float."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:date"
    sc.valueConstraintType = "mininclusive"
    sc.valueConstraint = "tom@tombaker.org"
    sc._valueConstraintType_mininclusive_parse()
    assert sc.valueConstraint == "tom@tombaker.org"
    sc._valueConstraintType_mininclusive_warn_if_value_not_numeric()
    assert sc.state_warns.get("valueConstraint")
    assert "tom@" in sc.state_warns.get("valueConstraint")

# def test_exit_with_ConfigError_if_configfile_specified_but_not_found(tmp_path):
#     """Exit with ConfigError if config file specified as argument is not found."""
#     os.chdir(tmp_path)
#     with pytest.raises(ConfigError):
#         get_config(configfile_name="dctap.yaml")
