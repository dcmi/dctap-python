"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import pytest
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate

def test_warn_if_valueNodeType_literal_used_with_any_value_shape():
    """If valueNodeType is literal, valueShape should be empty."""
    st = TAPStatementTemplate()
    st.propertyID = ":status"
    st.valueNodeType = "literal"
    st.valueShape = "Person"
    st._valueNodeType_warn_if_valueNodeType_literal_used_with_any_valueShape()
    assert len(st.state_warns) == 1
    warning = "Values of node type 'literal' cannot conform to value shapes."
    assert st.state_warns["valueDataType"] == warning

def test_warn_if_valueConstraintType_pattern_used_with_any_value_shape():
    """Regular expressions cannot conform to value shapes."""
    st = TAPStatementTemplate()
    st.propertyID = ":status"
    st.valueConstraintType = "pattern"
    st.valueShape = "Person"
    st._valueConstraintType_pattern_warn_if_used_with_value_shape()
    assert len(st.state_warns) == 1
    warning = "Values of constraint type 'pattern' cannot conform to a value shape."
    assert st.state_warns["valueConstraintType"] == warning

def test_warn_if_valueDataType_used_with_any_value_shape():
    """Value with datatypes are literal, so cannot conform to a value shape."""
    st = TAPStatementTemplate()
    st.propertyID = ":status"
    st.valueDataType = "xsd:date"
    st.valueShape = "Person"
    st._valueDataType_warn_if_used_with_valueShape()
    assert len(st.state_warns) == 1
    warning = "Values with datatypes (literals) cannot conform to value shapes."
    assert st.state_warns["valueDataType"] == warning

def test_extra_value_node_types():
    """Extra value node types."""
    nondefault_configyaml_str = """
    extra_value_node_types:
    - uri
    - nonliteral
    - IRIOrLiteral
    """
    config_dict = get_config(nondefault_configyaml_str=nondefault_configyaml_str)
    st = TAPStatementTemplate()
    st.valueNodeType = node_type = "LiteralOrIri"
    st._valueNodeType_is_from_enumerated_list(config_dict)
    assert len(st.state_warns) == 1
    warning = f"'{node_type}' is not a valid node type."
    assert st.state_warns["valueNodeType"] == warning
