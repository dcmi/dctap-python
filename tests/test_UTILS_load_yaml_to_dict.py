"""
Tests utils.load_yaml_to_dict

Args - accepts one of following::
- yamlstr
- yaml_filename

Works by 
"""

import os
from pathlib import Path
import pytest
from dctap.exceptions import ConfigError
from dctap.utils import load_yaml_to_dict



def test_load_yaml_to_dict_from_yamlstring():
    """Load YAML from string into Python dict."""
    good_config_yaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    output_dict = load_yaml_to_dict(good_config_yaml)
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")


def test_load_yaml_to_dict_from_pathobj(tmp_path):
    """Load YAML from Path object into Python dict."""
    good_config_yaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    os.chdir(tmp_path)
    pathobj = Path("config.yaml")
    pathobj.write_text(good_config_yaml)
    output_dict = load_yaml_to_dict(pathobj)
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")


def test_load_yaml_to_dict_from_yaml_filename(tmp_path):
    """Load YAML from filename into Python dict."""
    good_config_yaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    os.chdir(tmp_path)
    pathobj = Path("config.yaml")
    pathobj.write_text(good_config_yaml)
    output_dict = load_yaml_to_dict(yaml_filename="config.yaml")
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")


def test_exit_with_configerror_if_configfile_has_dict_with_duplicate_keys():
    """Exit with ConfigError if config file has dict with duplicate keys."""
    bad_config_yaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
    """
    with pytest.raises(ConfigError):
        load_yaml_to_dict(bad_config_yaml)


def test_load_yaml_to_dict_from_passed_some_config_yaml():
    """Get config dict when passed some config YAML."""
    some_config_yamlstring = """\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    output_dict = load_yaml_to_dict(some_config_yamlstring)
    assert output_dict.get("prefixes")
    assert output_dict.get("default_shape_identifier")
    assert ":" in output_dict.get("prefixes")
