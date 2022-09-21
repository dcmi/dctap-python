"""
Tests for TAPStatementTemplate._mininclusive_parse / _maxinclusive_parse
- Called by sc.normalize().

2022-09-21 definition: "A number to define lower and upper bounds of a numeric
value. 'Inclusive' means that the numbers listed will be included in the
bounds, i.e. '3-5' includes 3, 4, 5."
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()









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
