"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

# pylint: disable=redefined-outer-name
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
    st = TAPStatementTemplate()
    st.propertyID = "dcterms:creator,dcterms:date"
    st._parse_elements_configured_as_picklist_elements(config_dict)
    assert st.propertyID == ["dcterms:creator", "dcterms:date"]

def test_picklist_elements():
    """Elements enumerated in config settings are parsed as lists."""
    config_dict["picklist_item_separator"] = " "
    st = TAPStatementTemplate()
    st.propertyID = "dcterms:creator dcterms:date"
    st.valueNodeType = "iri bnode"
    st.valueDataType = "xsd:date xsd:time"
    st.valueShape = "a b c d"
    st._parse_elements_configured_as_picklist_elements(config_dict)
    assert st.propertyID == ["dcterms:creator", "dcterms:date"]
    assert st.valueNodeType == ["iri", "bnode"]
    assert st.valueDataType == ["xsd:date", "xsd:time"]
    assert st.valueShape == ["a", "b", "c", "d"]

def test_picklist_elements_single_space_is_default():
    """Space is default list item separator."""
    st = TAPStatementTemplate()
    st.propertyID = "dcterms:creator dcterms:date"
    st.valueNodeType = "iri bnode"
    st.valueDataType = "xsd:date xsd:time"
    st.valueShape = "a b c d"
    st._parse_elements_configured_as_picklist_elements(config_dict)
    assert st.propertyID == ["dcterms:creator", "dcterms:date"]
    assert st.valueNodeType == ["iri", "bnode"]
    assert st.valueDataType == ["xsd:date", "xsd:time"]
    assert st.valueShape == ["a", "b", "c", "d"]

def test_value_node_type_not_parsed_as_list():
    """When element not configured to be parsed as list, just pass through."""
    config_dict["picklist_elements"] = []
    st = TAPStatementTemplate()
    st.valueNodeType = "iri bnode"
    st._parse_elements_configured_as_picklist_elements(config_dict)
    assert st.valueNodeType == "iri bnode"

def test_picklist_item_separator_defaults_to_single_blank():
    """Setting picklist_item_separator of None defaults to single blank."""
    st = TAPStatementTemplate()
    config_dict = get_config()
    config_dict["picklist_elements"] = ["valueNodeType"]
    config_dict["picklist_item_separator"] = None
    st.valueNodeType = "iri bnode"
    st._parse_elements_configured_as_picklist_elements(config_dict)
    assert st.valueNodeType == ["iri", "bnode"]
