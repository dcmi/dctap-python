"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.csvreader import csvreader
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

def test_get_config_file_extra_aliases(tmp_path):
    """@@@@@@."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        "ShapID": "shapeID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "shapid" in config_dict.get("element_aliases")
