"""
Tests utils.load_yaml_to_dict

Args - accepts one of following::
- yamlstr
- yamlfile

Works by 
"""

import os
from pathlib import Path
import pytest
from dctap.defaults import CONFIGFILE
from dctap.exceptions import ConfigError
from dctap.utils import load_yaml_to_dict


@pytest.mark.done
def test_exit_with_filenotfounderror_if_configfile_not_found(tmp_path, capsys):
    """Exit with FileNotFoundError if config file not found."""
    os.chdir(tmp_path)
    x = load_yaml_to_dict(yamlfile=CONFIGFILE)
    # assert 'not found' in capsys.readouterr().out

@pytest.mark.done
def test_load_yaml_to_dict_from_yamlstring_when_string_empty():
    """But what if the passed YAML string is 'empty'?"""
    assert load_yaml_to_dict(yamlstring="") == None
    assert load_yaml_to_dict(yamlstring="###") == None


@pytest.mark.done
def test_load_yaml_to_dict_from_yamlstring():
    """Load YAML from string into Python dict."""
    good_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "dc:":      "http://purl.org/dc/terms/"
    """
    output_dict = load_yaml_to_dict(yamlstring=good_configyaml)
    assert output_dict.get("prefixes")
    assert "dc:" in output_dict.get("prefixes")
    assert "xsd:" in output_dict.get("prefixes")


@pytest.mark.done
def test_load_yaml_to_dict_from_pathobj(tmp_path):
    """Load YAML from Path object into Python dict."""
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


@pytest.mark.done
def test_load_yaml_to_dict_from_yamlfile(tmp_path):
    """Load YAML from filename into Python dict."""
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

@pytest.mark.done
def test_exit_with_configerror_if_configfile_has_dict_with_duplicate_keys():
    """Exit with ConfigError if config file has dict with duplicate keys."""
    bad_configyaml = """
    prefixes:
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"
    """
    with pytest.raises(ConfigError):
        load_yaml_to_dict(bad_configyaml)



@pytest.mark.done
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
