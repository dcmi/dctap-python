"""Tests dctap.csvreader._get_prefixes_actually_used."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _get_prefixes_actually_used


def test_get_prefixes_actually_used():
    """Get prefixes actually used in shapeID, propertyID, valueShape, valueDataType."""
    csvrows = [
        {
            "shapeID": ":a",
            "propertyID": "dc:creator",
            "valueShape": ":b",
            "valueDataType": "xsd:integer",
        },
        {
            "shapeID": "",
            "propertyID": "dc:type",
            "valueConstraint": "so:Book",
            "valuegestalt": "",
        },
        {
            "shapeID": ":author",
            "propertyID": "foaf:name",
            "valueConstraint": "",
            "valueShape": ":asdf",
            "note": "Typically: the author.",
        },
    ]
    expected_prefixes = [":", "dc:", "xsd:", "foaf:"]
    assert sorted(_get_prefixes_actually_used(csvrows)) == sorted(expected_prefixes)

def test_get_prefixes_actually_used_even_if_none_used():
    """Set config_dict.prefixes as empty dict if no prefixes used in TAP."""
    csvrows = [
        {
            "shapeID": "book",
            "propertyID": "creator",
            "valueShape": "author",
            "valueDataType": "integer",
        },
        {
            "shapeID": "",
            "propertyID": "type",
            "valueConstraint": "Book",
        },
        {
            "shapeID": "author",
            "propertyID": "name",
            "note": "Typically the author.",
        },
    ]
    expected_prefixes = []
    assert _get_prefixes_actually_used(csvrows) == expected_prefixes

def test_get_prefixes_actually_used_including_prefix_of_shapeid():
    """Includes prefix for ShapeID. Note that returned list is sorted."""
    csvrows = [
        {
            "shapeID": "biblio:book",
            "propertyID": "creator",
            "valueShape": "author",
            "valueDataType": "integer",
        },
        {
            "shapeID": "",
            "propertyID": "type",
            "valueConstraint": "Book",
        },
        {
            "shapeID": "author",
            "propertyID": "foaf:name",
            "note": "Typically the author.",
        },
    ]
    expected_prefixes = sorted(["biblio:", "foaf:"])
    actual_prefixes = sorted(_get_prefixes_actually_used(csvrows))
    assert actual_prefixes == expected_prefixes
