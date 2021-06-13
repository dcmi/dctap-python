"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from dctap.csvreader import _get_tapshapes
from dctap.tapclasses import TAPShape, TAPStatementConstraint


def test_get_tapshapes_one_default_shape():
    """CSV: one default shape."""
    rows = [
        {"shapeID": "", "propertyID": "dc:creator"},
        {"shapeID": "", "propertyID": "dc:date"},
        {"shapeID": "", "propertyID": "dc:subject"},
    ]
    tapshapes_output = _get_tapshapes(rows)
    expected_shapes = tapshapes_output[0]
    assert len(expected_shapes) == 1
    assert expected_shapes[0].shapeID == ":default"
    assert len(expected_shapes[0].sc_list) == 3


# def test_get_tapshapes_one_default_shape_shapeID_not_specified():
#     """One shape, default, where shapeID is not specified."""
#     rows = [{"propertyID": "dc:creator"}]
#     tapshapes_output = _get_tapshapes(rows)
#     expected_shapes = tapshapes_output[0]
#     assert expected_shapes[0].shapeID == ":default"
#     assert len(expected_shapes[0].sc_list) == 1
# 
# 
# def test_get_tapshapes_twoshapes_first_is_default():
#     """CSV: two shapes, first of which is default."""
#     rows = [
#         {"shapeID": "", "propertyID": "dc:creator"},
#         {"shapeID": "", "propertyID": "dc:type"},
#         {"shapeID": ":author", "propertyID": "foaf:name"},
#     ]
#     tapshapes_output = _get_tapshapes(rows)
#     expected_shapes = tapshapes_output[0]
#     assert expected_shapes[0].shapeID == ":default"
#     assert len(expected_shapes[0].sc_list) == 2
#     assert expected_shapes[1].shapeID == ":author"
# 
# 
# def test_get_tapshapes_twoshapes_mixed_statements():
#     """CSV: two shapes in three rows, in mixed order (ABA)."""
#     rows = [
#         {"shapeID": ":book", "propertyID": "dc:creator"},
#         {"shapeID": ":author", "propertyID": "foaf:name"},
#         {"shapeID": ":book", "propertyID": "dc:type"},
#     ]
#     tapshapes_output = _get_tapshapes(rows)
#     expected_shapes = tapshapes_output[0]
#     assert expected_shapes[0].shapeID == ":book"
#     assert len(expected_shapes[0].sc_list) == 2
#     assert expected_shapes[1].shapeID == ":author"
# 
# 
# def test_get_tapshapes_twoshapes_first_is_default_because_shapeID_empty():
#     """CSV: two shapes, first of which is default because shapeID is empty."""
#     rows = [
#         {"shapeID": "", "propertyID": "dc:creator"},
#         {"shapeID": "", "propertyID": "dc:type"},
#         {"shapeID": ":author", "propertyID": "foaf:name"},
#     ]
#     expected_shapes = [
#         TAPShape(
#             shapeID=":default",
#             start=True,
#             sc_list=[
#                 TAPStatementConstraint(propertyID="dc:creator"),
#                 TAPStatementConstraint(propertyID="dc:type"),
#             ],
#         ),
#         TAPShape(
#             shapeID=":author",
#             start=False,
#             sc_list=[
#                 TAPStatementConstraint(propertyID="foaf:name")
#             ],
#         ),
#     ]
#     assert _get_tapshapes(rows)[0] == expected_shapes
#     assert type(_get_tapshapes(rows)[0][0].sc_list[0]) == TAPStatementConstraint
# 
# 
# def test_get_tapshapes_two_shapes_one_property_each():
#     """CSV: two shapes, one property each."""
#     rows = [
#         {"shapeID": ":book", "propertyID": "dc:creator"},
#         {"shapeID": "", "propertyID": "dc:type"},
#         {"shapeID": ":author", "propertyID": "foaf:name"},
#     ]
#     expected_shapes = [
#         TAPShape(
#             shapeID=":book",
#             start=True,
#             sc_list=[
#                 TAPStatementConstraint(propertyID="dc:creator"),
#                 TAPStatementConstraint(propertyID="dc:type"),
#             ],
#         ),
#         TAPShape(
#             shapeID=":author",
#             sc_list=[TAPStatementConstraint(propertyID="foaf:name")],
#         ),
#     ]
#     assert _get_tapshapes(rows)[0] == expected_shapes
