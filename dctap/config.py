"""Default settings."""

import re
import sys
from dataclasses import asdict
from pathlib import Path

# pylint: disable=consider-using-from-import
import ruamel.yaml as yaml
from .defaults import (
    DEFAULT_CONFIGFILE_NAME,
    DEFAULT_HIDDEN_CONFIGFILE_NAME,
    DEFAULT_CONFIG_YAML,
)
from .exceptions import ConfigError
from .tapclasses import TAPShape, TAPStatementTemplate


def shape_elements(shape_class=TAPShape, settings=None):
    """List DCTAP elements supported by given shape class."""
    only_shape_elements = list(asdict(shape_class()))
    only_shape_elements.remove("sc_list")
    only_shape_elements.remove("sh_warnings")
    only_shape_elements.remove("extra_elements")
    extra_shape_elements = []
    if settings:
        if settings.get("extra_shape_elements"):
            for extra_element in settings.get("extra_shape_elements"):
                extra_shape_elements.append(extra_element)
    return (only_shape_elements, extra_shape_elements)


def statement_template_elements(
    statement_template_class=TAPStatementTemplate, settings=None
):
    """List DCTAP elements supported by statement template class."""
    only_sc_elements = list(asdict(statement_template_class()))
    only_sc_elements.remove("sc_warnings")
    only_sc_elements.remove("extra_elements")
    extra_sc_elements = []
    if settings:
        if settings.get("extra_statement_template_elements"):
            for extra_element in settings.get("extra_statement_template_elements"):
                extra_sc_elements.append(extra_element)
    return (only_sc_elements, extra_sc_elements)


def write_configfile(
    configfile_name=DEFAULT_CONFIGFILE_NAME,
    config_yamldoc=DEFAULT_CONFIG_YAML,
    terse=False,
):
    """Write initial config file, by default to CWD, or exit if already exists."""
    if terse:
        config_yamldoc = '\n'.join( # remove lines starting with more than one '#'
            [ln for ln in config_yamldoc.splitlines() if not re.match("^##", ln)]
        )
        config_yamldoc = '\n'.join( # remove lines that consist only of whitespace
            [ln.rstrip() for ln in config_yamldoc.splitlines() if ln.rstrip()]
        )
    if Path(configfile_name).exists():
        raise ConfigError(f"{repr(configfile_name)} exists - will not overwrite.")
    try:
        with open(configfile_name, "w", encoding="utf-8") as outfile:
            outfile.write(config_yamldoc)
            print(
                f"Built-in settings written to {str(configfile_name)} for editing.",
                file=sys.stderr,
            )
    except FileNotFoundError as error:
        raise ConfigError(f"{repr(configfile_name)} not writeable.") from error


def get_config(
    configfile_name=None,
    config_yamldoc=DEFAULT_CONFIG_YAML,
    shape_class=TAPShape,
    statement_template_class=TAPStatementTemplate,
):
    """Get built-in settings then override from config file (if found)."""

    def load2dict(configfile=None):
        """Parse contents of YAML configfile and return dictionary."""
        bad_form = f"{repr(configfile)} is badly formed: fix, re-generate, or delete."
        config_yaml = Path(configfile).read_text(encoding='UTF-8')
        try:
            file_config_dict = yaml.safe_load(config_yaml)
        except (yaml.YAMLError, yaml.scanner.ScannerError) as error:
            raise ConfigError(bad_form) from error
        return file_config_dict

    elements_dict = {}
    elements_dict["shape_elements"] = shape_elements(shape_class)[0]
    elements_dict["statement_template_elements"] = statement_template_elements(
        statement_template_class
    )[0]
    elements_dict["csv_elements"] = (
        elements_dict["shape_elements"] + elements_dict["statement_template_elements"]
    )

    config_dict = {}
    config_dict["element_aliases"] = {}
    config_dict["element_aliases"].update(
        _alias2element_mappings(elements_dict["csv_elements"])
    )
    config_dict["prefixes"] = {}
    config_dict.update(elements_dict)
    if yaml.safe_load(config_yamldoc):
        config_dict.update(yaml.safe_load(config_yamldoc))

    file_config_dict = {}
    if configfile_name:
        try:
            file_config_dict.update(load2dict(configfile_name))
        except FileNotFoundError as error:
            raise ConfigError(
                f"{repr(configfile_name)} not found; using defaults."
            ) from error
    elif Path(DEFAULT_CONFIGFILE_NAME).exists():
        file_config_dict.update(load2dict(DEFAULT_CONFIGFILE_NAME))
    elif Path(DEFAULT_HIDDEN_CONFIGFILE_NAME).exists():
        file_config_dict.update(load2dict(DEFAULT_HIDDEN_CONFIGFILE_NAME))

    config_dict.update(file_config_dict)
    return config_dict


def _alias2element_mappings(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    alias2element_mappings = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        alias2element_mappings[lowerkey] = csv_elem  # { lowerkey: camelcasedValue }
    return alias2element_mappings
