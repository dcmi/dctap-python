"""In getting rows: compute alias-to-element aliases from config dict."""


import pytest
from dctap.config import _get_aliases_dict


def test_config_get__alias2element_mappings():
    """Get basic computed aliases (lowercased)."""

    csv_elements_list = ["propertyID", "propertyLabel"]
    expected_mappings = {"propertyid": "propertyID", "propertylabel": "propertyLabel"}
    assert _get_aliases_dict(csv_elements_list) == expected_mappings
