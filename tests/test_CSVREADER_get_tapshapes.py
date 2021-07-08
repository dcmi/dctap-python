"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _get_tapshapes
from dctap.tapclasses import TAPShape, TAPStatementConstraint

SETTINGS_DICT = get_config()

def test_get_tapshapes_one_default_shape():
    """CSV: one default shape."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:date"},
        {"shapeID": "", "propertyID": "dc:subject"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert len(expected_shapes) == 1
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert len(expected_shapes["shapes"][0]["statement_constraints"]) == 3


def test_get_tapshapes_one_default_shape_shapeID_not_specified():
    """One shape, default, where shapeID is not specified."""
    rows = [{"propertyID": "dc:creator"}]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == "default"


def test_get_tapshapes_twoshapes_first_is_default():
    """CSV: two shapes, first of which is default."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_constraints"]) == 2


def test_get_tapshapes_twoshapes_mixed_statements():
    """CSV: two shapes in three rows, in mixed order (ABA)."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
        {"shapeID": ":book", "propertyID": "dc:type"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == ":book"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_constraints"]) == 2


def test_get_tapshapes_twoshapes_first_is_default_because_shapeID_empty():
    """CSV: two shapes, first of which is default because shapeID is empty."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = {'shapes': [{'sh_warnings': {},
                 'shapeID': 'default',
                 'shapeLabel': '',
                 'statement_constraints': [{'mandatory': None,
                                            'note': '',
                                            'propertyID': 'dc:creator',
                                            'propertyLabel': '',
                                            'repeatable': None,
                                            'sc_warnings': {},
                                            'valueConstraint': '',
                                            'valueConstraintType': '',
                                            'valueDataType': '',
                                            'valueNodeType': '',
                                            'valueShape': ''},
                                           {'mandatory': None,
                                            'note': '',
                                            'propertyID': 'dc:type',
                                            'propertyLabel': '',
                                            'repeatable': None,
                                            'sc_warnings': {},
                                            'valueConstraint': '',
                                            'valueConstraintType': '',
                                            'valueDataType': '',
                                            'valueNodeType': '',
                                            'valueShape': ''}]},
                {'sh_warnings': {},
                 'shapeID': ':author',
                 'shapeLabel': '',
                 'statement_constraints': [{'mandatory': None,
                                            'note': '',
                                            'propertyID': 'foaf:name',
                                            'propertyLabel': '',
                                            'repeatable': None,
                                            'sc_warnings': {},
                                            'valueConstraint': '',
                                            'valueConstraintType': '',
                                            'valueDataType': '',
                                            'valueNodeType': '',
                                            'valueShape': ''}]}]}
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_constraints"]) == 2
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]) == dict
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"]) == list
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]) == dict
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]["statement_constraints"]) == list
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]["statement_constraints"][0]) == dict


def test_get_tapshapes_two_shapes_one_property_each():
    """CSV: two shapes, one property each."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = {'shapes': [
                        {'shapeID': ':book',
                         'statement_constraints': [
                             {'propertyID': 'dc:creator'},
                             {'propertyID': 'dc:type'}
                         ] 
                        }, {'shapeID': ':author',
                          'statement_constraints': [
                             {'propertyID': 'foaf:name'}
                          ]
                        }
                      ]
                    }
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == ":book"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
