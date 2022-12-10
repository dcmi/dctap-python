"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

def test_get_config_file_extra_aliases(tmp_path):
    """Get extra element aliases from config file."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        "ShapID": "shapeID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "shapid" in config_dict.get("element_aliases")

def test_get_config_file_even_propertyid_can_be_aliased(tmp_path):
    """Even propertyID can be aliased."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        "PropID": "propertyID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "propid" in config_dict.get("element_aliases")
    assert config_dict["element_aliases"]["propid"] == "propertyID"

def test_get_config_file_extra_aliases_numbers_acceptable(tmp_path):
    """Numbers as dict keys are handled as strings."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        1: "shapeID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "1" in config_dict.get("element_aliases")

def test_get_config_file_extra_aliases_blank_strings_as_keys_are_acceptable(tmp_path):
    """Blank strings are acceptable as dict keys, even if it makes no sense."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        "": "shapeID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "" in config_dict.get("element_aliases")
    assert config_dict.get("element_aliases")[""] == "shapeID"

def test_get_extra_aliases_dict_none_harmless(tmp_path):
    """Harmless if YAML for extra_element_aliases evaluates to None."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")

def test_get_extra_aliases_list_value(tmp_path):
    """If YAML for extra_element_aliases is a list, converted to empty dict."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
    - one
    - two
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")

def test_get_extra_aliases_dict_handles_spaces_and_punctuation(tmp_path):
    """In addition to lowercasing, drops punctuation and spaces."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text("""
    extra_element_aliases:
        "S  h,apid": "shapeID"
        "   f  oo,BAR": "shapeID"
    """)
    config_dict = get_config()
    assert "extra_element_aliases" in config_dict
    assert "propertyid" in config_dict.get("element_aliases")
    assert "shapid" in config_dict.get("element_aliases")
    assert "foobar" in config_dict.get("element_aliases")
