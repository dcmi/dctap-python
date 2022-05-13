"""Get lists of shape / statement template elements from dataclasses."""

import pytest
from dataclasses import asdict
from dctap.config import get_config, get_shape_elements, get_statement_template_elements
from dctap.tapclasses import TAPShape, TAPStatementTemplate

def test_get_TAPShape_elements_when_no_config_dict_specified():
    """List TAPShape elements (minus sh_warnings and st_list)."""
    expected = ['shapeID', 'shapeLabel']
    assert get_shape_elements(TAPShape)[0] == expected

def test_get_TAPShape_elements_plus_extras_when_config_dict_specified():
    """List TAPShape elements plus extras."""
    expected_shape_elements = ["shapeID", "shapeLabel"]
    expected_xtra_shape_elements = ["closed", "start"]
    config_dict = dict(extra_shape_elements=["closed", "start"])
    assert get_shape_elements(TAPShape, config_dict)[0] == expected_shape_elements
    assert get_shape_elements(TAPShape, config_dict)[1] == expected_xtra_shape_elements

def test_get_TAPStatementTemplate_elements_when_no_config_dict_specified():
    """List TAPStatementTemplate elements (minus st_warnings)."""
    expected = [
        "propertyID",
        "propertyLabel",
        "mandatory",
        "repeatable",
        "valueNodeType",
        "valueDataType",
        "valueConstraint",
        "valueConstraintType",
        "valueShape",
        "note",
    ]
    assert sorted(get_statement_template_elements(TAPStatementTemplate)[0]) == sorted(expected)

def test_get_TAPStatementTemplate_elements_plus_extras_when_config_dict_specified():
    """List TAPStatementTemplate elements plus extras."""
    expected_st_elements = [
        "propertyID",
        "propertyLabel",
        "mandatory",
        "repeatable",
        "valueNodeType",
        "valueDataType",
        "valueConstraint",
        "valueConstraintType",
        "valueShape",
        "note",
    ]
    expected_extra_st_elements = [
        "min",
        "max",
    ]
    config_dict = { "extra_statement_template_elements": ["min", "max"] }
    actual_st_elements, actual_extra_st_elements = get_statement_template_elements(TAPStatementTemplate, config_dict)
    assert sorted(actual_st_elements) == sorted(expected_st_elements)
    assert sorted(actual_extra_st_elements) == sorted(expected_extra_st_elements)
