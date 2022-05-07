"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path

# pylint: disable=consider-using-from-import
import ruamel.yaml as yaml
from .defaults import DEFAULT_CONFIGFILE_NAME, DEFAULT_CONFIG_YAML
from .exceptions import ConfigError
from .tapclasses import TAPShape, TAPStatementConstraint


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


def statement_constraint_elements(
    statement_constraint_class=TAPStatementConstraint, settings=None
):
    """List DCTAP elements supported by given statement constraint class."""
    only_sc_elements = list(asdict(statement_constraint_class()))
    only_sc_elements.remove("sc_warnings")
    only_sc_elements.remove("extra_elements")
    extra_sc_elements = []
    if settings:
        if settings.get("extra_statement_constraint_elements"):
            for extra_element in settings.get("extra_statement_constraint_elements"):
                extra_sc_elements.append(extra_element)
    return (only_sc_elements, extra_sc_elements)


def write_configfile(
    configfile_name=DEFAULT_CONFIGFILE_NAME,
    config_yamldoc=DEFAULT_CONFIG_YAML,
):
    """Write initial config file, by default to CWD, or exit if already exists."""
    if Path(configfile_name).exists():
        raise ConfigError(f"{repr(configfile_name)} exists - will not overwrite.")
    try:
        with open(configfile_name, "w", encoding="utf-8") as outfile:
            outfile.write(config_yamldoc)
            print(
                f"Built-in settings written to {str(configfile_name)} for editing.",
                file=sys.stderr,
            )
    except FileNotFoundError:
        # pylint: disable=raise-missing-from
        raise ConfigError(f"{repr(configfile_name)} not writeable; try different name.")


def get_config(
    configfile_name=None,
    config_yamldoc=DEFAULT_CONFIG_YAML,
    shape_class=TAPShape,
    statement_constraint_class=TAPStatementConstraint,
):
    """Get config dict from file if found, else use built-in defaults."""
    # pylint: disable=raise-missing-from
    elements_dict = {}
    elements_dict["shape_elements"] = shape_elements(shape_class)[0]
    elements_dict["statement_constraint_elements"] = statement_constraint_elements(
        statement_constraint_class
    )[0]
    elements_dict["csv_elements"] = (
        elements_dict["shape_elements"] + elements_dict["statement_constraint_elements"]
    )
    bad_form = f"{repr(configfile_name)} is badly formed: fix, re-generate, or delete."
    not_found = f"{repr(configfile_name)} not found or not readable."

    if configfile_name:  # if a specific config file was named
        try:
            config_yaml = Path(configfile_name).read_text(encoding='UTF-8')
        except (FileNotFoundError, PermissionError):
            raise ConfigError(not_found)
    else:
        try:
            config_yaml = Path(DEFAULT_CONFIGFILE_NAME).read_text(encoding='UTF-8')
        except (FileNotFoundError, PermissionError):
            config_yaml = config_yamldoc

    try:
        config_dict = yaml.safe_load(config_yaml)
    except (yaml.YAMLError, yaml.scanner.ScannerError):
        raise ConfigError(bad_form)

    config_dict.update(elements_dict)

    if not config_dict.get("element_aliases"):  # is this necessary?
        config_dict["element_aliases"] = {}     # is this necessary?
    config_dict["element_aliases"].update(
        _compute_alias2element_mappings(config_dict["csv_elements"])
    )
    return config_dict


def _compute_alias2element_mappings(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    alias2element_mappings = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        alias2element_mappings[lowerkey] = csv_elem  # { lowerkey: camelcasedValue }
    return alias2element_mappings
