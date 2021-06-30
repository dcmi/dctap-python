"""Writes starter configuration file (YAML format)."""

import os
import pytest
from pathlib import Path
from dctap.config import DEFAULT_CONFIG_YAML, DEFAULT_CONFIGFILE_NAME, write_configfile


def test_write_default_configfile_and_read_back(tmp_path):
    """Write DEFAULT_CONFIG_YAML to DEFAULT_CONFIGFILE_NAME and read back as text."""
    os.chdir(tmp_path)
    write_configfile()
    assert open(DEFAULT_CONFIGFILE_NAME).read() == DEFAULT_CONFIG_YAML


def test_write_specified_configfile_and_read_back(tmp_path):
    """Write specified configfile and read back as text."""
    os.chdir(tmp_path)
    specified_configfile = "dctap.yaml"
    write_configfile(specified_configfile)
    assert open(specified_configfile).read() == DEFAULT_CONFIG_YAML


def test_not_write_default_configfile_if_already_exists(tmp_path):
    """Exits with error if DEFAULT_CONFIGFILE_NAME already exists."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_configfile()

def test_not_write_specified_configfile_if_already_exists(tmp_path):
    """Exits with error if specified configfile already exists."""
    os.chdir(tmp_path)
    os.mkdir("config")
    configfile = "config/dctap.yaml"
    Path(configfile).write_text("Config stuff")
    with pytest.raises(SystemExit):
        write_configfile("config/dctap.yaml")


def test_not_write_specified_configfile_if_not_writeable(tmp_path):
    """Exits with error if specified configfile cannot be written."""
    os.chdir(tmp_path)
    configfile = "config/dctap.yaml"
    with pytest.raises(SystemExit):
        write_configfile("config/dctap.yaml")

