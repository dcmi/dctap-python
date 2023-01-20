"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path
from dctap.defaults import CONFIGFILE, CONFIGYAML
from dctap.exceptions import ConfigError
from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.utils import load_yaml_to_dict, coerce_concise


def get_config(
    nondefault_configyaml_str=None,
    nondefault_configfile_name=None,
    default_configyaml_str=CONFIGYAML,
    default_configfile_name=CONFIGFILE,
    default_shape_class=TAPShape,
    default_state_class=TAPStatementTemplate,
):
    """Get configuration dictionary from package defaults (or from non-defaults)."""
    # pylint: disable=too-many-arguments
    configyaml_read = None
    configdict_read = None
    config_dict = _initialize_config_dict(default_shape_class, default_state_class)

    if nondefault_configfile_name and nondefault_configyaml_str:
        raise ConfigError("Can load YAML from either string or file, not both.")

    if nondefault_configfile_name:
        nondefault_configfile = Path(nondefault_configfile_name)
        try:
            configyaml_read = nondefault_configfile.read_text(encoding="utf-8")
        except FileNotFoundError as err:
            message = f"Config file '{nondefault_configfile_name}' not found."
            raise ConfigError(message) from err
        configdict_read = load_yaml_to_dict(yamlstring=configyaml_read)
        if configdict_read is not None:
            config_dict.update(configdict_read)
        config_dict = _add_extra_element_aliases(config_dict)
        config_dict = _add_colons_to_prefixes_if_needed(config_dict)
        return config_dict

    if nondefault_configyaml_str:
        configdict_read = load_yaml_to_dict(yamlstring=nondefault_configyaml_str)
        if configdict_read is not None:
            if not configdict_read.get("default_shape_identifier"):
                configdict_read["default_shape_identifier"] = "default"
            config_dict.update(configdict_read)
        config_dict = _add_extra_element_aliases(config_dict)
        config_dict = _add_colons_to_prefixes_if_needed(config_dict)
        return config_dict

    try:
        configyaml_read = Path(default_configfile_name).read_text(encoding="utf-8")
    except FileNotFoundError:
        configyaml_read = default_configyaml_str
    configdict_read = load_yaml_to_dict(yamlstring=configyaml_read)
    if configdict_read is not None:
        config_dict.update(configdict_read)
    config_dict = _add_extra_element_aliases(config_dict)
    config_dict = _add_colons_to_prefixes_if_needed(config_dict)
    return config_dict


def _add_extra_element_aliases(config_dict):
    """If extra element aliases are specified, add them to the configuration dict."""
    extras = config_dict.get("extra_element_aliases")
    if extras:
        try:
            extras = {coerce_concise(str(k).lower()): v for (k, v) in extras.items()}
        except AttributeError:
            extras = {}
        config_dict["element_aliases"].update(extras)
    return config_dict


def _add_colons_to_prefixes_if_needed(config_dict):
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


def _get_shems(shape):
    """List TAP elements supported by given shape class."""
    main_shems = list(asdict(shape()))
    main_shems.remove("state_list")
    main_shems.remove("shape_warns")
    main_shems.remove("shape_extras")
    return main_shems


def _get_stems(state):
    """List TAP elements supported by given statement template class."""
    main_stems = list(asdict(state()))
    main_stems.remove("state_warns")
    main_stems.remove("state_extras")
    return main_stems


def _initialize_config_dict(shapeclass, stateclass):
    """Initialize config dict with element lists (computed) and placeholder keys."""
    config_dict = {}
    ems_dict = {}
    shems = ems_dict["shape_elements"] = _get_shems(shapeclass)
    stems = ems_dict["statement_template_elements"] = _get_stems(stateclass)
    ems_dict["csv_elements"] = shems + stems
    config_dict["element_aliases"] = {}
    config_dict["element_aliases"].update(_get_aliases_dict(ems_dict["csv_elements"]))
    config_dict["default_shape_identifier"] = "default"
    config_dict["prefixes"] = {}
    config_dict["extra_shape_elements"] = []
    config_dict["extra_statement_template_elements"] = []
    config_dict["picklist_elements"] = []
    config_dict["picklist_item_separator"] = " "
    config_dict["extra_value_node_types"] = []
    config_dict["extra_element_aliases"] = {}
    config_dict.update(ems_dict)
    return config_dict


def write_configfile(
    nondefault_configyaml_str=None,
    default_configfile_name=CONFIGFILE,
    default_configyaml_str=CONFIGYAML,
):
    """Write initial config file or exit trying."""
    if Path(default_configfile_name).exists():
        raise ConfigError(f"'{default_configfile_name}' exists - will not overwrite.")
    if nondefault_configyaml_str:  # useful for testing
        default_configyaml_str = nondefault_configyaml_str
    try:
        with open(default_configfile_name, "w", encoding="utf-8") as outfile:
            outfile.write(default_configyaml_str)
            print(f"Settings written to '{default_configfile_name}'.", file=sys.stderr)
    except FileNotFoundError as error:
        raise ConfigError(f"'{default_configfile_name}' not writeable.") from error


def _get_aliases_dict(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    aliases_to_elements = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        aliases_to_elements[lowerkey] = csv_elem  # { foobar: fooBar }
    return aliases_to_elements
