"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError


def test_extra_shape_elements(tmp_path):
    """Add extra shape elements to config dict.

    Note 2022-05-13: os.chdir(tmp_path) is needed here because 
    previous pytest wrote a bad config file to tmp_path.
    It appears that this test, to succeed, needs to change 
    away from the directory with that bad config file.
    """
    os.chdir(tmp_path) 
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["shape_elements"].extend(config_dict["extra_shape_elements"])
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel", "closed", "start"]
