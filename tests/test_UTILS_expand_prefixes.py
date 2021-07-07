"""Verify that string is valid as URL."""

import os
import pytest
from dctap.utils import expand_uri_prefixes


def test_utils_expand_uri_prefixes(tmp_path):
    """Expands prefixes in shapes dictionary according as per config settings."""
    config_dict = {
    "default_shape_name": ":default",
    "prefixes": { ":": "http://example.org/",
                  "dcterms:": "http://purl.org/dc/terms/",
                  "wdt:": "http://www.wikidata.org/prop/direct/",
                  "foaf:": "http://xmlns.com/foaf/0.1/"
                 }
    }
    shapes_dict = {'shapes':  
        [
            {
              'shapeID': ':book',
              'statement_constraints': [
                    { 
                      'propertyID': 'dcterms:creator',
                      'valueShape': ':author' 
                    }, 
                    {
                      'propertyID': 'wdt:P1476'
                    }
              ]
            }, 
            {
              'shapeID': ':author',
              'statement_constraints': [
                    {
                      'propertyID': 'foaf:name',
                      'valueDataType': 'xsd:string'
                    }
               ]
            }
        ]
    }
    expected_output = {'shapes': 
        [
            {
              'shapeID': 'http://example.org/book',
              'statement_constraints': [
                    {
                      'propertyID': 'http://purl.org/dc/terms/creator',
                      'valueShape': 'http://example.org/author'
                    },
                    {
                      'propertyID': 'http://www.wikidata.org/prop/direct/P1476'
                    }
                ]
            },
            {
              'shapeID': 'http://example.org/author',
              'statement_constraints': [
                    {
                      'propertyID': 'http://xmlns.com/foaf/0.1/name',
                      'valueDataType': 'xsd:string'
                    }
                ]
            }
        ]
    }
    assert expand_uri_prefixes(shapes_dict, config_dict) == expected_output
