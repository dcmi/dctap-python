"""See https://github.com/dcmi/dctap-python/issues/18#issue-1274937034 .

Phil is getting:
    Valid DCTAP CSV must have a 'propertyID' column.
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from dctap.config import get_config
from dctap.csvreader import csvreader, _get_rows
from dctap.defaults import DEFAULT_CONFIGFILE_NAME, DEFAULT_CONFIG_YAML

PHIL_CONFIG_YAMLDOC = """### dctap configuration file (in YAML format)
extra_statement_template_elements:
 - severity

element_aliases:
     "Mand": "mandatory"
     "Rep": "repeatable"
"""

@pytest.mark.skip
def test_get_config_with_extra_element_aliases():
    """Extra element aliases are added to existing aliases, not replacements."""
    given_config_dict = { "extra_element_aliases": { "Eigenschaftsidentifikator": "propertyID" } }
    config_dict = get_config()
    expected_config_dict = {
        "element_aliases": {
            'propertyid': 'propertyID',  
            'propertylabel': 'propertyLabel',  
            'eigenschaftsidentifikator': 'propertyID',  
        }
    }
    given_config_dict["element_aliases"].update(expected_mappings) == expected_config_dict["element_aliases"]
    given_config_dict == expected_config_dict

def test_get_config_from_phils_yamldoc(tmp_path):
    """Get config dict when passed Phil's YAML."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(PHIL_CONFIG_YAMLDOC)
    config_dict = get_config()
    assert config_dict["element_aliases"] == {'Mand': 'mandatory', 'Rep': 'repeatable'}
    assert config_dict["extra_statement_template_elements"] == [ 'severity' ]

def test_get_element_aliases_from_default_yamldoc(tmp_path):
    """Get config dict (with element aliases) directly from built-in defaults."""
    os.chdir(tmp_path)
    config_dict = get_config(config_yamldoc=DEFAULT_CONFIG_YAML)
    assert config_dict["element_aliases"]["propertyid"] == "propertyID"
    assert config_dict["element_aliases"]["mandatory"] == "mandatory"
    assert config_dict["element_aliases"]["repeatable"] == "repeatable"

@pytest.mark.skip
def test_get_tapshapes_dict_given_phils_yamldoc(tmp_path):
    """Get tapshape_dict with Phil's configuration."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(PHIL_CONFIG_YAMLDOC)
    (tapshapes_dict, warnings_dict) = csvreader(csvfile_obj, config_dict)

@pytest.mark.skip
def test_get_rows_phils_data(tmp_path):
    """Get list of rows, as dicts, from one-row, one-column CSV."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "PropertyID\n"
            "dct:title\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    expected_rows_list = [ {'propertyID': 'http://purl.org/dc/terms/creator'} ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict)
    assert actual_rows_list == expected_rows_list
