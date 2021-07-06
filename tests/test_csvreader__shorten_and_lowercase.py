"""Removes spaces, dashes, underscores from string, then returns in lowercase."""

from dctap.csvreader import _shorten_and_lowercase

def test_shorten_and_lowercase():
    """Removes spaces, dashes, and underscores, returns in lowercase."""
    assert _shorten_and_lowercase("Property ID") == "propertyid"
    assert _shorten_and_lowercase("Property__ID") == "propertyid"
    assert _shorten_and_lowercase("Property-ID") == "propertyid"
