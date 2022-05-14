"""
dctap.csvreader._get_tapshapes 
- 
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.csvreader import _get_tapshapes
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError

@pytest.mark.skip
def test_get_tapshapes_shape_elements_on_their_own_line(tmp_path):
    """Getting rows_list from tests/test_CSVREADER_get_rows.py ."""
    os.chdir(tmp_path) # precaution to avoid interference among pytests
    config_dict = get_config()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["extra_shape_elements"] = ["closed", "start"]
    rows_list = [
        {
            "shapeID": ":a",
            "shapeLabel": "Book",
            "closed": False,
            "start": True,
        },
        {
            "propertyID": "ex:name",
            "valueNodeType": "literal",
        },
    ]
    assert _get_tapshapes(rows_list, config_dict) == []
