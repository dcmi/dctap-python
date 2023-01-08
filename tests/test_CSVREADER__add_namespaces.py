"""
Test csvreader._add_namespaces

Arguments:
- tapshapes (as computed by csvreader._get_tapshapes)
- config_dict (as computed by config.get_config)
- prefixes_used (as computed by csvreader._get_prefixes_actually_used)
"""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _add_namespaces

NONDEFAULT_CONFIGYAML = """
default_shape_identifier: "default"

prefixes:
    "ex:":      "http://example.org/"
    "dct:":     "http://purl.org/dc/terms/"
    "school:":  "http://school.example/#"
    "xsd:":     "http://www.w3.org/2001/XMLSchema#"
    "dc11:":    "http://purl.org/dc/elements/1.1/"
"""

def test_add_key_namespaces_to_dict_tapshapes():
    """
    Adds key 'namespaces' to dict 'tapshapes'.

    Args:
    - tapshapes   - takes precomputed dict with one key: 'shapes'
    - config_dict - computes from NONDEFAULT_CONFIGYAML
    """
    given_config_dict = get_config(nondefault_configyaml_str=NONDEFAULT_CONFIGYAML)
    assert "school:" in given_config_dict.get("prefixes")
    assert "ex:" in given_config_dict.get("prefixes")
    assert "dct:" in given_config_dict.get("prefixes")
    assert "xsd:" in given_config_dict.get("prefixes")
    assert "dc11:" in given_config_dict.get("prefixes")
    assert "dc:" not in given_config_dict.get("prefixes")

    given_csvrows = [
        {
            "shapeID": "school:a",
            "propertyID": "ex:quantity",
            "valueDataType": "xsd:integer",
        },
        {"shapeID": "ex:a", "propertyID": "dct:date", "valueDataType": "xsd:date"},
    ]

    given_tapshapes = {
        "shapes": [
            {
                "shape_warns": {},
                "shapeID": "default",
                "shapeLabel": "",
                "statement_templates": [
                    {"propertyID": "dc:creator"},
                    {"propertyID": "dc:type"},
                ],
            }
        ]
    }

    expected_tapshapes = {
        "namespaces": {
            "ex:": "http://example.org/",
            "dct:": "http://purl.org/dc/terms/",
            "school:": "http://school.example/#",
            "xsd:": "http://www.w3.org/2001/XMLSchema#",
        },
        "shapes": [
            {
                "shape_warns": {},
                "shapeID": "default",
                "shapeLabel": "",
                "statement_templates": [
                    {"propertyID": "dc:creator"},
                    {"propertyID": "dc:type"},
                ],
            }
        ],
    }

    # As computed by csvreader._get_prefixes_actually_used(given_csvrows)
    prefixes_actually_used = ["ex:", "xsd:", "school:", "dct:"]

    actual_tapshapes = _add_namespaces(
        tapshapes=given_tapshapes,
        config_dict=given_config_dict,
        prefixes_used=prefixes_actually_used,
    )

    assert actual_tapshapes == expected_tapshapes
