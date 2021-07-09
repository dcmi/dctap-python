"""Get lists of shape / statement constraint elements from dataclasses."""

from dataclasses import asdict
from dctap.config import get_config, _shape_elements, _statement_constraint_elements
from dctap.tapclasses import TAPShape, TAPStatementConstraint

def test_get_TAPShape_elements_when_no_config_dict_specified():
    """List TAPShape elements (minus sh_warnings and sc_list)."""
    expected = ['shapeID', 'shapeLabel']
    assert _shape_elements(TAPShape) == expected

def test_get_TAPShape_elements_plus_extras_when_config_dict_specified():
    """List TAPShape elements plus extras."""
    expected = ["shapeID", "shapeLabel", "closed", "start"]
    config_dict = { "extra_shape_elements": ["closed", "start"] }
    assert _shape_elements(TAPShape, config_dict) == expected

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
    assert sorted(_statement_constraint_elements(TAPStatementConstraint)) == sorted(expected)

def test_get_TAPStatementConstraint_elements_plus_extras_when_config_dict_specified():
    """List TAPStatementConstraint elements plus extras."""
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
        "min",
        "max",
    ]
    config_dict = { "extra_statement_constraint_elements": ["min", "max"] }
    assert sorted(_statement_constraint_elements(TAPStatementConstraint, config_dict)) == sorted(expected)

