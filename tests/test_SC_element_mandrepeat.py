"""Test for elements mandatory and repeatable."""

from textwrap import dedent
from dctap.tapclasses import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_tapshapes


def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "true"
    sc.repeatable = "TRUE"
    sc._mandatory_repeatable_have_supported_boolean_values()
    assert sc.mandatory is True
    assert sc.repeatable is True


def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "1"
    sc.repeatable = "0"
    sc._mandatory_repeatable_have_supported_boolean_values()
    assert sc.mandatory is True
    assert sc.repeatable is False


def test_mandatory_and_repeatable_default_to_none():
    """The Boolean elements default to None if no value is declared."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc._mandatory_repeatable_have_supported_boolean_values()
    assert sc.mandatory is None
    assert sc.repeatable is None


def test_booleans_shown_as_True_False_in_text_display():
    """Booleans display in text output as "True" and "False"."""
    some_input = {'shapes': [{'sh_warnings': {},
             'shapeID': ':default',
             'shapeLabel': '',
             'statement_constraints': [{'mandatory': 1,
                                        'note': '',
                                        'propertyID': ':creator',
                                        'propertyLabel': '',
                                        'repeatable': 0,
                                        'sc_warnings': {},
                                        'valueConstraint': '',
                                        'valueConstraintType': '',
                                        'valueDataType': '',
                                        'valueNodeType': '',
                                        'valueShape': ''}]}]}
    expected_output_dedented = dedent(
        """\
    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :creator
                mandatory:           True
                repeatable:          False
    """
    )
    assert pprint_tapshapes(some_input) == expected_output_dedented.splitlines()

def test_mandatory_and_repeatable_raise_warnings_given_unsupported_boolean_value():
    """@@@"""
    sc = TAPStatementConstraint()
    print(f"Instance: {sc}")
    print(f"Statement warnings at start of test: {sc.sc_warnings}")
    sc.propertyID = "dc:creator"
    sc.mandatory = "WAHR"
    sc.repeatable = "WAHR"
    sc._mandatory_repeatable_have_supported_boolean_values()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    print(f"Mandatory: {sc.mandatory}")
    print(f"Repeatable: {sc.repeatable}")
    assert len(sc.sc_warnings) == 2
    assert sc.mandatory is "WAHR"
    assert sc.repeatable is "WAHR"
