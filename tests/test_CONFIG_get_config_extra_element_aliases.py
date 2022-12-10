"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

NONDEFAULT_CONFIG_YAMLDOC = """\
extra_element_aliases:
    "ShapID": "shapeID"
"""

def test_get_config_file_extra_aliases(tmp_path):
    """Get extra element aliases from config file."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(NONDEFAULT_CONFIG_YAMLDOC)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "element_aliases" in config_dict               # computed and configurable
    assert "propertyid" in config_dict.get("element_aliases")
    assert "shapid" in config_dict.get("element_aliases")
