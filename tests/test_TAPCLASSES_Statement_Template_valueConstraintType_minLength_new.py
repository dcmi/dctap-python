"""
Tests for TAPStatementTemplate._minlength_parse / _maxlength_parse 
- Called by sc.normalize().

2022-09-21 definition: "A number to define the minimum or maximum length of a
string value."
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()


@pytest.mark.skip
def test_valueConstraintType_minlength_parse():
    """Here: string must be more than two characters long."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "minlength"
    sc.valueConstraint = "2"
    sc._valueConstraintType_minlength_parse(config_dict)
    assert sc.valueConstraint == ["fr", "it", "de"]







# def test_valueConstraintType_languagetag_parse():
#     """If valueConstraintType list, valueConstraint parsed on whitespace."""
#     sc = TAPStatementTemplate()
#     sc.propertyID = "dcterms:creator"
#     sc.valueConstraintType = "languagetag"
#     sc.valueConstraint = "fr it de"
#     sc._valueConstraintType_languageTag_parse(config_dict)
#     assert sc.valueConstraint == ["fr", "it", "de"]
#
# def test_exit_with_ConfigError_if_configfile_specified_but_not_found(tmp_path):
#     """Exit with ConfigError if config file specified as argument is not found."""
#     os.chdir(tmp_path)
#     with pytest.raises(ConfigError):
#         get_config(configfile_name="dctap.yaml")
