"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()
config_dict["picklist_elements"] = [
    "propertyID", 
    "valueNodeType", 
    "valueDataType", 
    "valueShape",
]

def test_picklist_elements_comma_separated():
    """Elements enumerated in config settings are parsed as lists."""
    config_dict["picklist_item_separator"] = ","
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator,dcterms:date"
    sc._parse_elements_configured_as_picklist_elements(config_dict)
    assert sc.propertyID == ["dcterms:creator", "dcterms:date"]

def test_picklist_elements():
    """Elements enumerated in config settings are parsed as lists."""
    config_dict["picklist_item_separator"] = " "
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator dcterms:date"
    sc.valueNodeType = "iri bnode"
    sc.valueDataType = "xsd:date xsd:time"
    sc.valueShape = "a b c d"
    sc._parse_elements_configured_as_picklist_elements(config_dict)
    assert sc.propertyID == ["dcterms:creator", "dcterms:date"]
    assert sc.valueNodeType == ["iri", "bnode"]
    assert sc.valueDataType == ["xsd:date", "xsd:time"]
    assert sc.valueShape == ["a", "b", "c", "d"]

def test_picklist_elements_single_space_is_default():
    """Space is default list item separator."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator dcterms:date"
    sc.valueNodeType = "iri bnode"
    sc.valueDataType = "xsd:date xsd:time"
    sc.valueShape = "a b c d"
    sc._parse_elements_configured_as_picklist_elements(config_dict)
    assert sc.propertyID == ["dcterms:creator", "dcterms:date"]
    assert sc.valueNodeType == ["iri", "bnode"]
    assert sc.valueDataType == ["xsd:date", "xsd:time"]
    assert sc.valueShape == ["a", "b", "c", "d"]

def test_value_node_type_not_parsed_as_list():
    """When element not configured to be parsed as list, just pass through."""
    config_dict["picklist_elements"] = []
    sc = TAPStatementTemplate()
    sc.valueNodeType = "iri bnode"
    sc._parse_elements_configured_as_picklist_elements(config_dict)
    assert sc.valueNodeType == "iri bnode"

def test_picklist_item_separator_defaults_to_single_blank():
    """Setting picklist_item_separator of None defaults to single blank."""
    sc = TAPStatementTemplate()
    config_dict = get_config()
    config_dict["picklist_elements"] = [ "valueNodeType" ]
    config_dict["picklist_item_separator"] = None
    sc.valueNodeType = "iri bnode"
    sc._parse_elements_configured_as_picklist_elements(config_dict)
    assert sc.valueNodeType == ["iri", "bnode"]
