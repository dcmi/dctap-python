"""Compute default config dict."""

import pytest
from dctap.config import _initialize_config_dict
from dctap.tapclasses import TAPShape, TAPStatementTemplate


def test_initialize_config_dict():
    """Compute default config dict from TAP classes and add placeholders."""
    expected_output = {
        "csv_elements": [
            "shapeID",
            "shapeLabel",
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
        ],
        "default_shape_identifier": "default",
        "element_aliases": {
            "mandatory": "mandatory",
            "note": "note",
            "propertyid": "propertyID",
            "propertylabel": "propertyLabel",
            "repeatable": "repeatable",
            "shapeid": "shapeID",
            "shapelabel": "shapeLabel",
            "valueconstraint": "valueConstraint",
            "valueconstrainttype": "valueConstraintType",
            "valuedatatype": "valueDataType",
            "valuenodetype": "valueNodeType",
            "valueshape": "valueShape",
        },
        "extra_element_aliases": {},
        "extra_shape_elements": [],
        "extra_statement_template_elements": [],
        "extra_value_node_types": [],
        "picklist_elements": [],
        "picklist_item_separator": " ",
        "prefixes": {},
        "shape_elements": ["shapeID", "shapeLabel"],
        "statement_template_elements": [
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
        ],
    }
    assert _initialize_config_dict(TAPShape, TAPStatementTemplate) == expected_output
