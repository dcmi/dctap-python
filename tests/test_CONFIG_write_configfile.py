"""Write starter YAML configuration file."""

import os
import pytest
from pathlib import Path
from dctap.config import write_configfile
from dctap.defaults import CONFIGFILE
from dctap.exceptions import ConfigError

NONDEFAULT_CONFIGYAML = """\
default_shape_identifier: "default"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""


def test_write_default_configfile_and_read_back(tmp_path):
    """Write DEFAULT_CONFIGYAML to CONFIGFILE and read back as text."""
    os.chdir(tmp_path)
    write_configfile(nondefault_configyaml_str=NONDEFAULT_CONFIGYAML)
    assert open(CONFIGFILE).read() == NONDEFAULT_CONFIGYAML


def test_write_specified_configfile_and_read_back(tmp_path):
    """Write specified configfile and read back as text."""
    os.chdir(tmp_path)
    specified_config_file = "foobar.yaml"
    write_configfile(
        default_configfile_name=specified_config_file,
        nondefault_configyaml_str=NONDEFAULT_CONFIGYAML,
    )
    assert open(specified_config_file).read() == NONDEFAULT_CONFIGYAML


def test_not_write_default_configfile_if_already_exists(tmp_path):
    """Exits if config file not specified and CONFIGFILE already exists."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_configfile()


def test_exits_if_file_not_writeable(tmp_path):
    """Exits if config file not writeable. Note: throws two exceptions."""
    os.chdir(tmp_path)
    config_filename = "/asdf/asdf/asdf/asdf/foobar.yaml"
    with pytest.raises(SystemExit):
        write_configfile(
            default_configfile_name=config_filename,
            nondefault_configyaml_str=NONDEFAULT_CONFIGYAML,
        )
    with pytest.raises(ConfigError):
        write_configfile(
            default_configfile_name=config_filename,
            nondefault_configyaml_str=NONDEFAULT_CONFIGYAML,
        )
