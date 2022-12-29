"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import CONFIGFILE1
from dctap.exceptions import ConfigError


@pytest.mark.skip
def test_get_config_from_passed_nondefault_yaml_even_if_prefixes_lack_colons():
    """Prefixes without colons are tolerated in YAML docs but added by get_config."""
    some_config_yamlstring = """\
    default_shape_identifier: "default"
    prefixes:
        "": "http://example.org/"
        "dcterms": "http://purl.org/dc/terms/"
        "school": "http://school.example/#"
    """
    config_dict = get_config(config_yamldoc=some_config_yamlstring)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")
    assert "dcterms:" in config_dict.get("prefixes")
    assert "school:" in config_dict.get("prefixes")


@pytest.mark.skip
def test_get_config_from_builtins():
    """Get config dict from built-in settings."""
    config_dict = get_config()
    assert config_dict.get("prefixes")                    # here: built-in defaults
    assert config_dict.get("csv_elements")                # computed from dataclasses
    assert config_dict.get("shape_elements")              # computed from dataclasses
    assert config_dict.get("statement_template_elements") # computed from dataclasses
    assert config_dict.get("element_aliases")             # computed from dataclasses
    assert ":" in config_dict.get("prefixes")             # built-in default
    assert "xsd:" in config_dict.get("prefixes")          # built-in default
    assert "school:" not in config_dict.get("prefixes")


@pytest.mark.skip
def test_get_config_from_default_config_file_even_if_empty(tmp_path):
    """Get well-formed config dict even if config file is empty."""
    os.chdir(tmp_path)
    Path(CONFIGFILE1).write_text("""###""")
    config_dict = get_config()
    assert config_dict.get("prefixes")                    # here: built-in defaults
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")                # computed
    assert config_dict.get("shape_elements")              # computed
    assert config_dict.get("statement_template_elements") # computed
    assert config_dict.get("element_aliases")             # asserted/computed
    assert config_dict.get("value_node_types") is None
    assert "school:" not in config_dict.get("prefixes")


@pytest.mark.skip
def test_get_config_from_default_config_file_if_present(tmp_path):
    """Get config dict from config file CONFIGFILE1 if present."""
    os.chdir(tmp_path)
    Path(CONFIGFILE1).write_text("""\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """)
    config_dict = get_config()
    assert config_dict.get("prefixes")                    # here: from dctap.yaml
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")                # computed
    assert config_dict.get("shape_elements")              # computed
    assert config_dict.get("statement_template_elements") # computed
    assert config_dict.get("element_aliases")             # asserted/computed
    assert config_dict.get("value_node_types") is None
    assert "school:" in config_dict.get("prefixes")


@pytest.mark.skip
def test_get_config_from_passed_nondefault_yaml():
    """Get config dict when passed non-default YAML."""
    some_config_yamlstring = """\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    config_dict = get_config(config_yamldoc=some_config_yamlstring)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")


@pytest.mark.skip
def test_exit_with_configerror_if_configfile_specified_but_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError):
        get_config(configfile1="dctap.yaml")


@pytest.mark.skip
def test_exit_with_configerror_if_specified_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if config file specified as argument has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    nondefault_configfile_name = "dctap_settings.yml"
    Path(nondefault_configfile_name).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config(configfile_name=nondefault_configfile_name)


@pytest.mark.skip
def test_exit_with_ConfigError_if_default_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if default config file has bad YAML."""
    os.chdir(tmp_path)
    bad_config_yaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(CONFIGFILE1).write_text(bad_config_yaml)
    with pytest.raises(ConfigError):
        get_config()


@pytest.mark.skip
def test_exit_with_ConfigError_wtf(tmp_path):
    """2022-05-13: Instructive issue with pytest, part I:

    For this test to succeed, would need to change away from directory with bad 
    config file created in previous test (above).
    """
    with pytest.raises(ConfigError):
        get_config()


@pytest.mark.skip
def test_extra_shape_elements(tmp_path):
    """2022-05-13: Instructive issue with pytest, part II:

    os.chdir(tmp_path) is needed here because 
    a previous pytest (above) wrote a bad config file to tmp_path.
    """
    os.chdir(tmp_path) 
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["shape_elements"].extend(config_dict["extra_shape_elements"])
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel", "closed", "start"]
