"""@@@."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _get_prefixes


def test_get_prefixes():
    """@@@"""
    csvrows = [ 
        {
            'shapeID': ':a',
            'propertyID': 'dc:creator',
            'valueShape': ':b',
            'valueDataType': 'xsd:integer',
        }, {
            'shapeID': '',
            'propertyID': 'dc:type',
            'valueConstraint': 'so:Book',
            'valuegestalt': ''
        }, {
            'shapeID': ':author',
            'propertyID': 'foaf:name',
            'valueConstraint': '',
            'valueShape': ':asdf',
            "note": "Typically: the author.",
        }
    ]
    expected_prefixes = {":", "dc:", "xsd:", "foaf:"}
    assert _get_prefixes(csvrows) == expected_prefixes
