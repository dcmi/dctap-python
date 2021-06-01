"""CSVShape object holds statements sharing a common shapeID."""

from dctap.csvshape import CSVShape

SHAPE_OBJECT = CSVShape(
    start=True,
    shapeID=":a",
    tc_list=[
        {"propertyID": "dct:creator", "valueNodeType": "IRI"},
        {"propertyID": "dct:subject", "valueNodeType": "IRI"},
        {"propertyID": "dct:date", "valueNodeType": "String"},
    ],
)


def test_shape_fields_are_individually_addressable():
    """Fields of CSVShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.start
    assert shap.shapeID == ":a"
    assert shap.tc_list[1] == {"propertyID": "dct:subject", "valueNodeType": "IRI"}
    assert len(shap.tc_list) == 3


def test_tc_list_items_are_individually_addressable():
    """Items in tc_list field of CSVShape instance are individually addressable."""
    shap = SHAPE_OBJECT
    assert shap.tc_list[1]["propertyID"] == "dct:subject"
    assert shap.tc_list[2]["valueNodeType"] == "String"


def test_shape_initialized_by_assignment():
    """CSVShape instances can be created by assignment."""
    shap = CSVShape()
    shap.start = True
    shap.shapeID = ":a"
    shap.tc_list = []
    shap.tc_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:date", "valueNodeType": "String"})
    assert shap == SHAPE_OBJECT


def test_shape_initialized_with_no_propertyvalues_field_should_pass_for_now():
    """Test should pass for now but this condition should raise exception."""
    shap = CSVShape()
    shap.start = True
    shap.shapeID = ":a"
    assert shap == CSVShape(start=True, shapeID=":a")


def test_shape_initialized_with_no_start_field_should_pass_for_now():
    """Test should pass for now but this condition should raise exception."""
    shap = CSVShape()
    shap.shapeID = ":a"
    shap.tc_list = []
    shap.tc_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:date", "valueNodeType": "String"})
    assert shap == CSVShape(
        shapeID=":a",
        tc_list=[
            {"propertyID": "dct:creator", "valueNodeType": "IRI"},
            {"propertyID": "dct:subject", "valueNodeType": "IRI"},
            {"propertyID": "dct:date", "valueNodeType": "String"},
        ],
    )


def test_shape_initialized_with_no_shapeid_field_should_pass_for_now():
    """Test should pass for now but this condition should raise exception."""
    shap = CSVShape()
    shap.start = True
    shap.tc_list = []
    shap.tc_list.append({"propertyID": "dct:creator", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:subject", "valueNodeType": "IRI"})
    shap.tc_list.append({"propertyID": "dct:date", "valueNodeType": "String"})
    assert shap == CSVShape(
        start=True,
        tc_list=[
            {"propertyID": "dct:creator", "valueNodeType": "IRI"},
            {"propertyID": "dct:subject", "valueNodeType": "IRI"},
            {"propertyID": "dct:date", "valueNodeType": "String"},
        ],
    )
