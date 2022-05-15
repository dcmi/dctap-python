"""Rows-as-dicts list to shapes-as-dicts list where shape described on own line."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _get_tapshapes
from dctap.tapclasses import TAPShape, TAPStatementTemplate

SETTINGS_DICT = get_config()

@pytest.mark.skip
def test_get_tapshapes_one_default_shape_but_with_shape_elements_on_separate_line():
    """CSV: one named shape, declared on its own line."""
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

