"""
Tests whether values of following properties are 'IRI-like':
- propertyID
- valueDataType 
- valueConstraint (when valueConstraintType is 'IRIstem')
- If found not to be IRI-like, records warning in sc.state_warns.
"""

from dctap.tapclasses import TAPStatementTemplate

def test_warn_if_propertyID_not_URI():
    """Values of propertyID should be IRI-like."""
    sc = TAPStatementTemplate()
    sc.propertyID = "P31"
    sc._warn_if_propertyID_not_IRIlike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1


def test_warn_if_valueDataType_not_URI():
    """Values of valueDataType should be IRI-like."""
    sc = TAPStatementTemplate()
    sc.propertyID = "wdt:P31"
    sc.valueDataType = "date"
    sc._warn_if_valueDataType_not_IRIlike()
    print(sc.state_warns)
    print(dict(sc.state_warns))
    print(len(dict(sc.state_warns)))
    assert len(dict(sc.state_warns)) == 1
