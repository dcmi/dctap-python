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
