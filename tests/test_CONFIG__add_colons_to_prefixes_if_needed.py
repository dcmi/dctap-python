"""In getting rows: compute alias-to-element aliases from config dict."""


import pytest
from dctap.config import get_config, _add_colons_to_prefixes_if_needed


def test_add_colons_to_prefixes_if_needed(capsys):
    """If prefixes are configured without colons, adds colons."""
    config_dict = get_config()
    config_dict['prefixes'] = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        '': 'http://example.org/'
    }
    prefixes_expected = {
        'dc:': 'http://purl.org/dc/elements/1.1/',
        ':': 'http://example.org/',
    }
    config_dict = _add_colons_to_prefixes_if_needed(config_dict)
    assert prefixes_expected == config_dict["prefixes"]
