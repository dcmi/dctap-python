"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPStatementConstraint

def test_warn_if_propertyID_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "P31"
    sc._warn_if_propertyID_valueShape_valueDataType_not_IRIs()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    assert len(dict(sc.sc_warnings)) == 1


def test_warn_if_valueShape_not_URI():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.valueShape = "Person"
    sc._warn_if_propertyID_valueShape_valueDataType_not_IRIs()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    assert len(dict(sc.sc_warnings)) == 1


def test_mandatory_and_repeatable_raise_warnings_given_unsupported_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    print(f"Instance: {sc}")
    print(f"Statement warnings at start of test: {sc.sc_warnings}")
    sc.propertyID = "dc:creator"
    sc.mandatory = "WAHR"
    sc.repeatable = "WAHR"
    sc._mandatory_and_repeatable_have_supported_boolean_value()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    print(f"Mandatory: {sc.mandatory}")
    print(f"Repeatable: {sc.repeatable}")
    assert len(sc.sc_warnings) == 2
    assert sc.mandatory is "WAHR"
    assert sc.repeatable is "WAHR"
