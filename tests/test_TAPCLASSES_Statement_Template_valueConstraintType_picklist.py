"""Tests for private functions called by TAPStatementTemplate.normalize()."""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()


def test_valueConstraintType_picklist_parse():
    """If valueConstraintType picklist, valueConstraint parsed on whitespace."""
    st = TAPStatementTemplate()
    st.propertyID = "dcterms:creator"
    st.valueConstraintType = "picklist"
    st.valueConstraint = "one two three"
    st._valueConstraintType_picklist_parse(config_dict)
    assert st.valueConstraint == ["one", "two", "three"]


def test_valueConstraintType_picklist_parse_case_insensitive():
    """Value constraint types are case-insensitive."""
    st = TAPStatementTemplate()
    st.propertyID = "dcterms:creator"
    st.valueConstraintType = "PICKLIST"
    st.valueConstraint = "one two          three" # extra whitespace
    st._valueConstraintType_picklist_parse(config_dict)
    assert st.valueConstraint == ["one", "two", "three"]


def test_valueConstraintType_picklist_item_separator_comma(tmp_path):
    """Picklist values are split on List Item Separator - default or configured."""
    config_dict = get_config()
    config_dict["picklist_item_separator"] = ","
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,picklist,"one, two, three"\n'
        )
    )
    value_constraint = csvreader(
        open_csvfile_obj=open(csvfile_path), 
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["one", "two", "three"]


def test_valueConstraintType_picklist_item_separator_pipe(tmp_path):
    """Picklist values are split on pipe character if so configured."""
    config_dict = get_config()
    config_dict["picklist_item_separator"] = "|"
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,picklist,"one|two|three"\n'
        )
    )
    value_constraint = csvreader(
        open_csvfile_obj=open(csvfile_path), 
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["one", "two", "three"]
