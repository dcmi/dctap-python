"""Verify that string superficially looks like a URI or Compact URI."""

from dctap.utils import looks_like_uri_or_curie


def test_utils_looks_like_uri_or_curie():
    """True if string looks (very superficially) like a URI or Compact URI."""
    assert looks_like_uri_or_curie("http://www.gmd.de")
    assert looks_like_uri_or_curie("dc:creator")
    assert looks_like_uri_or_curie("dc:")
    assert looks_like_uri_or_curie(":")
    assert looks_like_uri_or_curie(":default")
    assert not looks_like_uri_or_curie("default")
    assert not looks_like_uri_or_curie(23412)
