"""Tests for private functions called by TAPStatementConstraint.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementConstraint
from dctap.csvreader import csvreader

config_dict = get_config()
config_dict["picklist_elements"] = [
    "propertyID", 
    "valueNodeType", 
    "valueDataType", 
    "valueShape",
]

def test_picklist_elements():
    """Elements enumerated in config settings are parsed as lists."""
    sc = TAPStatementConstraint()
    sc.propertyID = "dcterms:creator"
    sc.valueNodeType = "iri bnode"
    sc.valueDataType = "xsd:date xsd:time"
    sc.valueShape = "a b c d"
    sc._parse_elements_listed_in_configfile_as_picklists(config_dict)
    assert sc.propertyID == ["dcterms:creator"]
    assert sc.valueNodeType == ["iri", "bnode"]
    assert sc.valueDataType == ["xsd:date", "xsd:time"]
    assert sc.valueShape == ["a", "b", "c", "d"]

def test_value_node_type_not_parsed_as_list():
    """When element not configured to be parsed as list, just pass through."""
    config_dict["picklist_elements"] = []
    sc = TAPStatementConstraint()
    sc.valueNodeType = "iri bnode"
    sc._parse_elements_listed_in_configfile_as_picklists(config_dict)
    assert sc.valueNodeType == "iri bnode"

def test_picklist_item_separator_defaults_to_single_blank():
    """Setting picklist_item_separator of None defaults to single blank."""
    sc = TAPStatementConstraint()
    config_dict = get_config()
    config_dict["picklist_elements"] = [ "valueNodeType" ]
    config_dict["picklist_item_separator"] = None
    sc.valueNodeType = "iri bnode"
    sc._parse_elements_listed_in_configfile_as_picklists(config_dict)
    assert sc.valueNodeType == ["iri", "bnode"]
    
