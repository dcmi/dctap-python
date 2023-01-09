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
    assert config_dict.get("prefixes")  # here: built-in defaults
    assert config_dict.get("csv_elements")  # computed from dataclasses
    assert config_dict.get("shape_elements")  # computed from dataclasses
    assert config_dict.get("statement_template_elements")  # computed from dataclasses
    assert config_dict.get("element_aliases")  # computed from dataclasses
    assert ":" in config_dict.get("prefixes")  # built-in default
    assert "xsd:" in config_dict.get("prefixes")  # built-in default

def test_get_config_from_passed_nondefault_yaml():
    """Passed nondefault YAML."""
    some_configyaml = """
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    config_dict = get_config(nondefault_configyaml_str=some_configyaml)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")

def test_assigned_default_if_get_config_passed_yaml_with_empty_shapeid(tmp_path):
    """If passed YAML with empty shape ID, assigned 'default'."""
    os.chdir(tmp_path)
    some_configyaml = """
    default_shape_identifier: ""
    """
    config_dict = get_config(nondefault_configyaml_str=some_configyaml)
    assert config_dict.get("default_shape_identifier") == "default"

def test_get_config_from_default_configfile(tmp_path):
    """Get config dict from default config file CONFIGFILE if present."""
    os.chdir(tmp_path)
    nondefault_yaml = """
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    extra_value_node_types:
    - literal
    """
    Path(CONFIGFILE).write_text(nondefault_yaml)
    assert Path(CONFIGFILE).is_file()
    config_dict = get_config()
    assert config_dict.get("prefixes")  # here: from dctap.yaml
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")  # computed
    assert config_dict.get("shape_elements")  # computed
    assert config_dict.get("statement_template_elements")  # computed
    assert config_dict.get("element_aliases")  # asserted/computed
    assert config_dict.get("extra_value_node_types") == ["literal"]
    assert "school:" in config_dict.get("prefixes")

def test_get_config_from_nondefault_configfile_if_specified(tmp_path):
    """Get config dict from nondefault config file CONFIGFILE if specified."""
    os.chdir(tmp_path)
    nondefault_configfile_name = "nondefault.yaml"
    nondefault_yaml = """
    default_shape_identifier: "default"
    prefixes:
        "": "http://example.org/"
        "dcterms": "http://purl.org/dc/terms/"
        "school": "http://school.example/#"
    extra_element_aliases:
        "ShapID": "shapeID"
    """
    Path(nondefault_configfile_name).write_text(nondefault_yaml)
    assert Path(nondefault_configfile_name).is_file()
    config_dict = get_config(nondefault_configfile_name=nondefault_configfile_name)
    assert config_dict["extra_element_aliases"]["ShapID"] == "shapeID"
    # Correctly adds colons to prefixes if necessary.
    assert "school:" in config_dict.get("prefixes")
    assert ":" in config_dict.get("prefixes")

def test_get_config_from_passed_nondefault_yaml_even_if_prefixes_lack_colons():
    """Prefixes without colons are tolerated in YAML docs but added by get_config."""
    some_configyaml = """\
    default_shape_identifier: "default"
    prefixes:
        "": "http://example.org/"
        "dcterms": "http://purl.org/dc/terms/"
        "school": "http://school.example/#"
    """
    config_dict = get_config(nondefault_configyaml_str=some_configyaml)
    assert config_dict.get("prefixes")
    assert config_dict.get("default_shape_identifier")
    assert ":" in config_dict.get("prefixes")
    assert "dcterms:" in config_dict.get("prefixes")
    assert "school:" in config_dict.get("prefixes")

def test_extra_shape_elements(tmp_path):
    """Has extra_shape_elements."""
    os.chdir(tmp_path)
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    assert not Path(CONFIGFILE).is_file()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["shape_elements"].extend(config_dict["extra_shape_elements"])
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel", "closed", "start"]

def test_warn_if_specify_both_nondefault_yamlstring_and_yamlfile(tmp_path):
    """Exit with ConfigError if get_config specifies both YAML string and YAML file."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError) as err:
        get_config(
            nondefault_configfile_name="passed_in_filename.yaml",
            nondefault_configyaml_str="passed_in_yaml_string",
        )

def test_warn_if_specified_configfile_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(ConfigError) as err:
        get_config(nondefault_configfile_name="passed_in_filename.yaml")
    assert "not found" in str(err.value)
    assert err.type == dctap.exceptions.ConfigError
    assert "No such" in str(err.value.__cause__)

def test_warn_about_bad_yaml_if_yaml_parsererror(tmp_path, capsys):
    """Get config dict from default config file CONFIGFILE if present."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text(
        """default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    )
    assert Path(CONFIGFILE).is_file()
    assert "default_shape_identifier" in Path(CONFIGFILE).read_text(encoding="utf-8")
    config_dict = get_config()
    assert capsys.readouterr().err == "YAML is badly formed.\n"

def test_warn_of_bad_yaml_if_configfile_empty(tmp_path, capsys):
    """Get well-formed config dict even if config file is empty."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text("""###""")
    config_dict = get_config()
    assert Path(CONFIGFILE).is_file()
    assert Path(CONFIGFILE).read_text(encoding="utf-8") == "###"
    assert config_dict
    assert config_dict.get("default_shape_identifier")
    assert config_dict.get("csv_elements")  # computed
    assert config_dict.get("shape_elements")  # computed
    assert config_dict.get("statement_template_elements")  # computed
    assert config_dict.get("element_aliases")  # asserted/computed
    assert config_dict.get("value_node_types") is None
    assert capsys.readouterr().err == ""

def test_warn_if_yamlfile_found_with_bad_yaml(tmp_path, capsys):
    """Exit with ConfigError if config file specified as argument has bad YAML."""
    os.chdir(tmp_path)
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(CONFIGFILE).write_text(bad_configyaml)
    x = get_config()
    assert capsys.readouterr().err == "YAML is badly formed.\n"

def test_warn_if_yamlstring_found_with_bad_yaml(capsys):
    """Warn if passed-in YAML string has bad YAML."""
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    get_config(nondefault_configyaml_str=bad_configyaml)
    assert capsys.readouterr().err == "YAML is badly formed.\n"
