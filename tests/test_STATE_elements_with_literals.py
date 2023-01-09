"""
Tests TAPStatementTemplate._valueDataType_warn_if_used_with_valueNodeType_IRI

Values must be literals (strings) if they have a value datatype.
- If found not to be literals, records warning in sc.state_warns.
"""

import pytest
from dctap.tapclasses import TAPStatementTemplate, TAPShape

def test_warn_if_propertyID_not_URI():
    """Values of propertyID should be IRI-like."""
    sc = TAPStatementTemplate()
    sc.valueNodeType = node_type = "iri"
    sc.valueDataType = data_type = "xsd:integer"
    sc._valueDataType_warn_if_used_with_valueNodeType_IRI()
    assert len(dict(sc.state_warns)) == 1
    warning = f"Datatype '{data_type}' incompatible with node type '{node_type}'."
    assert sc.state_warns["valueDataType"] == warning

