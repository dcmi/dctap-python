"""Verify that string is valid as URL."""

from dctap.utils import is_uri


def test_utils_is_uri():
    """True if string is valid as URL."""
    assert is_uri("http://www.gmd.de")
    assert not is_uri("http:///www.gmd.de")
    assert not is_uri("file:///www.gmd.de")
    assert not is_uri("gmd:")
