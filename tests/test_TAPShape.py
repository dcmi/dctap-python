"""TAPShape object holds statements sharing a common shapeID."""

from dctap.tapclasses import TAPShape

SHAPE_OBJECT = TAPShape(
    shapeID=":a",
    shapeLabel="Resource",
    sc_list=[
        {"propertyID": "dct:creator", "valueNodeType": "IRI"},
        {"propertyID": "dct:subject", "valueNodeType": "IRI"},
        {"propertyID": "dct:date", "valueNodeType": "String"},
    ],
)


def test_shape_fields_are_individually_addressable():
    """Fields of TAPShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.shapeID == ":a"
    assert shap.shapeLabel == "Resource"
    assert shap.sc_list[1] == {"propertyID": "dct:subject", "valueNodeType": "IRI"}
    assert len(shap.sc_list) == 3


def test_sc_list_items_are_individually_addressable():
    """Items in sc_list field of TAPShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.sc_list[1]["propertyID"] == "dct:subject"
    assert shap.sc_list[2]["valueNodeType"] == "String"


def test_shape_initialized_by_assignment():
    """TAPShape instances can be created by assignment."""
    shap = TAPShape()
    shap.shapeID = ":a"
    shap.shapeLabel = "Resource"
    shap.sc_list = []
    shap.sc_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.sc_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.sc_list.append({"propertyID": "dct:date", "valueNodeType": "String"})
    assert shap == SHAPE_OBJECT


def test_shape_initialized_with_no_shapeid_field_should_pass_for_now():
    """Shape initialized with no shapeID will use default shapeID."""
    shap = TAPShape()
    shap.sc_list = []
    shap.sc_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.sc_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.sc_list.append({"propertyID": "dct:date", "valueNodeType": "String"})
    config_dict = dict()
    config_dict['default_shape_name'] = ":default"
    shap._normalize_default_shapeID(config_dict)
    assert shap == TAPShape(
        shapeID = ":default",
        sc_list=[
            {"propertyID": "dct:creator", "valueNodeType": "IRI"},
            {"propertyID": "dct:subject", "valueNodeType": "IRI"},
            {"propertyID": "dct:date", "valueNodeType": "String"},
        ],
    )


