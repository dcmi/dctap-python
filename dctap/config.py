"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path
from .defaults import dctap_defaults
from .exceptions import ConfigError
from .utils import load_yaml_to_dict, coerce_concise


@dctap_defaults()
def get_config(config_yamlfile=None, config_yamlstring=None, **kwargs):
    """@@@."""
    # pylint: disable=too-many-branches
    configfile = kwargs["configfile"]  # Any kwarg not listed here is simply ignored.
    configyaml = kwargs["configyaml"]
    config_dict = _initialize_config_dict()
    configyaml_from_file = None
    configdict_from_file = None

    # Makes no sense to specify two arguments, config_yamlfile and config_yamlstring.
    if config_yamlfile and config_yamlstring:
        raise ConfigError("Cannot load YAML from both string and file.")

    # If no arguments passed, try to parse default config file, update config_dict.
    if not config_yamlstring and not config_yamlfile:
        if Path(configfile).is_file():  # No need to warn if file does not exist.
            configyaml_from_file = Path(configfile).read_text(encoding="utf-8")

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

    # breakpoint(context=5)
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
def write_configfile(config_filename=None, config_yamlstring=None, **kwargs):
    """Write initial config file or exit trying."""
    configfile = kwargs["configfile"]
    configyaml = kwargs["configyaml"]
    if Path(configfile).exists():
        raise ConfigError(f"'{configfile}' exists - will not overwrite.")
    if config_filename:
        configfile = config_filename
    if config_yamlstring:  # useful for testing
        configyaml = config_yamlstring
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
