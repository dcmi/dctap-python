"""From list of rows-as-dictionaries, output dictionary of shapes-as-dictionaries."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _get_tapshapes

SETTINGS_DICT = get_config()


def test_get_tapshapes_two_shapes_with_rows_that_are_ignored():
    """Lines without shapeID and/or propertyID are ignored."""
    rows = [
        {"shapeID": ":bookshape"},
        {},
        {"propertyID": "dc:creator"},
        {},
        {"shapeID": ":author"},
        {"propertyID": "foaf:name"},
    ]
    (shapes, warns) = _get_tapshapes(rows, SETTINGS_DICT)
    assert len(shapes["shapes"]) == 2
    assert shapes["shapes"][0]["shapeID"] == ":bookshape"
    assert len(shapes["shapes"][0]["statement_templates"]) == 1
    assert shapes["shapes"][1]["shapeID"] == ":author"
    assert len(shapes["shapes"][1]["statement_templates"]) == 1

def test_get_tapshapes_two_shapes_declare_on_separate_rows():
    """Shape declared in own rows followed by rows with statement templates."""
    rows = [
        {"shapeID": ":bookshape"},
        {"propertyID": "dc:creator"},
        {"shapeID": ":author"},
        {"propertyID": "foaf:name"},
    ]
    (shapes, warns) = _get_tapshapes(rows, SETTINGS_DICT)
    assert len(shapes["shapes"]) == 2
    assert shapes["shapes"][0]["shapeID"] == ":bookshape"
    assert len(shapes["shapes"][0]["statement_templates"]) == 1
    assert shapes["shapes"][1]["shapeID"] == ":author"
    assert len(shapes["shapes"][1]["statement_templates"]) == 1

def test_get_tapshapes_shape_elements_declared_on_separate_row():
    """One shape, declared on its own row."""
    rows = [
        {"shapeID": ":bookshape", "shapeLabel": "Book"},
        {"propertyID": "dc:creator"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert len(expected_shapes) == 1
    assert expected_shapes["shapes"][0]["shapeID"] == ":bookshape"
    assert expected_shapes["shapes"][0]["shapeLabel"] == "Book"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 1

def test_get_tapshapes_one_default_shape_with_shapeID_asserted():
    """One default shape with shapeID asserted."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:date"},
        {"shapeID": "", "propertyID": "dc:subject"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert len(expected_shapes) == 1
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 3

def test_get_tapshapes_one_default_shape_with_shapeID_not_asserted():
    """One default shape with shapeID not asserted."""
    rows = [
        {"propertyID": "dc:creator"},
        {"propertyID": "dc:date"},
        {"propertyID": "dc:subject"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert len(expected_shapes) == 1
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 3

def test_get_tapshapes_two_shapes_first_is_default():
    """Two shapes, first of which is default."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 2

def test_get_tapshapes_two_shapes_where_rows_are_out_of_order():
    """Two shapes in three rows, in mixed order (ABA)."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
        {"shapeID": ":book", "propertyID": "dc:type"},
    ]
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == ":book"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 2
    assert len(expected_shapes["shapes"][1]["statement_templates"]) == 1

def test_get_tapshapes_two_shapes_spelled_out_entirely():
    """Two shapes, first of which is default because shapeID is empty."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = {'shapes': [{'shape_warns': {},
                 'shapeID': 'default',
                 'shapeLabel': '',
                 'statement_templates': [{'mandatory': None,
                                            'note': '',
                                            'propertyID': 'dc:creator',
                                            'propertyLabel': '',
                                            'repeatable': None,
                                            'state_warns': {},
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
                                            'state_warns': {},
                                            'valueConstraint': '',
                                            'valueConstraintType': '',
                                            'valueDataType': '',
                                            'valueNodeType': '',
                                            'valueShape': ''}]},
                {'shape_warns': {},
                 'shapeID': ':author',
                 'shapeLabel': '',
                 'statement_templates': [{'mandatory': None,
                                            'note': '',
                                            'propertyID': 'foaf:name',
                                            'propertyLabel': '',
                                            'repeatable': None,
                                            'state_warns': {},
                                            'valueConstraint': '',
                                            'valueConstraintType': '',
                                            'valueDataType': '',
                                            'valueNodeType': '',
                                            'valueShape': ''}]}]}
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == "default"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 2
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]) == dict
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"]) == list
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]) == dict
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]["statement_templates"]) == list
    assert type(_get_tapshapes(rows, SETTINGS_DICT)[0]["shapes"][0]["statement_templates"][0]) == dict

def test_get_tapshapes_two_shapes_shapeID_most_recently_used():
    """Two shapes, where shapeID left blank assigned "most recently used"."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = {'shapes': [
                        {'shapeID': ':book',
                         'statement_templates': [
                             {'propertyID': 'dc:creator'},
                             {'propertyID': 'dc:type'}
                         ] 
                        }, {'shapeID': ':author',
                          'statement_templates': [
                             {'propertyID': 'foaf:name'}
                          ]
                        }
                      ]
                    }
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == ":book"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 2

def test_get_tapshapes_two_shapes_shapeID_not_always_asserted():
    """Two shapes, where one line does not assert shapeID at all"."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = {'shapes': [
                        {'shapeID': ':book',
                         'statement_templates': [
                             {'propertyID': 'dc:creator'},
                             {'propertyID': 'dc:type'}
                         ] 
                        }, {'shapeID': ':author',
                          'statement_templates': [
                             {'propertyID': 'foaf:name'}
                          ]
                        }
                      ]
                    }
    tapshapes_output = _get_tapshapes(rows, SETTINGS_DICT)
    expected_shapes = tapshapes_output[0]
    assert expected_shapes["shapes"][0]["shapeID"] == ":book"
    assert expected_shapes["shapes"][1]["shapeID"] == ":author"
    assert len(expected_shapes["shapes"][0]["statement_templates"]) == 2
