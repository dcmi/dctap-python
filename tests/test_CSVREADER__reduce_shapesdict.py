"""Iteratively remove elements from shapes dictionary with falsy values."""

from dctap.csvreader import _simplify

def test_reduce_shapesdict():
    """Iterate thru shapes in shapes_dict, removing empty shape and sc elements."""
    input = {'shapes': [
                        {
                         'shapeID': 'a',
                         'shapeLabel': '',
                         'shape_warns': {},
                         'shape_extras': {'closed': 'True'},
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
                              'state_warns': {'valueConstraint': "Value constraint type ('picklist') but no value constraint."},
                              'state_extras': {'min': '1'}
                             }
                         ]
                        },
                        {
                         'shapeID': 'b',
                         'shapeLabel': '',
                         'shape_warns': {},
                         'shape_extras': {'closed': 'False'},
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
                              'state_warns': {},
                              'state_extras': {'min': '2'}
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
    assert _simplify(input) == expected_output
