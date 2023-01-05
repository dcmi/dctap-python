"""In getting rows: normalize element names (CSV header) as per config_config."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _normalize_element_name


def test_normalize_element_name():
    """Element names not recognized as aliases are left unchanged."""
    config_dict = get_config()
    element_aliases_dict = config_dict.get("element_aliases")
    assert _normalize_element_name("SHAPE ID", element_aliases_dict) == "shapeID"
    assert _normalize_element_name("SHAPE___ID", element_aliases_dict) == "shapeID"
    assert _normalize_element_name("rid", element_aliases_dict) == "rid"

def test_normalize_element_name_customized():
    """Uses customized element name aliases taken from configuration file."""
    element_aliases_dict = {
        "propertyid": "propertyID",
        "eigenschaftsidentifikator": "propertyID",
    }
    assert _normalize_element_name("propertyid", element_aliases_dict) == "propertyID"
    assert (
        _normalize_element_name("eigenschaftsidentifikator", element_aliases_dict)
        == "propertyID"
    )

def test_normalize_element_name_if_element_aliases_dict_pass_through_unchanged():
    """
    If no element aliases dict passed to function, pass element name through unchanged.
    Normally, this should not happen because these are computed and configurable.
    """
    assert _normalize_element_name("propertyid") == "propertyid"
    assert (
        _normalize_element_name("eigenschaftsidentifikator")
        == "eigenschaftsidentifikator"
    )
