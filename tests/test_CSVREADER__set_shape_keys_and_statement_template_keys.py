"""
dctap.csvreader._make_shapeobj - from docstring:

    Populates shape fields of dataclass TAPShape object from dict for one row.

    Args:
        tapshape_obj: Unpopulated instance of dctap.tapclasses.TAPShape:
            TAPShape(shapeID='', shapeLabel='', st_list=[], sh_warnings={}, extras={})
        row_dict: Dictionary of all columns headers (keys) and cell values (values) 
            found in a given row, with no distinction between shape elements and 
            statement template elements.
        main_shape_elements: Default TAPClass fields related to shapes.
        xtra_shape_elements: Extra TAPClass fields as per optional config file.

    Returns:
        TAPShape object with shape fields set.
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config, get_shems
from dctap.csvreader import _get_tapshapes, _make_shapeobj
from dctap.defaults import DEFAULT_CONFIGFILE_NAME
from dctap.exceptions import ConfigError
from dctap.tapclasses import TAPShape


def test_set_tapshapes_fields_shape_element_not_configured_is_ignored(tmp_path):
    """Set TAPShape fields based on header: cell_value dict for one row."""
    os.chdir(tmp_path) # precaution to avoid interference among pytests
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed"]
    shape_instance = TAPShape()
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
    }
    assert _make_shapeobj(one_row, config_dict=config_dict) == TAPShape(
        shapeID=':a', 
        shapeLabel='Book', 
        st_list=[],
        sh_warnings={}, 
        extras={"closed": False}
    )

@pytest.mark.skip
def test_set_tapshapes_fields_shape_element_not(tmp_path):
    """Set TAPShape fields based on header: cell_value dict for one row."""
    os.chdir(tmp_path) # precaution to avoid interference among pytests
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    shape_instance = TAPShape()
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
        "propertyID": "ex:name",
        "valueNodeType": "literal",
    }
    assert _make_shapeobj(one_row, config_dict) == TAPShape(
        shapeID=':a', 
        shapeLabel='Book', 
        st_list=[{"propertyID": "ex:name", "valueNodeType": "literal"}], 
        sh_warnings={}, 
        extras={"closed": False, "start": True}
    )

