"""
Tests 
- TAPStatementTemplate._valueDataType_warn_if_used_with_valueNodeType_IRI
  Values must be literals (strings) if they have a value datatype.
  - If found not to be literals, records warning in sc.state_warns.

- TAPStatementTemplate._valueDataType_warn_if_used_with_valueShape
"""

import pytest
from dctap.tapclasses import TAPStatementTemplate, TAPShape

def test_warn_if_nodetype_iri_used_with_any_valuedatatype():
    """Node type IRI is incompatible with any (literal) value datatype."""
    sc = TAPStatementTemplate()
    sc.valueNodeType = node_type = "iri"
    sc.valueDataType = data_type = "xsd:integer"
    sc._valueDataType_warn_if_used_with_valueNodeType_IRI()
    assert len(dict(sc.state_warns)) == 1
    warning = f"Datatype '{data_type}' incompatible with node type '{node_type}'."
    assert sc.state_warns["valueDataType"] == warning

def test_warn_if_valueshape_used_with_any_valuedatatype(capsys):
    """Use of a value shape is incompatible with any (literal) value datatype."""
    sc = TAPStatementTemplate()
    sc.valueDataType = data_type = "xsd:integer"
    sc.valueShape = node_type = "my:UserShape"
    sc._valueDataType_warn_if_used_with_valueShape()
    assert len(dict(sc.state_warns)) == 1
    warning = "Values with datatypes (literals) cannot conform to value shapes."
    assert sc.state_warns["valueDataType"] == warning
    # with capsys.disabled():
    #     print()
    #     print(sc.state_warns)

def test_warn_if_valuedatatype_used_with_any_value_shape():
    """Value with datatypes are literal, so cannot conform to a value shape."""
    st = TAPStatementTemplate()
    st.propertyID = ":status"
    st.valueDataType = "xsd:date"
    st.valueShape = "Person"
    st._valueDataType_warn_if_used_with_valueShape()
    assert len(st.state_warns) == 1
    warning = "Values with datatypes (literals) cannot conform to value shapes."
    assert st.state_warns["valueDataType"] == warning
