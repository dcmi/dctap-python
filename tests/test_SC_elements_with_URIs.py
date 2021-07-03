"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementConstraint

def test_warn_if_propertyID_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "P31"
    sc._elements_taking_IRIs_warn_if_not_IRIs()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    assert len(dict(sc.sc_warnings)) == 1


def test_warn_if_valueShape_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.valueShape = "Person"
    sc._elements_taking_IRIs_warn_if_not_IRIs()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    assert len(dict(sc.sc_warnings)) == 1
