"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import (
    get_config,
    DEFAULT_CONFIGFILE_NAME,
    DEFAULT_CONFIG_YAML,
)
from dctap.exceptions import ConfigError

YAML_CONFIGFILE_CONTENTS = """\
default_shape_name: ":default"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""


def test_get_config_from_default_config_file_if_present(tmp_path):
    """Get config dict from config file DEFAULT_CONFIGFILE_NAME if present."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(YAML_CONFIGFILE_CONTENTS)
    config_dict = get_config()
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_name")
    assert config_dict.get("csv_elements")
    assert config_dict.get("shape_elements")
    assert config_dict.get("statement_constraint_elements")
    assert config_dict.get("element_aliases")
    assert config_dict.get("value_node_types") is None

def test_exit_with_ConfigError_if_configfile_specified_but_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError):
        get_config(config_file="dctap.yml")

def test_exit_with_ConfigError_if_specified_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if config file specified as argument has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    nondefault_configfile_name = "dctap_settings.yml"
    Path(nondefault_configfile_name).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config(config_file=nondefault_configfile_name)

def test_exit_with_ConfigError_if_default_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if default config file has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(DEFAULT_CONFIGFILE_NAME).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config()
