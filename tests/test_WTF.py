"""Return config dictionary from reading config file."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.defaults import CONFIGFILE, dctap_defaults
from dctap.exceptions import ConfigError

@dctap_defaults()
def get_config(config_filename=None, config_yamldoc=None, **kwargs):
    """@@@"""
    configfile = kwargs["configfile"]
    breakpoint(context=5)
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

# @pytest.mark.skip(reason="Done!")
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
    print(str(Path.cwd()))
    os.chdir(tmp_path)
    print(str(Path.cwd()))
    with pytest.raises(FileNotFoundError) as fnfe:
        get_config()
    assert "not found" in str(fnfe.value)
    assert fnfe.type == FileNotFoundError
    assert "not found" in str(fnfe.value.__cause__)


