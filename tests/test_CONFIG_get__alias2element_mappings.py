"""In getting rows: compute alias-to-element aliases from config dict."""

from dctap.config import _alias2element_mappings


def test_config_get__alias2element_mappings():
    """Given config_dict["element_aliases"] (asserted), add computed aliases."""
    csv_elements_list = [ "propertyID", "propertyLabel" ]
    expected_mappings = {'propertyid': 'propertyID', 'propertylabel': 'propertyLabel'}
    computed_mappings = _alias2element_mappings(csv_elements_list)
    assert expected_mappings == computed_mappings
    given_config_dict = { "element_aliases": { "Eigenschaftsidentifikator": "propertyID" }}
    expected_config_dict = {
        "element_aliases": {
            'propertyid': 'propertyID',  
            'propertylabel': 'propertyLabel',  
            'eigenschaftsidentifikator': 'propertyID',  
        }
    }
    given_config_dict["element_aliases"].update(expected_mappings) == expected_config_dict["element_aliases"]
    given_config_dict == expected_config_dict
