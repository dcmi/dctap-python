"""Utilities."""

import re
from pathlib import Path
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.scanner import ScannerError
from urllib.parse import urlparse
from .exceptions import ConfigError

def load_yaml_to_dict(yamlstr=None, yaml_filename=None):
    """Load YAML from string, Path object, or filename, into Python dict."""
    yaml = YAML(typ='safe', pure=True)
    bad_form = f"{repr(yaml_filename)} is badly formed: fix, re-generate, or delete."
    dup_form = f"Dicts in {repr(yaml_filename)} may not have duplicate keys."
    if yaml_filename and yamlstr:
        raise sys.exit("Cannot load YAML from both string and file.")
    if yaml_filename:
        yaml_pathobj = Path(yaml_filename)
        try:
            yamlstr = yaml_pathobj.read_text(encoding="UTF-8")
        except FileNotFoundError:
            raise ConfigError(f"{repr(yaml_filename)} not found.")
    if yamlstr:
        try:
            yaml_as_dict = yaml.load(yamlstr)
        except (YAMLError, ScannerError) as error:
            raise ConfigError(bad_form) from error
    if yaml_as_dict:   # necessary?
        return yaml_as_dict   # necessary?
    return {}   # necessary?


def coerce_concise(some_str=None):
    """
    For given string:
    - delete spaces, underscores, dashes, commas
    - lowercase
    - delete surrounding single and double quotes
    """
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.replace(",", "")
    some_str = some_str.lower()
    some_str = some_str.strip('"')
    some_str = some_str.strip("'")
    return some_str


def coerce_integer(value_constraint=None):
    """Coerces string to integer or returns string untouched."""
    try:
        value_constraint = int(value_constraint)
    except (ValueError, TypeError):
        pass  # pass the valueConstraint through untouched
    return value_constraint


def coerce_numeric(value_constraint=None):
    """Coerces string to numeric type or returns string untouched."""
    try:
        if value_constraint == str(float(value_constraint)):
            value_constraint = float(value_constraint)
        else:
            value_constraint = int(value_constraint)
    except (ValueError, TypeError):
        pass  # pass the valueConstraint through untouched
    return value_constraint


def expand_uri_prefixes(shapes_dict=None, config_dict=None):
    """Expand namespace prefixes, eg: dc:date to http://purl.org/dc/terms/date."""
    # pylint: disable=too-many-nested-blocks
    if not config_dict.get("prefixes"):
        raise ConfigError("No 'prefixes' section found in config file.")
    for shape in shapes_dict["shapes"]:
        for prefix in config_dict["prefixes"]:
            if re.match(prefix, shape["shapeID"]):
                prefix_expanded = config_dict["prefixes"][prefix]
                shape["shapeID"] = re.sub(prefix, prefix_expanded, shape["shapeID"])
        for sc in shape["statement_templates"]:
            for element in ["propertyID", "valueDataType", "valueShape"]:
                if sc.get(element):
                    for prefix in config_dict["prefixes"]:
                        if re.match(prefix, sc.get(element)):
                            prefix_expanded = config_dict["prefixes"][prefix]
                            sc[element] = re.sub(prefix, prefix_expanded, sc[element])
    return shapes_dict


def is_uri(url_string):
    """True if string is valid as a URL."""
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_uri_or_prefixed_uri(uri):
    """True if string is URI or superficially looks like a prefixed URI."""
    if is_uri(uri):
        return True
    if re.match("[A-Za-z0-9_]*:[A-Za-z0-9_]*", uri):  # looks like prefixed URI
        return True
    return False


def strip_enclosing_angle_brackets(url):
    """Normalize URL by stripping angle brackets."""
    return url.lstrip("<").rstrip(">")
