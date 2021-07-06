"""Default settings."""

import sys
from dataclasses import asdict
from pathlib import Path

# pylint: disable=consider-using-from-import
import ruamel.yaml as yaml
from .exceptions import ConfigError
from .tapclasses import TAPShape, TAPStatementConstraint


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
    "propid": "propertyID"
    "mand": "mandatory"
    "rep": "repeatable"
    "nodetype": "valueNodeType"
    "datatype": "valueDataType"
    "vc": "valueConstraint"
    "vctype": "valueConstraintType"
    "vshape": "valueShape"
"""

DEFAULT_CONFIGFILE_NAME = "dctap.yml"


def write_configfile(
    config_file=DEFAULT_CONFIGFILE_NAME,
    config_yaml=DEFAULT_CONFIG_YAML,
):
    """Write initial config file, by default to CWD, or exit if already exists."""
    if Path(config_file).exists():
        raise ConfigError(f"{repr(config_file)} already exists - will not overwrite.")
    try:
        with open(config_file, "w", encoding="utf-8") as outfile:
            outfile.write(config_yaml)
            print(
                f"Built-in settings written to {str(config_file)} - edit as needed.",
                file=sys.stderr,
            )
    except FileNotFoundError:
        # pylint: disable=raise-missing-from
        raise ConfigError(f"{repr(config_file)} is not writeable - try different name.")


def get_config(
    config_file=None,
    nondefault_config_yaml=None,
    shape_class=TAPShape,
    statement_constraint_class=TAPStatementConstraint,
):
    """Get config dict from file if found, else get built-in defaults."""
    # pylint: disable=raise-missing-from
    elements_dict = dict()
    elements_dict["shape_elements"] = _shape_elements(shape_class)
    elements_dict["statement_constraint_elements"] = _statement_constraint_elements(
        statement_constraint_class
    )
    elements_dict["csv_elements"] = (
        elements_dict["shape_elements"] + elements_dict["statement_constraint_elements"]
    )
    bad_form = f"{repr(config_file)} is badly formed: fix, re-generate, or delete."
    not_found = f"{repr(config_file)} not found or not readable."
    if config_file: # if a specific config file was named
        try:
            config_yaml = Path(config_file).read_text()
        except (FileNotFoundError, PermissionError):
            raise ConfigError(not_found)
    else:
        try:
            config_yaml = Path(DEFAULT_CONFIGFILE_NAME).read_text()
        except (FileNotFoundError, PermissionError):
            if nondefault_config_yaml:
                config_yaml = nondefault_config_yaml
            else:
                config_yaml = DEFAULT_CONFIG_YAML
    try:
        config_dict = yaml.safe_load(config_yaml)
    except (yaml.YAMLError, yaml.scanner.ScannerError):
        raise ConfigError(bad_form)
    config_dict.update(elements_dict)
    if not config_dict.get("element_aliases"):   # is this necessary?
        config_dict["element_aliases"] = dict()  # is this necessary?
    config_dict["element_aliases"].update(
        _compute_alias2element_mappings(config_dict["csv_elements"])
    )
    return config_dict


def _compute_alias2element_mappings(csv_elements_list=None):
    """Compute shortkey/lowerkey-to-element mappings from list of CSV elements."""
    alias2element_mappings = dict()
    for csv_elem in csv_elements_list:
        # shortkey: initial letter (lowercase) + each uppercase letter, lowercased
        shortkey = "".join([csv_elem[0]] + [l.lower() for l in csv_elem if l.isupper()])
        lowerkey = csv_elem.lower()
        alias2element_mappings[shortkey] = csv_elem  # { shortkey: camelcasedValue }
        alias2element_mappings[lowerkey] = csv_elem  # { lowerkey: camelcasedValue }
    return alias2element_mappings


def _shape_elements(shape_class=TAPShape):
    """List DCTAP elements supported by given shape class."""
    sh_elements = list(asdict(shape_class()))
    sh_elements.remove("sc_list")
    sh_elements.remove("sh_warnings")
    return sh_elements


def _statement_constraint_elements(statement_constraint_class=TAPStatementConstraint):
    """List DCTAP elements supported by given statement constraint class."""
    sc_elements = list(asdict(statement_constraint_class()))
    sc_elements.remove("sc_warnings")
    return sc_elements
