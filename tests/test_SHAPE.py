"""TAPShape object holds statements sharing a common shapeID."""

import pytest
from dctap.tapclasses import TAPShape

SHAPE_OBJECT = TAPShape(
    shapeID=":a",
    shapeLabel="Resource",
    state_list=[
        {"propertyID": "dct:creator", "valueNodeType": "IRI"},
        {"propertyID": "dct:subject", "valueNodeType": "IRI"},
        {"propertyID": "dct:date", "valueNodeType": "Literal"},
    ],
)

def test_shape_fields_are_individually_addressable():
    """Fields of TAPShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.shapeID == ":a"
    assert shap.shapeLabel == "Resource"
    assert shap.state_list[1] == {"propertyID": "dct:subject", "valueNodeType": "IRI"}
    assert len(shap.state_list) == 3

def test_statement_template_list_items_are_individually_addressable():
    """Items in state_list field of TAPShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.state_list[1]["propertyID"] == "dct:subject"
    assert shap.state_list[2]["valueNodeType"] == "Literal"

def test_shape_initialized_by_assignment():
    """TAPShape instances can be created by assignment."""
    shap = TAPShape()
    shap.shapeID = ":a"
    shap.shapeLabel = "Resource"
    shap.state_list = []
    shap.state_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.state_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.state_list.append({"propertyID": "dct:date", "valueNodeType": "Literal"})
    assert shap == SHAPE_OBJECT

def test_shape_initialized_with_no_shapeid_field_should_pass_for_now():
    """Shape initialized with no shapeID will use default shapeID."""
    config_dict = {}
    config_dict["default_shape_identifier"] = "default"
    shap = TAPShape()
    shap.state_list = []
    shap.state_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.state_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.state_list.append({"propertyID": "dct:date", "valueNodeType": "Literal"})
    shap._normalize_default_shapeID(config_dict)
    assert shap == TAPShape(
        shapeID="default",
        state_list=[
            {"propertyID": "dct:creator", "valueNodeType": "IRI"},
            {"propertyID": "dct:subject", "valueNodeType": "IRI"},
            {"propertyID": "dct:date", "valueNodeType": "Literal"},
        ],
    )
