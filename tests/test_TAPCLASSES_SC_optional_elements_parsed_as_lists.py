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
    "propertyLabel", 
    "valueNodeType", 
    "valueDataType", 
    "valueShape",
    "note", 
]

def test_valueConstraintType_picklist_parse():
    """If valueConstraintType picklist, valueConstraint parsed on whitespace."""
    sc = TAPStatementConstraint()
    sc.propertyID = "dcterms:creator"
    sc.propertyLabel = "Author Writer"
    sc.valueNodeType = "iri bnode"
    sc.valueDataType = "xsd:date xsd:time"
    sc.valueShape = "a b c d"
    # sc.note = "'try this' 'try that'"
    sc._parse_elements_listed_in_configfile_as_lists(config_dict)
    assert sc.propertyID == ["dcterms:creator"]
    assert sc.propertyLabel == ["Author", "Writer"]
    assert sc.valueNodeType == ["iri", "bnode"]
    assert sc.valueDataType == ["xsd:date", "xsd:time"]
    assert sc.valueShape == ["a", "b", "c", "d"]
    # assert sc.note == ["try this", "try that"]

