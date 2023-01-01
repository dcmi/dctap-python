"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from ruamel.yaml import YAML, YAMLError
from dctap.config import get_config
from dctap.defaults import CONFIGFILE, dctap_defaults
from dctap.exceptions import ConfigError

@dctap_defaults()
def get_config(config_filename=None, config_yamldoc=None, **kwargs):
    """@@@"""
    configfile = kwargs["configfile"]
    if configfile:
        try:
            config_settings_from_file = load_yaml_to_dict(yaml_filename=configfile)
            config_dict.update(config_settings_from_file)
        except FileNotFoundError as fnfe:
            raise FileNotFoundError(f"Config file '{configfile}' not found.") from fnfe
    return config_dict


def load_yaml_to_dict(yaml_filename=None):
    """Load YAML from string, Path object, or filename, into Python dict."""
    yaml = YAML(typ='safe', pure=True)
    bad_form = f"'{yaml_filename}' has badly formed YAML: fix, re-generate, or delete."
    if yaml_filename:
        yaml_pathobj = Path(yaml_filename)
        try:
            yamlstr = yaml_pathobj.read_text(encoding="UTF-8")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"'{yaml_filename}' not found.") from e
    if yaml_as_dict:
        return yaml_as_dict
    return {}

def test_get_config_from_passed_nondefault_yaml_with_config_yamldoc():
    """@@@"""
    yamldoc = """default_identifier: "default"\n"""
    config_dict = get_config(config_yamldoc=yamldoc)
    assert config_dict.get("default_identifier")


def test_exit_with_configerror_if_my_configfile_specified_but_not_found(tmp_path):
    """Exit with ConfigError if config file specified as argument is not found."""
    print(str(Path.cwd()))
    os.chdir(tmp_path)
    print(str(Path.cwd()))
    with pytest.raises(FileNotFoundError) as fnfe:
        get_config()
    assert "not found" in str(fnfe.value)
    assert fnfe.type == FileNotFoundError
    assert "not found" in str(fnfe.value.__cause__)


