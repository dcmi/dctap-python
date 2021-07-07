"""Removes spaces, dashes, underscores from string, then returns in lowercase."""

from dctap.csvreader import _lowercase_despace_depunctuate

def test_lowercase_despace_depunctuate():
    """Removes spaces, dashes, and underscores, returns in lowercase."""
    assert _lowercase_despace_depunctuate("Property ID") == "propertyid"
    assert _lowercase_despace_depunctuate("Property__ID") == "propertyid"
    assert _lowercase_despace_depunctuate("Property-ID") == "propertyid"
