"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path

from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.scanner import ScannerError
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
    state_class=TAPStatementTemplate,
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
            yaml = YAML(typ='safe', pure=True)
            config_read_from_file = yaml.load(config_yaml)
        except (YAMLError, ScannerError) as error:
            raise ConfigError(bad_form) from error

        if config_read_from_file:
            return config_read_from_file
        return {}

    elements_dict = {}
    elements_dict["shape_elements"] = get_shems(shape_class)
    elements_dict["statement_template_elements"] = get_stems(state_class)
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
    yaml = YAML(typ='safe', pure=True)
    if yaml.load(config_yamldoc):
        config_dict.update(yaml.load(config_yamldoc))

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

    # Then extra element aliases, if declared, are added to element aliases.
    extras = config_dict.get("extra_element_aliases")
    if extras:
        try:
            extras = {coerce_concise(str(k).lower()): v for (k, v) in extras.items()}
        except AttributeError:
            extras = {}
        config_dict["element_aliases"].update(extras)

    # Ensure that each prefix ends in a colon.
    config_dict = _add_colons_to_prefixes_if_needed(config_dict)

    return config_dict

def _add_colons_to_prefixes_if_needed(config_dict=None):
    """Reconstitute config_dict.prefixes, ensuring that each prefix ends in colon."""
    prefixes = config_dict.get("prefixes")
    new_prefixes = {}
    if prefixes:
        for prefix in prefixes:
            if not prefix.endswith(":"):
                new_prefixes[prefix + ":"] = prefixes[prefix]
            else:
                new_prefixes[prefix] = prefixes[prefix]
    config_dict["prefixes"] = new_prefixes
    return config_dict

def get_shems(shape_class=None):
    """List TAP elements supported by given shape class."""
    main_shems = list(asdict(shape_class()))
    main_shems.remove("state_list")
    main_shems.remove("shape_warns")
    main_shems.remove("shape_extras")
    return main_shems


def get_stems(state_class=None):
    """List TAP elements supported by given statement template class."""
    main_stems = list(asdict(state_class()))
    main_stems.remove("state_warns")
    main_stems.remove("state_extras")
    return main_stems


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
