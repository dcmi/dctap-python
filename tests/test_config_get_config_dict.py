"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config_dict
from dctap.exceptions import BadYamlError, ConfigWarning

DEFAULT_CONFIGFILE_NAME = ".dctaprc"

ALT_CONFIG_YAML = """\
prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""


# def test_get_config_dict_from_default_config_file_if_present(tmp_path):
#     """Get config dict from config file .dctaprc if present."""
#     os.chdir(tmp_path)
#     assert get_config_dict()["prefixes"] == {
#         ":": "http://example.org/",
#         "dct:": "http://purl.org/dc/terms/",
#     }
#     assert get_config_dict() == {
#         "prefixes": {":": "http://example.org/", "dct:": "http://purl.org/dc/terms/"},
#         "valueNodeType": ["URI", "BNode", "Nonliteral"],
#         "valueConstraintType": ["UriStem", "LitPicklist"],
#     }
# TEST_CONFIGFILE_NAME = ".dctaprc"
# 
# TEST_DEFAULT_CONFIG_SETTINGS_YAML = """\
# prefixes:
#     ":": "http://example.org/"
#     "dct:": "http://purl.org/dc/terms/"
# 
# valueConstraintType:
# - UriStem
# - LitPicklist
# """
# 

@pytest.fixture()
def dir_with_dctaprc(tmp_path):
    """Set up directory with simple config file for use as pytest fixture."""
    os.chdir(tmp_path)
    Path(TEST_CONFIGFILE_NAME).write_text(TEST_DEFAULT_CONFIG_SETTINGS_YAML)
    return Path.cwd()


def test_get_default_config_settings_if_configfile_not_found(tmp_path):
    """Get default config settings if no default config file is found."""
    os.chdir(tmp_path)
    assert get_config_dict(default_config_yaml=ALT_CONFIG_YAML)["prefixes"] == {
        ":": "http://example.org/",
        "dcterms:": "http://purl.org/dc/terms/",
    }


def test_exit_if_configfile_has_bad_yaml(tmp_path):
    """Raise exception if config file has bad YAML."""
    os.chdir(tmp_path)
    configfile_content = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(DEFAULT_CONFIGFILE_NAME).write_text(configfile_content)
    assert get_config_dict(default_config_yaml=ALT_CONFIG_YAML)[
        "prefixes"
    ] == {
        ":": "http://example.org/",
        "dcterms:": "http://purl.org/dc/terms/",
    }
    # with pytest.raises(ConfigWarning):
    #    get_config_dict()
