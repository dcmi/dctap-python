"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
import dctap
from dctap.config import get_config
from dctap.defaults import CONFIGFILE
from dctap.exceptions import ConfigError

def test_get_config_from_builtins(tmp_path):
    """Get config dict from built-in settings."""
    os.chdir(tmp_path)
    config_dict = get_config()
    assert config_dict.get("prefixes")                    # here: built-in defaults
    assert config_dict.get("csv_elements")                # computed from dataclasses
    assert config_dict.get("shape_elements")              # computed from dataclasses
    assert config_dict.get("statement_template_elements") # computed from dataclasses
    assert config_dict.get("element_aliases")             # computed from dataclasses
    assert ":" in config_dict.get("prefixes")             # built-in default
    assert "xsd:" in config_dict.get("prefixes")          # built-in default

@pytest.mark.skip
@pytest.mark.done
def test_get_config_from_default_config_file_if_present(tmp_path, capsys):
    """Get config dict from default config file CONFIGFILE if present."""
    os.chdir(tmp_path)
    nondefault_yaml = """
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    Path(CONFIGFILE).write_text(nondefault_yaml)
    assert Path(CONFIGFILE).is_file()
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
@pytest.mark.done
def test_get_config_from_passed_nondefault_yaml_even_if_prefixes_lack_colons():
    """Prefixes without colons are tolerated in YAML docs but added by get_config."""
    some_configyaml = """\
    default_shape_identifier: "default"
    prefixes:
        "": "http://example.org/"
        "dcterms": "http://purl.org/dc/terms/"
        "school": "http://school.example/#"
    """
    config_dict = get_config(config_yamlstring=some_configyaml)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")
    assert "dcterms:" in config_dict.get("prefixes")
    assert "school:" in config_dict.get("prefixes")

@pytest.mark.skip
@pytest.mark.done
def test_extra_shape_elements(tmp_path):
    """2022-05-13: Instructive issue with pytest, part II:

    os.chdir(tmp_path) is needed here because 
    a previous pytest (above) wrote a bad config file to tmp_path.
    """
    os.chdir(tmp_path) 
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    assert not Path(CONFIGFILE).is_file()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["shape_elements"].extend(config_dict["extra_shape_elements"])
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel", "closed", "start"]

@pytest.mark.skip(reason="Not implemented yet")
def test_exit_with_configerror_if_yamlstring_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if YAML string has bad YAML."""
    os.chdir(tmp_path)
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    with pytest.raises(ConfigError):
        get_config(config_yamlstring=bad_configyaml)

@pytest.mark.skip(reason="Not implemented yet")
def test_get_config_even_if_configfile_empty(tmp_path):
    """Get well-formed config dict even if config file is empty."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text("""###""")
    config_dict = get_config()
    assert Path(CONFIGFILE).is_file()
    assert config_dict.get("prefixes")                    # here: built-in defaults
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")                # computed
    assert config_dict.get("shape_elements")              # computed
    assert config_dict.get("statement_template_elements") # computed
    assert config_dict.get("element_aliases")             # asserted/computed
    assert config_dict.get("value_node_types") is None
    assert "school:" not in config_dict.get("prefixes")

@pytest.mark.skip(reason="Not implemented yet")
def test_warn_if_specified_configfile_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError) as err:
        get_config(config_yamlfile="passed_in_filename.yaml")
    assert "not found" in str(err.value)
    assert err.type == dctap.exceptions.ConfigError
    assert "No such" in str(err.value.__cause__)

@pytest.mark.skip(reason="Not implemented yet")
def test_exit_with_ConfigError_wtf(tmp_path):
    """2022-05-13: Instructive issue with pytest, part I:

    For this test to succeed, would need to change away from directory with bad 
    config file created in previous test (above).
    """
    with pytest.raises(ConfigError):
        get_config()

@pytest.mark.skip
def test_get_config_from_passed_nondefault_yaml_with_configyaml():
    """Works when passed YAML via configyaml, directly overriding @dctap_defaults."""
    some_configyaml = """\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    config_dict = get_config(configyaml=some_configyaml)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")

@pytest.mark.skip
def test_warn_about_bad_yaml_if_yaml_parsererror(tmp_path):
    """Get config dict from default config file CONFIGFILE if present."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text("""default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """)
    assert Path(CONFIGFILE).is_file()
    assert "default_shape_identifier" in Path(CONFIGFILE).read_text()
    config_dict = get_config()
    with pytest.raises(ConfigError):
        get_config()
    assert capsys.readouterr().out == f"YAML in 'dctap.yaml' is badly formed."

@pytest.mark.skip(reason="Not yet implemented")
def test_get_config_from_passed_nondefault_yaml_with_config_yamldoc():
    """
    Works when passed YAML via config_yamldoc, also overriding @dctap_defaults.

    2022-12-31 So why, one might ask, have both configyaml and config_yamldoc? 
    Because config_yamldoc can appear in function signature, while configyaml (which 
    normally would be passed by decorator), need not be declared in function 
    signature.
    """
    some_configyaml = """\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    config_dict = get_config(config_yamldoc=some_configyaml)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")

@pytest.mark.skip(reason="Not implemented yet")
def test_exit_with_ConfigError_if_default_configfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if default config file has bad YAML."""
    os.chdir(tmp_path)
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(CONFIGFILE).write_text(bad_configyaml)
    with pytest.raises(ConfigError):
        get_config()

@pytest.mark.skip(reason="Not implemented yet")
def test_exit_with_configerror_if_yamlfile_found_with_bad_yaml(tmp_path):
    """Exit with ConfigError if config file specified as argument has bad YAML."""
    os.chdir(tmp_path)
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(CONFIGFILE).write_text(bad_configyaml)
    with pytest.raises(ConfigError):
        get_config()
