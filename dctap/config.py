"""Default settings."""

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
from .utils import coerce_concise


def get_config(
    configfile_name=None,
    config_yamldoc=DEFAULT_CONFIG_YAML,
    shape_class=TAPShape,
    stem_class=TAPStatementTemplate,
):
    """
    Get built-in settings then override from config file (if found).
    - Note: extra element aliases added to defaults.
    """

    def load2dict(configfile=None):
        """Parse contents of YAML configfile and return dictionary."""
        bad_form = f"{repr(configfile)} is badly formed: fix, re-generate, or delete."
        config_yaml = Path(configfile).read_text(encoding="UTF-8")
        try:
            config_read_from_file = yaml.safe_load(config_yaml)
        except (yaml.YAMLError, yaml.scanner.ScannerError) as error:
            raise ConfigError(bad_form) from error

        if config_read_from_file:
            return config_read_from_file
        return {}

    elements_dict = {}
    elements_dict["shape_elements"] = get_shems(shape_class)[0]
    elements_dict["statement_template_elements"] = get_stems(stem_class)[0]
    elements_dict["csv_elements"] = (
        elements_dict["shape_elements"] + elements_dict["statement_template_elements"]
    )

    config_dict = {}
    config_dict["element_aliases"] = {}
    config_dict["element_aliases"].update(
        _alias2element_mappings(elements_dict["csv_elements"])
    )
    config_dict["default_shape_identifier"] = "default"
    config_dict["prefixes"] = {}
    config_dict["extra_shape_elements"] = []
    config_dict["extra_statement_template_elements"] = []
    config_dict["picklist_elements"] = []
    config_dict["picklist_item_separator"] = " "
    config_dict["extra_value_node_types"] = []
    config_dict["extra_element_aliases"] = {}

    config_dict.update(elements_dict)
    if yaml.safe_load(config_yamldoc):
        config_dict.update(yaml.safe_load(config_yamldoc))

    config_dict_from_file = {}
    if configfile_name:
        try:
            config_dict_from_file.update(load2dict(configfile_name))
        except FileNotFoundError as error:
            raise ConfigError(f"{repr(configfile_name)} not found.") from error
    elif Path(DEFAULT_CONFIGFILE_NAME).exists():
        config_dict_from_file.update(load2dict(DEFAULT_CONFIGFILE_NAME))
    elif Path(DEFAULT_HIDDEN_CONFIGFILE_NAME).exists():
        config_dict_from_file.update(load2dict(DEFAULT_HIDDEN_CONFIGFILE_NAME))

    # Settings from config file may override defaults.
    config_dict.update(config_dict_from_file)

    # But extra element aliases, if declared, are added to element aliases.
    extras = config_dict.get("extra_element_aliases")
    if extras:
        try:
            extras = {coerce_concise(str(k).lower()):v for (k, v) in extras.items()}
        except AttributeError:
            extras = {}
        config_dict["element_aliases"].update(extras)

    return config_dict


def get_shems(shape_class=TAPShape, settings=None):
    """List DCTAP elements supported by given shape class."""
    only_shape_elements = list(asdict(shape_class()))
    only_shape_elements.remove("state_list")
    only_shape_elements.remove("shape_warns")
    only_shape_elements.remove("shape_extras")
    extra_shape_elements = []
    if settings:
        if settings.get("extra_shape_elements"):
            for extra_element in settings.get("extra_shape_elements"):
                extra_shape_elements.append(extra_element)
    return (only_shape_elements, extra_shape_elements)


def get_stems(stem_class=TAPStatementTemplate, settings=None):
    """List DCTAP elements supported by statement template class."""
    only_st_elements = list(asdict(stem_class()))
    only_st_elements.remove("state_warns")
    only_st_elements.remove("state_extras")
    extra_st_elements = []
    if settings:
        if settings.get("extra_statement_template_elements"):
            for extra_element in settings.get("extra_statement_template_elements"):
                extra_st_elements.append(extra_element)
    return (only_st_elements, extra_st_elements)


def write_configfile(
    configfile_name=DEFAULT_CONFIGFILE_NAME,
    config_yamldoc=DEFAULT_CONFIG_YAML,
):
    """Write initial config file or exit trying."""

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


def _alias2element_mappings(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""

    alias2element_mappings = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        alias2element_mappings[lowerkey] = csv_elem  # { foobar: fooBar }
    return alias2element_mappings
