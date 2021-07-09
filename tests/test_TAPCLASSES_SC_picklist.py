"""Tests for private functions called by TAPStatementConstraint.validate()."""

import pytest
from dctap.config import get_config
from dctap.tapclasses import TAPStatementConstraint

config_dict = get_config()

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

def test_valueConstraintType_picklist_item_separator_in_default_config():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.config_dict = config_dict
    assert sc.config_dict.get("picklist_item_separator")
    assert sc.config_dict.get("picklist_item_separator") == " "

def test_valueConstraintType_picklist_item_separator_comma():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.config_dict = config_dict
    sc.config_dict["picklist_item_separator"] = ","
    assert sc.config_dict.get("picklist_item_separator")
    assert sc.config_dict.get("picklist_item_separator") == ","
