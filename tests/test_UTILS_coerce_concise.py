"""Removes spaces, dashes, underscores from string, then returns in lowercase."""

from dctap.utils import coerce_concise

def test_coerce_concise():
    """Removes spaces, dashes, and underscores, returns in lowercase."""
    assert coerce_concise("Property ID") == "propertyid"
    assert coerce_concise("Property__ID") == "propertyid"
    assert coerce_concise("Property-ID") == "propertyid"
