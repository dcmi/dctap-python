"""In getting rows: compute alias-to-element aliases from config dict."""

from dctap.config import _alias2element_mappings


def test_config_get__alias2element_mappings():
    """Given config_dict["extra_element_aliases"] (asserted), add computed aliases."""
    csv_elements_list = [ "propertyID", "propertyLabel" ]
    expected_mappings = {'propertyid': 'propertyID', 'propertylabel': 'propertyLabel'}
    computed_mappings = _alias2element_mappings(csv_elements_list)
    assert expected_mappings == computed_mappings
