"""In getting rows: get customized element aliases from config dict."""

from dctap.config import _compute_alias2element_mappings


def test_config_get__compute_alias2element_mappings():
    """Given config_dict["element_aliases"] (asserted), add computed aliases."""
    csv_elements_list = [ "propertyID", "propertyLabel" ]
    expected_mappings = {'pid': 'propertyID', 'propertyid': 'propertyID', 'pl': 'propertyLabel', 'propertylabel': 'propertyLabel'}
    computed_mappings = _compute_alias2element_mappings(csv_elements_list)
    assert expected_mappings == computed_mappings
    given_config_dict = { "element_aliases": { "Eigenschaftsidentifikator": "propertyID" }}
    expected_config_dict = {
        "element_aliases": {
            'propertyid': 'propertyID',  
            'pid': 'propertyID',  
            'pl': 'propertyLabel',  
            'propertylabel': 'propertyLabel',  
            'eigenschaftsidentifikator': 'propertyID',  
        }
    }
    given_config_dict["element_aliases"].update(expected_mappings) == expected_config_dict["element_aliases"]
    given_config_dict == expected_config_dict
