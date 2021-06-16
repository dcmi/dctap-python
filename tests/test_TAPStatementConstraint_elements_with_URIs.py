"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementConstraint

def test_warn_if_propertyID_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "P31"
    sc._warn_if_propertyID_and_valueShape_are_not_IRIs()
    print(sc.statement_warnings)
    print(dict(sc.statement_warnings))
    print(len(dict(sc.statement_warnings)))
    assert len(dict(sc.statement_warnings)) == 1


def test_warn_if_shapeID_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "P31"
    sc.valueShape = "Person"
    sc._warn_if_propertyID_and_valueShape_are_not_IRIs()
    print(sc.statement_warnings)
    print(dict(sc.statement_warnings))
    print(len(dict(sc.statement_warnings)))
    assert len(dict(sc.statement_warnings)) == 2

