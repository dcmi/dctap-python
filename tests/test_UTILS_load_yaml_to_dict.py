"""
Tests utils.load_yaml_to_dict

Args - just one of the following (or none):
- yamlstring
- yamlfile
"""

import os
from pathlib import Path
import pytest
from dctap.defaults import CONFIGFILE
from dctap.exceptions import ConfigError
from dctap.utils import load_yaml_to_dict

def test_return_none_if_yaml_in_configfile_gets_parser_error(tmp_path, capsys):
    """Return None if given configfile gets YAML parser error."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text(
        """default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    )
    assert load_yaml_to_dict(yamlfile=CONFIGFILE) is None
    assert capsys.readouterr().err == "YAML in 'dctap.yaml' is badly formed.\n"

def test_return_none_if_yaml_in_configfile_is_bad(tmp_path):
    """Return None if given configfile has bad YAML."""
    os.chdir(tmp_path)
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(CONFIGFILE).write_text(bad_configyaml)
    assert load_yaml_to_dict(yamlfile=CONFIGFILE) is None

def test_return_none_if_specified_yamlstring_is_bad_yaml():
    """Return None if specified YAML string has bad YAML."""
    bad_configyaml = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    assert load_yaml_to_dict(yamlstring=bad_configyaml) is None

def test_warn_if_configfile_not_found(tmp_path, capsys):
    """Warn if specified config file not found."""
    os.chdir(tmp_path)
    x = load_yaml_to_dict(yamlfile=CONFIGFILE)
    assert capsys.readouterr().err == f"File '{CONFIGFILE}' not found.\n"

def test_load_yaml_to_dict_from_yamlstring_when_string_empty():
    """Return None if passed YAML string is empty or devoid of YAML content"""
    assert load_yaml_to_dict(yamlstring="") is None
    assert load_yaml_to_dict(yamlstring="###") is None

def test_load_yaml_to_dict_from_yamlstring():
    """If YAML string is good, convert into Python dict."""
    good_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    output_dict = load_yaml_to_dict(yamlstring=good_configyaml)
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")

def test_load_yaml_to_dict_from_pathobj(tmp_path):
    """If YAML string in given Path object is good, convert into Python dict."""
    good_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    os.chdir(tmp_path)
    pathobj = Path("config.yaml")
    pathobj.write_text(good_configyaml)
    output_dict = load_yaml_to_dict(pathobj)
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")

def test_load_yaml_to_dict_from_yamlfile(tmp_path):
    """If YAML string in given filename is good, convert into Python dict."""
    good_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    os.chdir(tmp_path)
    Path("config.yaml").write_text(good_configyaml)
    assert Path("config.yaml").is_file()
    output_dict = load_yaml_to_dict(yamlfile="config.yaml")
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")

def test_exit_with_badyamlerror_if_configfile_has_dict_with_duplicate_keys(capsys):
    """Warn that YAML badly formed if config file has dict with duplicate keys."""
    bad_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
    """
    assert load_yaml_to_dict(yamlstring=bad_configyaml) is None
    assert capsys.readouterr().err == "YAML is badly formed.\n"

def test_load_yaml_to_dict_from_passed_some_configyaml():
    """Get config dict when passed some config YAML."""
    some_configyaml = """\
    default_shape_identifier: "default"
    prefixes:
        ":": "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "school:": "http://school.example/#"
    """
    output_dict = load_yaml_to_dict(some_configyaml)
    assert output_dict.get("prefixes")
    assert output_dict.get("default_shape_identifier")
    assert ":" in output_dict.get("prefixes")
