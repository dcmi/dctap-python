"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

NONDEFAULT_CONFIG_YAMLDOC = """\
default_shape_identifier: "default"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""


def test_get_config_from_builtins(tmp_path):
    """Get config dict from built-in settings."""
    config_dict = get_config()
    assert "prefixes" in list(config_dict.keys())                 # built-in/configurable
    assert config_dict.get("csv_elements")                        # computed from dataclasses
    assert config_dict.get("shape_elements")                      # computed from dataclasses
    assert config_dict.get("statement_constraint_elements")       # computed from dataclasses
    assert config_dict.get("element_aliases")                     # computed/configurable
    ## The following are commented out in the built-in configuration
    # assert config_dict.get("default_shape_identifier")            # configurable with built-in default
    # assert config_dict.get("picklist_item_separator")             # configurable with built-in default
    # assert config_dict.get("extra_statement_constraint_elements") # configurable
    # assert config_dict.get("extra_shape_elements")                # configurable
    # assert config_dict.get("extra_value_node_types")              # configurable
    # assert config_dict.get("picklist_elements")                   # configurable

def test_get_config_from_default_config_file_if_present(tmp_path):
    """Get config dict from config file DEFAULT_CONFIGFILE_NAME if present."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(NONDEFAULT_CONFIG_YAMLDOC)
    config_dict = get_config()
    assert "prefixes" in list(config_dict.keys())
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")                       # computed
    assert config_dict.get("shape_elements")                     # computed
    assert config_dict.get("statement_constraint_elements")      # computed
    assert config_dict.get("element_aliases")                    # asserted/computed
    assert config_dict.get("value_node_types") is None

def test_get_config_from_nondefault_yaml(tmp_path):
    """Get config dict when passed non-default YAML."""
    config_dict = get_config(config_yamldoc=NONDEFAULT_CONFIG_YAMLDOC)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")

def test_exit_with_ConfigError_if_configfile_specified_but_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError):
        get_config(configfile_name="dctap.yml")

def test_exit_with_ConfigError_if_specified_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if config file specified as argument has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    nondefault_configfile_name = "dctap_settings.yml"
    Path(nondefault_configfile_name).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config(configfile_name=nondefault_configfile_name)

def test_exit_with_ConfigError_if_default_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if default config file has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(DEFAULT_CONFIGFILE_NAME).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config()
