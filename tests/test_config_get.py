"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config, DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

YAML_CONFIGFILE_CONTENTS = """\
default_shape_name: ":default"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""

def test_get_config_from_default_config_file_if_present(tmp_path):
    """Get config dict from config file .dctaprc if present."""
    os.chdir(tmp_path)
    Path(DEFAULT_CONFIGFILE_NAME).write_text(YAML_CONFIGFILE_CONTENTS)
    assert get_config()["prefixes"] == {
        ":": "http://example.org/",
        "dcterms:": "http://purl.org/dc/terms/",
    }
    assert get_config() == {
        "default_shape_name": ":default",
        "prefixes": { ":": "http://example.org/",
                      "dcterms:": "http://purl.org/dc/terms/",
                    },
    }


def test_get_default_config_settings_if_configfile_not_found(tmp_path):
    """Get default config settings if no default config file is found."""
    os.chdir(tmp_path)
    assert get_config()["prefixes"]


def test_exit_if_configfile_has_bad_yaml(tmp_path):
    """Raise exception if config file has bad YAML."""
    os.chdir(tmp_path)
    BAD_CONFIG_YAML = "DELIBE\nRATELY BAD: -: ^^YAML CONTENT^^\n"
    Path(DEFAULT_CONFIGFILE_NAME).write_text(BAD_CONFIG_YAML)
    with pytest.raises(ConfigError):
        get_config()
