"""
Tests for TAPStatementTemplate._languageTag_parse
- Called by sc.normalize().

2022-09-21 definition: "One or more language tags that can be applied to
strings used with the property are given valueConstraintType languageTag.
Languages are most commonly designated using the ISO 639 standard codes." [1]

[1] https://www.loc.gov/standards/iso639-2/langhome.html
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.csvreader import csvreader


def test_valueConstraintType_languagetag_parse():
    """If valueConstraintType list, valueConstraint parsed on whitespace."""
    config_dict = get_config()
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "languagetag"
    sc.valueConstraint = "fr it de"
    sc._valueConstraintType_languageTag_parse(config_dict)
    assert sc.valueConstraint == ["fr", "it", "de"]


def test_valueConstraintType_languagetag_item_separator_comma(tmp_path):
    """@@@"""
    config_dict = get_config()
    config_dict["picklist_item_separator"] = ","
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,languagetag,"fr, it, de"\n'
        )
    )
    value_constraint = csvreader(
        open_csvfile_obj=open(csvfile_path), 
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["fr", "it", "de"]


def test_valueConstraintType_languagetag_item_separator_pipe(tmp_path):
    """@@@"""
    config_dict = get_config()
    config_dict["picklist_item_separator"] = "|"
    config_dict["default_shape_identifier"] = "default"
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            'PropertyID,valueConstraintType,valueConstraint\n'
            'ex:foo,languagetag,"fr|it|de"\n'
        )
    )
    value_constraint = csvreader(
        open_csvfile_obj=open(csvfile_path), 
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )["shapes"][0]["statement_templates"][0]["valueConstraint"]
    assert value_constraint == ["fr", "it", "de"]

