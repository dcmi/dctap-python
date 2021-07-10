"""Test for elements mandatory and repeatable."""

import pytest
from textwrap import dedent
from dctap.config import get_config
from dctap.tapclasses import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_tapshapes


def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "true"
    sc.repeatable = "TRUE"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory is "True"
    assert sc.repeatable is "True"

def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc.mandatory = "1"
    sc.repeatable = "0"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory is "True"
    assert sc.repeatable is "False"

def test_mandatory_and_repeatable_default_to_none():
    """The Boolean elements default to None if no value is declared."""
    sc = TAPStatementConstraint()
    sc.propertyID = "wdt:P31"
    sc._normalize_booleans_mandatory_repeatable()
    assert sc.mandatory is None
    assert sc.repeatable is None

@pytest.mark.skip
def test_booleans_shown_as_True_False_in_text_display():
    """Booleans display in text output as "True" and "False"."""
    SHAPES_DICT = {'shapes': [{'sh_warnings': {},
             'shapeID': 'default',
             'shapeLabel': '',
             'statement_constraints': [{'mandatory': "True",
                                        'note': '',
                                        'propertyID': ':creator',
                                        'propertyLabel': '',
                                        'repeatable': "False",
                                        'sc_warnings': {},
                                        'valueConstraint': '',
                                        'valueConstraintType': '',
                                        'valueDataType': '',
                                        'valueNodeType': '',
                                        'valueShape': ''}]}]}
    expected_output_list = [
        "DCTAP instance",
        "    Shape",
        "        shapeID:                 default",
        "        Statement Constraint",
        "            propertyID:          :creator",
        "            mandatory:           True",
        "            repeatable:          False",
    ]
    SETTINGS_DICT = get_config()
    pprint_tapshapes_output = pprint_tapshapes(SHAPES_DICT, SETTINGS_DICT)
    assert(SETTINGS_DICT["extra_shape_elements"])
    assert "min" in SETTINGS_DICT["extra_statement_constraint_elements"]
    assert "max" in SETTINGS_DICT["extra_statement_constraint_elements"]
    assert len(expected_output_list) == 7
    assert type(expected_output_list) == list
    assert expected_output_list[0] == "DCTAP instance"
    assert type(pprint_tapshapes_output) == list
    assert len(pprint_tapshapes_output) == 7
    # assert pprint_tapshapes_output == expected_output_list

def test_mandatory_and_repeatable_raise_warn_unsupported_boolean_values():
    """@@@"""
    sc = TAPStatementConstraint()
    sc.propertyID = "dc:creator"
    sc.mandatory = "WAHR"
    sc.repeatable = "WAHR"
    sc._normalize_booleans_mandatory_repeatable()
    print(sc.sc_warnings)
    print(dict(sc.sc_warnings))
    print(len(dict(sc.sc_warnings)))
    print(f"Mandatory: {sc.mandatory}")
    print(f"Repeatable: {sc.repeatable}")
    assert len(sc.sc_warnings) == 2
    assert sc.mandatory is "WAHR"
    assert sc.repeatable is "WAHR"
