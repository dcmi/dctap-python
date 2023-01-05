"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path
from .defaults import CONFIGFILE, CONFIGYAML
from .exceptions import ConfigError
from .tapclasses import TAPShape, TAPStatementTemplate
from .utils import load_yaml_to_dict, coerce_concise


def get_config(
    default_shape_class=TAPShape,
    default_state_class=TAPStatementTemplate,
    default_configfile_name=CONFIGFILE,
    default_configyaml_string=CONFIGYAML,
    nondefault_configyaml_string=None,
):
    """Get configuration dictionary from package defaults."""
    # pylint: disable=too-many-branches
    config_dict = _initialize_config_dict(default_shape_class, default_state_class)
    configyaml_from_file = None
    configdict_from_file = None

    ## Makes no sense to specify two arguments, default_configfile_name and default_configyaml_string.
    # if default_configfile_name and default_configyaml_string:
    #    raise ConfigError("Cannot load YAML from both string and file.")

    # Try to parse default config file, update config_dict.
    if not default_configyaml_string and not default_configfile_name:
        if Path(
            default_configfile_name
        ).is_file():  # No need to warn if file does not exist.
            configyaml_from_file = Path(default_configfile_name).read_text(
                encoding="utf-8"
            )

        if not configyaml_from_file:
            configyaml_from_file = default_configyaml_string
            configdict_from_file = load_yaml_to_dict(
                yamlstring=default_configyaml_string
            )
        else:
            configdict_from_file = load_yaml_to_dict(yamlstring=configyaml_from_file)

        if configdict_from_file is not None:  # But YAML contents could be bad.
            config_dict.update(configdict_from_file)

    # If default_configfile_name was passed, try to read and parse, then update config_dict.
    if default_configfile_name and not default_configyaml_string:
        try:
            configyaml_from_file = Path(default_configfile_name).read_text(
                encoding="utf-8"
            )
        except FileNotFoundError as err:
            raise ConfigError(
                f"Config file '{default_configfile_name}' not found."
            ) from err
        if configyaml_from_file is not None:
            configdict_from_file = load_yaml_to_dict(yamlstring=configyaml_from_file)
            if configdict_from_file is not None:  # But YAML contents could be bad.
                config_dict.update(configdict_from_file)

    # If default_configyaml_string was passed, try to use it to update config_dict.
    if default_configyaml_string:
        configdict_from_yamlstring = load_yaml_to_dict(
            yamlstring=default_configyaml_string
        )
        if configdict_from_yamlstring is not None:
            config_dict.update(configdict_from_yamlstring)

    # Extra element aliases, if declared, are added to element aliases.
    extras = config_dict.get("extra_element_aliases")
    if extras:
        try:
            extras = {coerce_concise(str(k).lower()): v for (k, v) in extras.items()}
        except AttributeError:
            extras = {}
        config_dict["element_aliases"].update(extras)

    config_dict = _add_colons_to_prefixes_if_needed(config_dict)
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


def write_configfile(
    default_configfile_name=CONFIGFILE,
    default_configyaml_string=CONFIGYAML,
    nondefault_configyaml_string=None,
):
    """Write initial config file or exit trying."""
    if Path(default_configfile_name).exists():
        raise ConfigError(f"'{default_configfile_name}' exists - will not overwrite.")
    if nondefault_configyaml_string:  # useful for testing
        default_configyaml_string = nondefault_configyaml_string
    try:
        with open(default_configfile_name, "w", encoding="utf-8") as outfile:
            outfile.write(default_configyaml_string)
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
