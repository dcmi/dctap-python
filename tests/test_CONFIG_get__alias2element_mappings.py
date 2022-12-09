"""In getting rows: compute alias-to-element aliases from config dict."""


from dctap.config import _alias2element_mappings


def test_config_get__alias2element_mappings():
    """Get basic computed aliases (lowercased)."""

    csv_elements_list = [ "propertyID", "propertyLabel" ]
    expected_mappings = {'propertyid': 'propertyID', 'propertylabel': 'propertyLabel'}
    assert _alias2element_mappings(csv_elements_list) == expected_mappings
