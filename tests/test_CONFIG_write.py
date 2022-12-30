"""Write starter YAML configuration file."""

import os
import pytest
from pathlib import Path
from dctap.config import write_configfile
from dctap.defaults import CONFIGFILE

NONDEFAULT_CONFIGYAML = """\
default_shape_identifier: "default"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""

def test_write_default_configfile_and_read_back(tmp_path):
    """Write DEFAULT_CONFIGYAML to CONFIGFILE and read back as text."""
    os.chdir(tmp_path)
    write_configfile(
        configfile_name=CONFIGFILE, 
        configyaml=NONDEFAULT_CONFIGYAML)
    assert open(CONFIGFILE).read() == NONDEFAULT_CONFIGYAML

def test_write_specified_configfile_and_read_back(tmp_path):
    """Write specified configfile and read back as text."""
    os.chdir(tmp_path)
    specified_config_file = "dctap.yaml"
    write_configfile(
        configfile_name=specified_config_file, 
        configyaml=NONDEFAULT_CONFIGYAML
    )
    assert open(specified_config_file).read() == NONDEFAULT_CONFIGYAML

def test_not_write_default_configfile_if_already_exists(tmp_path):
    """Exits if config file not specified and CONFIGFILE already exists."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_configfile(
            configfile_name=CONFIGFILE, 
            configyaml=NONDEFAULT_CONFIGYAML
        )

def test_not_write_specified_configfile_if_already_exists(tmp_path):
    """Exits if config file specified and already exists."""
    os.chdir(tmp_path)
    os.mkdir("config")
    config_file = "config/dctap.yaml"
    Path(config_file).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_configfile(
            configfile_name="config/dctap.yaml", 
            configyaml=NONDEFAULT_CONFIGYAML
        )

def test_exits_if_specified_configfile_writeable(tmp_path):
    """Exits with error if specified configfile cannot be written."""
    os.chdir(tmp_path)
    config_file = "config/dctap.yaml"
    with pytest.raises(SystemExit):
        write_configfile(
            configfile_name="config/dctap.yaml", 
            configyaml=NONDEFAULT_CONFIGYAML
        )
