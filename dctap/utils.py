"""Utilities."""

import re
import sys
from urllib.parse import urlparse


def strip_enclosing_angle_brackets(url):
    """Normalize URL by stripping angle brackets."""
    return url.lstrip("<").rstrip(">")


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
    else:
        return False


def expand_prefixes(shapes_dict=None, config_dict=None):
    """@@@"""
    for shape in shapes_dict["shapes"]:
        for prefix in config_dict["prefixes"]:
            if re.match(prefix, shape["shapeID"]):
                prefix_expanded = config_dict["prefixes"][prefix]
                shape["shapeID"] = re.sub(prefix, prefix_expanded, shape["shapeID"])
        for sc in shape["statement_constraints"]:
            for prop in ['propertyID', 'valueShape']:
                for prefix in config_dict["prefixes"]:
                    if sc.get(prop):
                        if re.match(prefix, sc[prop]):
                            prefix_expanded = config_dict["prefixes"][prefix]
                            sc[prop] = re.sub(prefix, prefix_expanded, sc[prop])
    return shapes_dict
