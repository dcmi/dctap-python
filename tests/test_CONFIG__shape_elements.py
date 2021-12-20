"""Get lists of shape / statement constraint elements from dataclasses."""

import pytest
from dataclasses import asdict
from dctap.config import get_config, shape_elements, statement_constraint_elements
from dctap.tapclasses import TAPShape, TAPStatementConstraint

def test_get_TAPShape_elements_when_no_config_dict_specified():
    """List TAPShape elements (minus sh_warnings and sc_list)."""
    expected = ['shapeID', 'shapeLabel']
    assert shape_elements(TAPShape)[0] == expected

def test_get_TAPShape_elements_plus_extras_when_config_dict_specified():
    """List TAPShape elements plus extras."""
    expected_shape_elements = ["shapeID", "shapeLabel"]
    expected_xtra_shape_elements = ["closed", "start"]
    config_dict = dict(extra_shape_elements=["closed", "start"])
    assert shape_elements(TAPShape, config_dict)[0] == expected_shape_elements
    assert shape_elements(TAPShape, config_dict)[1] == expected_xtra_shape_elements

def test_get_TAPStatementConstraint_elements_when_no_config_dict_specified():
    """List TAPStatementConstraint elements (minus sc_warnings)."""
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
    assert sorted(statement_constraint_elements(TAPStatementConstraint)[0]) == sorted(expected)

def test_get_TAPStatementConstraint_elements_plus_extras_when_config_dict_specified():
    """List TAPStatementConstraint elements plus extras."""
    expected_sc_elements = [
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
    expected_extra_sc_elements = [
        "min",
        "max",
    ]
    config_dict = { "extra_statement_constraint_elements": ["min", "max"] }
    actual_sc_elements, actual_extra_sc_elements = statement_constraint_elements(TAPStatementConstraint, config_dict)
    assert sorted(actual_sc_elements) == sorted(expected_sc_elements)
    assert sorted(actual_extra_sc_elements) == sorted(expected_extra_sc_elements)
