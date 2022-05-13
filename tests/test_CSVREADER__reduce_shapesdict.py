"""Iteratively remove elements from shapes dictionary with falsy values."""

from dctap.csvreader import _reduce_shapesdict

def test_reduce_shapesdict():
    """Iterate thru shapes in shapes_dict, removing empty shape and sc elements."""
    input = {'shapes': [
                        {
                         'shapeID': 'a',
                         'shapeLabel': '',
                         'sh_warnings': {},
                         'extra_elements': {'closed': 'True'},
                         'statement_templates': [
                             {
                              'propertyID': 'dc:creator',
                              'propertyLabel': '',
                              'mandatory': None,
                              'repeatable': None,
                              'valueNodeType': '',
                              'valueDataType': '',
                              'valueConstraint': '',
                              'valueConstraintType': 'picklist',
                              'valueShape': '',
                              'note': '',
                              'st_warnings': {'valueConstraint': "Value constraint type ('picklist') but no value constraint."},
                              'extra_elements': {'min': '1'}
                             }
                         ]
                        },
                        {
                         'shapeID': 'b',
                         'shapeLabel': '',
                         'sh_warnings': {},
                         'extra_elements': {'closed': 'False'},
                         'statement_templates': [
                             {
                              'propertyID': 'foaf:name',
                              'propertyLabel': '',
                              'mandatory': None,
                              'repeatable': None,
                              'valueNodeType': '',
                              'valueDataType': '',
                              'valueConstraint': '',
                              'valueConstraintType': '',
                              'valueShape': '',
                              'note': '',
                              'st_warnings': {},
                              'extra_elements': {'min': '2'}
                             }
                         ]
                        }
                       ]
            }
    expected_output = {'shapes': [
                        {
                         'shapeID': 'a',
                         'closed': 'True',
                         'statement_templates': [
                             {
                              'propertyID': 'dc:creator',
                              'valueConstraintType': 'picklist',
                              'min': '1',
                             }
                         ]
                        },
                        {
                         'shapeID': 'b',
                         'closed': 'False',
                         'statement_templates': [
                             {
                              'propertyID': 'foaf:name',
                              'min': '2',
                             }
                         ]
                        }
                       ]
            }
    assert _reduce_shapesdict(input) == expected_output
