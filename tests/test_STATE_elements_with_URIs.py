"""
Tests TAPStatementTemplate._warn_if_value_not_urilike
- Values of following properties should (or could) be 'IRI-like':
  - propertyID
  - valueDataType 
- If found not to be IRI-like, records warning in sc.state_warns.

Does not test:
- valueConstraint (when valueConstraintType is 'IRIstem')
"""

import pytest
from dctap.tapclasses import TAPStatementTemplate, TAPShape

def test_warn_if_propertyID_not_URI():
    """Values of propertyID should be IRI-like."""
    sc = TAPStatementTemplate()
    sc.propertyID = "P31"
    sc._warn_if_value_not_urilike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1

def test_warn_if_valueDataType_not_URI():
    """Values of valueDataType should be IRI-like."""
    sc = TAPStatementTemplate()
    sc.propertyID = "wdt:P31"
    sc.valueDataType = "date"
    sc._warn_if_value_not_urilike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1

def test_warn_if_shapeID_not_URI():
    """Values of shapeID should commonly be IRI-like."""
    sh = TAPShape()
    sh.shapeID = "FoodShape"
    sh._warn_if_value_not_urilike()
    print(sh.shape_warns)
    print(dict(sh.shape_warns))
    print(len(dict(sh.shape_warns)))
    assert len(dict(sh.shape_warns)) == 1
