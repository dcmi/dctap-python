"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from dctap.csvreader import _get_tapshapes
from dctap.tapclasses import TAPShape, TAPStatementConstraint


def test_get_tapshapes_valueConstraint_URI_with_valueNodeType_Literal():
    """Warn when valueConstraint looks like URI and valueNodeType Literal."""
    rows = [
            {"propertyID": "dc:creator",
             "valueNodeType": "Literal",
             "valueConstraint": "ex:12345",
            },
    ]    
    tapshapes_output = _get_tapshapes(rows)
    expected_shapes = tapshapes_output[0]
    warnings_dict = tapshapes_output[1]
    assert len(expected_shapes) == 1
    assert expected_shapes[0].shapeID == ":default"
    assert len(expected_shapes[0].sc_list) == 1
    assert warnings_dict[":default"].get('valueNodeType') is not None


