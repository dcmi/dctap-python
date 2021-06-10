"""Pretty-print csvshape dicts to console."""

import pytest
from dataclasses import asdict
from textwrap import dedent
from dctap.classes import TAPShape, TAPStatementConstraint
from dctap.inspect import pprint_csvshapes
from dctap.csvreader import _get_csvshapes

SHAPES_LIST = [
    TAPShape(
        shapeID=":a",
        shapeLabel=None,
        start=True,
        sc_list=[
            TAPStatementConstraint(
                propertyID="dct:creator",
                mandatory=False,
                note=None,
                propertyLabel=None,
                repeatable=False,
                valueConstraint=None,
                valueConstraintType=None,
                valueDataType=None,
                valueNodeType=None,
                valueShape=None,
            ), TAPStatementConstraint(
                propertyID="dct:date",
                mandatory=False,
                note=None,
                propertyLabel=None,
                repeatable=False,
                valueConstraint=None,
                valueConstraintType=None,
                valueDataType=None,
                valueNodeType=None,
                valueShape=None,
            ),
        ],
    ),
    TAPShape(
        shapeID=":b",
        shapeLabel=None,
        start=False,
        sc_list=[
            TAPStatementConstraint(
                propertyID="foaf:name",
                mandatory=False,
                note=None,
                propertyLabel=None,
                repeatable=False,
                valueConstraint=None,
                valueConstraintType=None,
                valueDataType=None,
                valueNodeType=None,
                valueShape=None,
            )
        ],
    ),
]


def test_pprint_tapshapes_two_shapes():
    """Pretty-print list of TAPShape objects."""
    expected_output_dedented = dedent(
        """\
    DCTAP instance
        Shape
            shapeID: :a
            Statement Constraint
                propertyID: dct:creator
            Statement Constraint
                propertyID: dct:date
        Shape
            shapeID: :b
            Statement Constraint
                propertyID: foaf:name
    """
    )
    assert pprint_csvshapes(SHAPES_LIST) == expected_output_dedented.splitlines()


def test_pprint_tapshapes_two_shapes_verbose():
    """Pretty-print list of TAPShape objects."""
    expected_output_dedented = dedent(
        """\
    DCTAP instance
        Shape
            shapeID: :a
            shapeLabel: None
            Statement Constraint
                propertyID: dct:creator
                propertyLabel: None
                mandatory: False
                repeatable: False
                valueNodeType: None
                valueDataType: None
                valueConstraint: None
                valueConstraintType: None
                valueShape: None
                note: None
            Statement Constraint
                propertyID: dct:date
                propertyLabel: None
                mandatory: False
                repeatable: False
                valueNodeType: None
                valueDataType: None
                valueConstraint: None
                valueConstraintType: None
                valueShape: None
                note: None
        Shape
            shapeID: :b
            shapeLabel: None
            Statement Constraint
                propertyID: foaf:name
                propertyLabel: None
                mandatory: False
                repeatable: False
                valueNodeType: None
                valueDataType: None
                valueConstraint: None
                valueConstraintType: None
                valueShape: None
                note: None
    """
    )
    assert (
        pprint_csvshapes(SHAPES_LIST, verbose=True)
        == expected_output_dedented.splitlines()
    )
