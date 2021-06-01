"""Sets up directory with simple config file for use as pytest fixture."""

import os
from pathlib import Path
import pytest
from dctap.config import write_starter_configfile

TEST_CONFIGFILE_NAME = ".csv2rc"

TEST_DEFAULT_CONFIG_SETTINGS_YAML = """\
prefixes:
    ":": "http://example.org/"
    "dct:": "http://purl.org/dc/terms/"

valueNodeType:
- URI
- BNode
- Nonliteral

valueConstraintType:
- UriStem
- LitPicklist
"""


@pytest.fixture()
def dir_with_csv2rc(tmp_path):
    """Set up directory with simple config file for use as pytest fixture."""
    os.chdir(tmp_path)
    Path(TEST_CONFIGFILE_NAME).write_text(TEST_DEFAULT_CONFIG_SETTINGS_YAML)
    return Path.cwd()
