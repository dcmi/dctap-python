"""Pretty-print tapshape dicts to console."""

import pytest
from dataclasses import asdict
from textwrap import dedent
from dctap.tapclasses import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_tapshapes


SHAPES_DICT = {'shapes': [{'sh_warnings': {},
             'shapeID': ':a',
             'shapeLabel': None,
             'statement_constraints': [{'mandatory': False,
                                        'note': None,
                                        'propertyID': 'dct:creator',
                                        'propertyLabel': None,
                                        'repeatable': True,
                                        'sc_warnings': {},
                                        'valueConstraint': None,
                                        'valueConstraintType': None,
                                        'valueDataType': None,
                                        'valueNodeType': None,
                                        'valueShape': None},
                                       {'mandatory': False,
                                        'note': None,
                                        'propertyID': 'dct:date',
                                        'propertyLabel': None,
                                        'repeatable': True,
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
                                        'valueShape': None}]}]}


def test_pprint_tapshapes_two_shapes():
    """Pretty-print list of TAPShape objects."""
    expected_output_dedented = dedent(
        """\
    DCTAP instance
        Shape
            shapeID:                 :a
            Statement Constraint
                propertyID:          dct:creator
                mandatory:           False
                repeatable:          True
            Statement Constraint
                propertyID:          dct:date
                mandatory:           False
                repeatable:          True
        Shape
            shapeID:                 :b
            Statement Constraint
                propertyID:          foaf:name
    """
    )
    assert pprint_tapshapes(SHAPES_DICT) == expected_output_dedented.splitlines()


def test_pprint_tapshapes_two_shapes_verbose():
    """Pretty-print list of TAPShape objects."""
    expected_output_dedented = dedent(
        """\
    DCTAP instance
        Shape
            shapeID:                 :a
            shapeLabel:              None
            Statement Constraint
                propertyID:          dct:creator
                propertyLabel:       None
                mandatory:           False
                repeatable:          True
                valueNodeType:       None
                valueDataType:       None
                valueConstraint:     None
                valueConstraintType: None
                valueShape:          None
                note:                None
            Statement Constraint
                propertyID:          dct:date
                propertyLabel:       None
                mandatory:           False
                repeatable:          True
                valueNodeType:       None
                valueDataType:       None
                valueConstraint:     None
                valueConstraintType: None
                valueShape:          None
                note:                None
        Shape
            shapeID:                 :b
            shapeLabel:              None
            Statement Constraint
                propertyID:          foaf:name
                propertyLabel:       None
                mandatory:           None
                repeatable:          None
                valueNodeType:       None
                valueDataType:       None
                valueConstraint:     None
                valueConstraintType: None
                valueShape:          None
                note:                None
    """
    )
    assert (
        pprint_tapshapes(SHAPES_DICT, verbose=True)
        == expected_output_dedented.splitlines()
    )
