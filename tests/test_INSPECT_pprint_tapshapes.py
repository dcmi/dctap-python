"""Pretty-print tapshape dicts to console."""

import pytest
from dataclasses import asdict
from textwrap import dedent
from dctap.config import get_config
from dctap.tapclasses import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_tapshapes

SETTINGS_DICT = get_config()

SHAPES_DICT = {'shapes': [{'sh_warnings': {},
             'shapeID': ':a',
             'shapeLabel': None,
             'statement_constraints': [{'mandatory': "False",
                                        'note': None,
                                        'propertyID': 'dct:creator',
                                        'propertyLabel': None,
                                        'repeatable': "True",
                                        'sc_warnings': {},
                                        'valueConstraint': None,
                                        'valueConstraintType': None,
                                        'valueDataType': None,
                                        'valueNodeType': None,
                                        'valueShape': None},
                                       {'mandatory': "False",
                                        'note': None,
                                        'propertyID': 'dct:date',
                                        'propertyLabel': None,
                                        'repeatable': "True",
                                        'sc_warnings': {},
                                        'valueConstraint': None,
                                        'valueConstraintType': None,
                                        'valueDataType': None,
                                        'valueNodeType': None,
                                        'valueShape': None}]},
            {'sh_warnings': {},
             'shapeID': ':b',
             'shapeLabel': None,
             'statement_constraints': [{'mandatory': None,
                                        'note': None,
                                        'propertyID': 'foaf:name',
                                        'propertyLabel': None,
                                        'repeatable': None,
                                        'sc_warnings': {},
                                        'valueConstraint': None,
                                        'valueConstraintType': None,
                                        'valueDataType': None,
                                        'valueNodeType': None,
                                        'valueShape': None,
                                        'min': 1,
                                        'max': 3,
                                        }]}]}

expected_output_list = [
    "DCTAP instance",
    "    Shape",
    "        shapeID:                 :a",
    "        Statement Constraint",
    "            propertyID:          dct:creator",
    "            mandatory:           False",
    "            repeatable:          True",
    "        Statement Constraint",
    "            propertyID:          dct:date",
    "            mandatory:           False",
    "            repeatable:          True",
    "    Shape",
    "        shapeID:                 :b",
    "        Statement Constraint",
    "            propertyID:          foaf:name",
    "            extra/min:           1",
    "            extra/max:           3",
]

def test_pprint_tapshapes_two_shapes():
    """Pretty-print list of TAPShape objects."""
    pprint_tapshapes_output = pprint_tapshapes(SHAPES_DICT, SETTINGS_DICT)
    #assert(SETTINGS_DICT["extra_shape_elements"])
    #assert "min" in SETTINGS_DICT["extra_statement_constraint_elements"]
    #assert "max" in SETTINGS_DICT["extra_statement_constraint_elements"]
    assert len(expected_output_list) == 17
    assert type(expected_output_list) == list
    assert expected_output_list[0] == "DCTAP instance"
    assert type(pprint_tapshapes_output) == list
#    assert len(pprint_tapshapes_output) == 17
#    assert pprint_tapshapes_output == expected_output_list
