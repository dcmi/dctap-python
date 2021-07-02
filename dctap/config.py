"""Default settings."""

import sys
from pathlib import Path
from ruamel import yaml
from .exceptions import ConfigError


DEFAULT_CONFIG_YAML = """# dctap configuration file (in YAML format)
default_shape_name: ":default"

value_node_types:
- iri
- literal
- bnode

prefixes:
    ":":        "http://example.org/"
    "dc:":      "http://purl.org/dc/elements/1.1/"
    "dcterms:": "http://purl.org/dc/terms/"
    "dct:":     "http://purl.org/dc/terms/"
    "foaf:":    "http://xmlns.com/foaf/0.1/"
    "owl:":     "http://www.w3.org/2002/07/owl#"
    "rdf:":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    "rdfs:":    "http://www.w3.org/2000/01/rdf-schema#"
    "schema:":  "http://schema.org/"
    "skos:":    "http://www.w3.org/2004/02/skos/core#"
    "skosxl:":  "http://www.w3.org/2008/05/skos-xl#"
    "wdt:":     "http://www.wikidata.org/prop/direct/"
    "xsd:":     "http://www.w3.org/2001/XMLSchema#"

# Aliases (case-insensitive) mapped to "official" element names (case-sensitive)
element_aliases:
    "Prop ID": "propertyID"
    "Mand": "mandatory"
    "Rep": "repeatable"
    "Node Type": "valueNodeType"
    "Datatype": "valueDataType"
    "VC": "valueConstraint"
    "VCType": "valueConstraintType"
    "VShape": "valueConstraintType"
"""

DEFAULT_CONFIGFILE_NAME = ".dctaprc"


def get_config(configfile=None):
    """Get config dict from file if found, else get built-in defaults."""
    # pylint: disable=raise-missing-from
    if not configfile:
        file_to_try = DEFAULT_CONFIGFILE_NAME
    else:
        file_to_try = configfile
    bad_form = f"{repr(file_to_try)} is badly formed: fix, re-generate, or delete."
    not_found = f"{repr(file_to_try)} not found or not readable."
    try:
        return yaml.safe_load(Path(file_to_try).read_text())
    except (FileNotFoundError, PermissionError):
        if configfile:  # if one was specified as an argument
            raise ConfigError(not_found)
    except (yaml.YAMLError, yaml.scanner.ScannerError):
        raise ConfigError(bad_form)
    return yaml.safe_load(DEFAULT_CONFIG_YAML)


def write_configfile(configfile=None):
    """Write initial config file, by default to CWD, or exit if already exists."""
    if not configfile:
        configfile = DEFAULT_CONFIGFILE_NAME
    if Path(configfile).exists():
        raise ConfigError(f"{repr(configfile)} already exists - will not overwrite.")
    try:
        with open(configfile, "w", encoding="utf-8") as outfile:
            outfile.write(DEFAULT_CONFIG_YAML)
            print(
                f"Built-in settings written to {str(configfile)} - edit as needed.",
                file=sys.stderr,
            )
    except FileNotFoundError:
        # pylint: disable=raise-missing-from
        raise ConfigError(f"{repr(configfile)} is not writeable - try different name.")
