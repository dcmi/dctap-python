"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path
from .defaults import CONFIGYAML, dctap_defaults
from .exceptions import ConfigError
from .utils import load_yaml_to_dict


@dctap_defaults()
def get_config(config_filename=None, config_yamldoc=None, **kwargs):
    """Populates config dict:
    3. Updates dict from YAML string if passed in with configyaml, otherwise
       updates dict from dctap-python built-in CONFIGYAML.
    4. Or if config file name is passed in, and file exists, updates dict from file.
    """
    shapeclass = kwargs["shapeclass"]
    stateclass = kwargs["stateclass"]
    configfile = kwargs["configfile"]
    configyaml = kwargs["configyaml"]

    # 1. Initializes config dict with element lists (computed) and placeholder keys.
    config_dict = _initialize_config_dict()
    if configyaml:
        dict_from_yamlstr = load_yaml_to_dict(yamlstr=configyaml)
        config_dict.update(dict_from_yamlstr)

    # 2. Settings from configfile, if passed in and file exists, update defaults.
    if configfile:
        try:
            config_dict.update(load_yaml_to_dict(yaml_filename=configfile))
        except (FileNotFoundError, ConfigError):
            pass

    return config_dict

#
#    # Then extra element aliases, if declared, are added to element aliases.
#    extras = config_dict.get("extra_element_aliases")
#    if extras:
#        try:
#            extras = {coerce_concise(str(k).lower()): v for (k, v) in extras.items()}
#        except AttributeError:
#            extras = {}
#        config_dict["element_aliases"].update(extras)
#
#    # Ensure that each prefix ends in a colon.
#    config_dict = _add_colons_to_prefixes_if_needed(config_dict)
#
#    return config_dict


@dctap_defaults()
def _initialize_config_dict(**kwargs):
    """Initialize config dict with element lists (computed) and placeholder keys."""
    shapeclass = kwargs["shapeclass"]
    stateclass = kwargs["stateclass"]
    config_dict = {}
    ems_dict = {}
    shems = ems_dict["shape_elements"] = get_shems(shapeclass)
    stems = ems_dict["statement_template_elements"] = get_stems(stateclass)
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


def get_shems(shapeclass=None):
    """List TAP elements supported by given shape class."""
    main_shems = list(asdict(shapeclass()))
    main_shems.remove("state_list")
    main_shems.remove("shape_warns")
    main_shems.remove("shape_extras")
    return main_shems


def get_stems(stateclass=None):
    """List TAP elements supported by given statement template class."""
    main_stems = list(asdict(stateclass()))
    main_stems.remove("state_warns")
    main_stems.remove("state_extras")
    return main_stems


@dctap_defaults()
def write_configfile(config_filename=None, config_yamldoc=None, **kwargs):
    """Write initial config file or exit trying."""
    shapeclass = kwargs["shapeclass"]
    stateclass = kwargs["stateclass"]
    configfile = kwargs["configfile"]
    configyaml = kwargs["configyaml"]
    if Path(configfile).exists():
        raise ConfigError(f"'{configfile}' exists - will not overwrite.")
    if config_filename:
        configfile = config_filename
    if config_yamldoc:  # useful for testing
        configyaml = config_yamldoc
    try:
        with open(configfile, "w", encoding="utf-8") as outfile:
            outfile.write(configyaml)
            message = f"Settings written to '{configfile}'."
            print(message, file=sys.stderr)
    except FileNotFoundError as error:
        raise ConfigError(f"'{configfile}' not writeable.") from error


def _get_aliases_dict(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    aliases_to_elements = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        aliases_to_elements[lowerkey] = csv_elem  # { foobar: fooBar }
    return aliases_to_elements
