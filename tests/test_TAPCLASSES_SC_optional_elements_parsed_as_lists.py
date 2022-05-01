"""Tests for private functions called by TAPStatementConstraint.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementConstraint
from dctap.csvreader import csvreader

config_dict = get_config()
config_dict["elements_parsed_as_lists"] = [
    "propertyID", 
    "valueNodeType", 
    "valueDataType", 
    "valueShape",
]

def test_elements_parsed_as_lists():
    """Elements enumerated in config settings are parsed as lists."""
    sc = TAPStatementConstraint()
    sc.propertyID = "dcterms:creator"
    sc.valueNodeType = "iri bnode"
    sc.valueDataType = "xsd:date xsd:time"
    sc.valueShape = "a b c d"
    sc._parse_elements_listed_in_configfile_as_lists(config_dict)
    assert sc.propertyID == ["dcterms:creator"]
    assert sc.valueNodeType == ["iri", "bnode"]
    assert sc.valueDataType == ["xsd:date", "xsd:time"]
    assert sc.valueShape == ["a", "b", "c", "d"]

@pytest.mark.skip
def test_value_node_type_not_parsed_as_list():
    """Value Node Type not parsed as list - should raise error if not configured."""
    config_dict = get_config()
    sc = TAPStatementConstraint()
    sc.valueNodeType = "iri bnode"
    sc._parse_elements_listed_in_configfile_as_lists(config_dict)
    assert sc.valueNodeType == ["iri", "bnode"]
