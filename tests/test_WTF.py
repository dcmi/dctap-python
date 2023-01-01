"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import CONFIGFILE
from dctap.exceptions import ConfigError

@pytest.fixture(scope="session")
def tmp_dir(tmp_path_factory):
    # Create a unique temporary directory for the entire test session
    tmp_dir = tmp_path_factory.mktemp("test_session")
    return tmp_dir


@pytest.mark.skip(reason="Done!")
def test_get_config_from_passed_nondefault_yaml_with_config_yamldoc():
    """
    Works when passed YAML via config_yamldoc, also overriding @dctap_defaults.

    2022-12-31 So why, one might ask, have both configyaml and config_yamldoc? 
    Because config_yamldoc can appear in function signature, while configyaml (which 
    normally would be passed by decorator), need not be declared in function signature.
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


def test_exit_with_configerror_if_my_configfile_specified_but_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError) as fnfe:
        get_config()
    assert "not found" in str(fnfe.value)
    assert fnfe.type == FileNotFoundError
    assert "not found" in str(fnfe.value.__cause__)


