"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from dctap.csvreader import _get_csvshapes
from dctap.csvshape import CSVShape, CSVTripleConstraint


def test_get_csvshapes_one_default_shape():
    """CSV: one default shape."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:date"},
    ]
    expected_shapes = _get_csvshapes(rows)
    assert len(expected_shapes) == 1
    assert expected_shapes[0].shapeID == ":default"
    assert len(expected_shapes[0].tc_list) == 2


def test_get_csvshapes_one_default_shape_shapeID_not_specified():
    """One shape, default, where shapeID is not specified."""
    rows = [{"propertyID": "dc:creator"}]
    expected_shapes = _get_csvshapes(rows)
    assert expected_shapes[0].shapeID == ":default"
    assert len(expected_shapes[0].tc_list) == 1


def test_get_csvshapes_twoshapes_first_is_default():
    """CSV: two shapes, first of which is default."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = _get_csvshapes(rows)
    assert expected_shapes[0].shapeID == ":default"
    assert len(expected_shapes[0].tc_list) == 2
    assert expected_shapes[1].shapeID == ":author"


def test_get_csvshapes_twoshapes_mixed_statements():
    """CSV: two shapes in three rows, in mixed order (ABA)."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
        {"shapeID": ":book", "propertyID": "dc:type"},
    ]
    expected_shapes = _get_csvshapes(rows)
    assert expected_shapes[0].shapeID == ":book"
    assert len(expected_shapes[0].tc_list) == 2
    assert expected_shapes[1].shapeID == ":author"


def test_get_csvshapes_twoshapes_first_is_default_because_shapeID_empty():
    """CSV: two shapes, first of which is default because shapeID is empty."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = [
        CSVShape(
            shapeID=":default",
            start=True,
            tc_list=[
                CSVTripleConstraint(propertyID="dc:creator"),
                CSVTripleConstraint(propertyID="dc:type"),
            ],
        ),
        CSVShape(
            shapeID=":author",
            start=False,
            tc_list=[
                CSVTripleConstraint(propertyID="foaf:name")
            ],
        ),
    ]
    assert _get_csvshapes(rows) == expected_shapes
    assert type(_get_csvshapes(rows)[0].tc_list[0]) == CSVTripleConstraint


def test_get_csvshapes_two_shapes_one_property_each():
    """CSV: two shapes, one property each."""
    rows = [
        {"shapeID": ":book", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:type"},
        {"shapeID": ":author", "propertyID": "foaf:name"},
    ]
    expected_shapes = [
        CSVShape(
            shapeID=":book",
            start=True,
            tc_list=[
                CSVTripleConstraint(propertyID="dc:creator"),
                CSVTripleConstraint(propertyID="dc:type"),
            ],
        ),
        CSVShape(
            shapeID=":author",
            tc_list=[CSVTripleConstraint(propertyID="foaf:name")],
        ),
    ]
    assert _get_csvshapes(rows) == expected_shapes
