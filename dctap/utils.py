"""Utilities."""

import re
import sys
from urllib.parse import urlparse
from pandas.core.frame import DataFrame


def strip_angle_brackets_from_url(url):
    """Normalize URL by stripping angle brackets."""
    return url.lstrip("<").rstrip(">")


def is_uri(url):
    """True if string is valid as a URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_uri_or_prefixed_uri(uri):
    """True if string is valid as a URI or prefixed URI."""
    if re.match("[A-Za-z0-9_]*:[A-Za-z0-9_]*", uri):
        return True
    if is_uri(uri):
        return True
    if not re.match("[A-Za-z0-9_]*:[A-Za-z0-9_]*", uri):
        print(
            f"Warning: {repr(uri)} is not a valid " "URI or prefixed URI.",
            file=sys.stderr,
        )
        return False
    return True


def pprint_df(df: DataFrame):
    """Print pandas DataFrame instance, left-aligned."""
    # https://stackoverflow.com/questions/17232013/how-to-set-the-pandas-dataframe-data-left-right-alignment
    left_aligned_df = df.style.set_properties(**{"text-align": "left"})
    left_aligned_df = left_aligned_df.set_table_styles(
        [dict(selector="th", props=[("text-align", "left")])]
    )
    return left_aligned_df
