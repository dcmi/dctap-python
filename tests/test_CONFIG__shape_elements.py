"""Get lists of shape / statement template elements from dataclasses."""

import pytest
from dataclasses import asdict
from dctap.config import get_config, get_shems, get_stems
from dctap.tapclasses import TAPShape, TAPStatementTemplate

def test_get_TAPShape_elements_when_no_config_dict_specified():
    """List TAPShape elements (minus shape_warns and state_list)."""
    expected = ['shapeID', 'shapeLabel']
    assert get_shems(TAPShape)[0] == expected

def test_get_TAPShape_elements_plus_extras_when_config_dict_specified():
    """List TAPShape elements plus extra shape elements."""
    expected_main_shems = ["shapeID", "shapeLabel"]
    expected_xtra_shems = ["closed", "start"]
    #config_dict = dict(extra_shape_elements=["closed", "start"])
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    assert get_shems(TAPShape, config_dict)[0] == expected_main_shems
    assert get_shems(TAPShape, config_dict)[1] == expected_xtra_shems

def test_get_TAPStatementTemplate_elements_when_no_config_dict_specified():
    """List TAPStatementTemplate elements (minus state_warns)."""
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
    assert sorted(get_stems(TAPStatementTemplate)[0]) == sorted(expected)

def test_get_TAPStatementTemplate_elements_plus_extras_when_config_dict_specified():
    """List TAPStatementTemplate elements plus extra statement elements."""
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
    (actual_st_elements, actual_extra_st_elements) = get_stems(TAPStatementTemplate, config_dict)
    assert sorted(actual_st_elements) == sorted(expected_st_elements)
    assert sorted(actual_extra_st_elements) == sorted(expected_extra_st_elements)
