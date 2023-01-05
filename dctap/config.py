"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path
from .defaults import CONFIGFILE, CONFIGYAML
from .exceptions import ConfigError
from .tapclasses import TAPShape, TAPStatementTemplate
from .utils import load_yaml_to_dict, coerce_concise


def get_config(
    shape_class=TAPShape,
    state_class=TAPStatementTemplate,
    config_yamlfile=CONFIGFILE,
    config_yamlstring=CONFIGYAML,
    nondefault_config_yamlstring=None,
):
    """Get configuration dictionary from package defaults."""
    # pylint: disable=too-many-branches
    config_dict = _initialize_config_dict(shape_class, state_class)
    configyaml_from_file = None
    configdict_from_file = None

    ## Makes no sense to specify two arguments, config_yamlfile and config_yamlstring.
    #if config_yamlfile and config_yamlstring:
    #    raise ConfigError("Cannot load YAML from both string and file.")

    # Try to parse default config file, update config_dict.
    if not config_yamlstring and not config_yamlfile:
        if Path(config_yamlfile).is_file():  # No need to warn if file does not exist.
            configyaml_from_file = Path(config_yamlfile).read_text(encoding="utf-8")

        if not configyaml_from_file:
            configyaml_from_file = configyaml
            configdict_from_file = load_yaml_to_dict(yamlstring=configyaml)
        else:
            configdict_from_file = load_yaml_to_dict(yamlstring=configyaml_from_file)

        if configdict_from_file is not None:  # But YAML contents could be bad.
            config_dict.update(configdict_from_file)

    # If config_yamlfile was passed, try to read and parse, then update config_dict.
    if config_yamlfile and not config_yamlstring:
        try:
            configyaml_from_file = Path(config_yamlfile).read_text(encoding="utf-8")
        except FileNotFoundError as err:
            raise ConfigError(f"Config file '{config_yamlfile}' not found.") from err
        if configyaml_from_file is not None:
            configdict_from_file = load_yaml_to_dict(yamlstring=configyaml_from_file)
            if configdict_from_file is not None:  # But YAML contents could be bad.
                config_dict.update(configdict_from_file)

    # If config_yamlstring was passed, try to use it to update config_dict.
    if config_yamlstring:
        configdict_from_yamlstring = load_yaml_to_dict(yamlstring=config_yamlstring)
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
    config_filename=CONFIGFILE,
    config_yamlstring=CONFIGYAML,
    nondefault_config_yamlstring=None
):
    """Write initial config file or exit trying."""
    if Path(config_filename).exists():
        raise ConfigError(f"'{config_filename}' exists - will not overwrite.")
    if nondefault_config_yamlstring:  # useful for testing
        config_yamlstring = nondefault_config_yamlstring
    try:
        with open(config_filename, "w", encoding="utf-8") as outfile:
            outfile.write(config_yamlstring)
            print(f"Settings written to '{config_filename}'.", file=sys.stderr)
    except FileNotFoundError as error:
        raise ConfigError(f"'{config_filename}' not writeable.") from error


def _get_aliases_dict(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    aliases_to_elements = {}
    for csv_elem in csv_elements_list:
        lowerkey = csv_elem.lower()
        aliases_to_elements[lowerkey] = csv_elem  # { foobar: fooBar }
    return aliases_to_elements
