"""dctap.csvreader._make_shape"""

import os
import pytest
from dctap.config import get_config
from dctap.csvreader import _make_shape
from dctap.tapclasses import TAPShape


def test_make_shapes_returns_tapshape_object_even_in_absence_of_propertyID(tmp_path):
    """Populates TAPShape object even in the absence of a propertyID."""
    os.chdir(tmp_path)  # precaution to avoid interference among pytests
    config_dict = get_config()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
    }
    assert _make_shape(
        row_dict=one_row, config_dict=config_dict, shape_class=TAPShape
    ) == TAPShape(
        shapeID=":a", shapeLabel="Book", state_list=[], shape_warns={}, shape_extras={}
    )


def test_make_shape_recognizes_only_shape_elements_so_configured(tmp_path):
    """Populates TAPShape object but ignores any statement template elements in row."""
    os.chdir(tmp_path)  # precaution to avoid interference among pytests
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed"]
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
    }
    assert _make_shape(
        row_dict=one_row, config_dict=config_dict, shape_class=TAPShape
    ) == TAPShape(
        shapeID=":a",
        shapeLabel="Book",
        state_list=[],
        shape_warns={},
        shape_extras={"closed": False},
    )


def test_make_shape_reads_all_extra_shape_elements_so_configured(tmp_path):
    """Reads all elements configured as extra shape elements."""
    os.chdir(tmp_path)  # precaution to avoid interference among pytests
    config_dict = get_config()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["extra_shape_elements"] = ["closed", "start"]
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
    }
    assert _make_shape(
        row_dict=one_row, config_dict=config_dict, shape_class=TAPShape
    ) == TAPShape(
        shapeID=":a",
        shapeLabel="Book",
        state_list=[],
        shape_warns={},
        shape_extras={"closed": False, "start": True},
    )


def test_make_shape_sets_shape_elements_only(tmp_path):
    """Populates TAPShape object but ignores any statement template elements in row."""
    os.chdir(tmp_path)  # precaution to avoid interference among pytests
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed", "start"]
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "Book",
        "closed": False,
        "start": True,
        "propertyID": "ex:name",
        "valueNodeType": "literal",
    }
    shape = _make_shape(row_dict=one_row, config_dict=config_dict, shape_class=TAPShape)
    assert shape.shapeID == ":a"
    assert shape.shapeLabel == "Book"
    # pylint: disable=use-implicit-booleaness-not-comparison
    assert shape.shape_warns == {}
    assert shape.shape_extras == {"closed": False, "start": True}
    assert shape.state_list == []  # _make_shape() sets shape fields only, not ST fields


def test_make_shape_extra_shape_elements_that_are_empty_are_passed_through(tmp_path):
    """Empty shape elements are passed through, but not unasserted elements."""
    os.chdir(tmp_path)  # precaution to avoid interference among pytests
    config_dict = get_config()
    assert config_dict["shape_elements"] == ["shapeID", "shapeLabel"]
    config_dict["extra_shape_elements"] = ["closed", "start"]
    one_row = {
        "shapeID": ":a",
        "shapeLabel": "",
        "closed": "",
    }
    assert _make_shape(
        row_dict=one_row, config_dict=config_dict, shape_class=TAPShape
    ) == TAPShape(
        shapeID=":a",
        shapeLabel="",
        state_list=[],
        shape_warns={},
        shape_extras={"closed": ""},
    )
