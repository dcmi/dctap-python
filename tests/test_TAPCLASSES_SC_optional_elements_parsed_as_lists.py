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
    """Elements are parsed as lists - as so configured."""
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
