"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import pytest
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate

def test_warn_if_valueNodeType_literal_used_with_any_value_shape():
    """If valueNodeType is literal, valueShape should be empty."""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueNodeType = "literal"
    sc.valueShape = "Person"
    sc._valueNodeType_warn_if_valueNodeType_literal_used_with_any_valueShape()
    assert len(sc.state_warns) == 1
    warning = "Values of node type 'literal' cannot conform to value shapes."
    assert sc.state_warns["valueDataType"] == warning

def test_warn_if_valueConstraintType_pattern_used_with_any_value_shape():
    """Regular expressions cannot conform to value shapes."""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueConstraintType = "pattern"
    sc.valueShape = "Person"
    sc._valueConstraintType_pattern_warn_if_used_with_value_shape()
    assert len(sc.state_warns) == 1
    warning = "Values of constraint type 'pattern' cannot conform to a value shape."
    assert sc.state_warns["valueConstraintType"] == warning

def test_warn_if_valueDataType_used_with_any_value_shape():
    """Value with datatypes are literal, so cannot conform to a value shape."""
    sc = TAPStatementTemplate()
    sc.propertyID = ":status"
    sc.valueDataType = "xsd:date"
    sc.valueShape = "Person"
    sc._valueDataType_warn_if_used_with_valueShape()
    assert len(sc.state_warns) == 1
    warning = "Values with datatypes are literals cannot conform to value shapes."
    assert sc.state_warns["valueDataType"] == warning

def test_extra_value_node_types():
    """Extra value node types."""
    st = TAPStatementTemplate()
    nondefault_configyaml_str = """
    extra_value_node_types:
    - uri
    - nonliteral
    - IRIOrLiteral
    """
    config_dict = get_config(nondefault_configyaml_str=nondefault_configyaml_str)
    st._valueNodeType_is_from_enumerated_list(config_dict)
