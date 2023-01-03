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

def test_get_config_from_default_config_file_if_present():
    """
    Adds key 'namespaces' to dict 'tapshapes'.

    Args:
    - tapshapes   - takes precomputed dict with one key: 'shapes'
    - config_dict - computes from NONDEFAULT_CONFIGYAML
    - csvrows     - takes precomputed list of dicts
    """
    given_config_dict = get_config(config_yamlstring=NONDEFAULT_CONFIGYAML)
    assert "school:" in given_config_dict.get("prefixes")
    assert "ex:" in given_config_dict.get("prefixes")
    assert "dct:" in given_config_dict.get("prefixes")
    assert "xsd:" in given_config_dict.get("prefixes")
    assert "dc11:" in given_config_dict.get("prefixes")
    assert "dc:" not in given_config_dict.get("prefixes")

#    given_csvrows = [
#        {
#            'shapeID': 'school:a', 
#            'propertyID': 'ex:quantity', 
#            'valueDataType': 'xsd:integer'
#        }, {
#            'shapeID': 'ex:a', 
#            'propertyID': 'dct:date', 
#            'valueDataType': 'xsd:date'
#        },
#    ]
#
#    given_tapshapes = {
#        'shapes': [
#            {
#                'shape_warns': {},
#                'shapeID': 'default',
#                'shapeLabel': '',
#                'statement_templates': [
#                    { 'propertyID': 'dc:creator' },
#                    { 'propertyID': 'dc:type' }
#                ]
#            }
#        ]
#    }
#
#    expected_tapshapes = {
#        'namespaces': {
#            'ex:': 'http://example.org/',
#            'dct:': 'http://purl.org/dc/terms/',
#            'school:': 'http://school.example/#',
#            'xsd:': 'http://www.w3.org/2001/XMLSchema#',
#        },
#        'shapes': [
#            {
#                'shape_warns': {},
#                'shapeID': 'default',
#                'shapeLabel': '',
#                'statement_templates': [
#                    { 'propertyID': 'dc:creator' },
#                    { 'propertyID': 'dc:type' }
#                ]
#            }
#        ]
#    }
#
#    actual_tapshapes = _add_namespaces(
#        tapshapes=given_tapshapes,
#        config_dict=given_config_dict,
#        csvrows=given_csvrows,
#    )
#
#    assert actual_tapshapes == expected_tapshapes
