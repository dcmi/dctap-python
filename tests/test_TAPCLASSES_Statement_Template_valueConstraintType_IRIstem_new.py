"""
Tests for TAPStatementTemplate private methods:
- sc._valueConstraintType_iristem_parse
- sc._valueConstraintType_IRIstem_warn_if_valueConstraint_not_valid_regex
- Called by sc.normalize().

2022-09-21 definition: "When the value is to be chosen from a list of terms
that share a namespace (like http://vocab.getty.edu/page/aat/), the
valueConstraintType is IRIstem and the valueConstraint gives the base IRI for
the list."
"""

import os
import pytest
from pathlib import Path
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.csvreader import csvreader

config_dict = get_config()


def test_valueConstraintType_IRIstem_single_value_parsed_as_singleton_list():
    """Value is parsed on whitespace into list by sc.normalize()."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "IRIstem"
    sc.valueConstraint = 'http://example.org/'
    sc._valueConstraintType_iristem_parse()
    expected_value = ['http://example.org/']
    assert sc.valueConstraint == expected_value


def test_valueConstraintType_IRIstem_multiple_values_parsed_as_list():
    """Value is parsed on whitespace into list by sc.normalize()."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "IRIstem"
    sc.valueConstraint = 'http://example.org/ http://elpmaxe.org'
    sc._valueConstraintType_iristem_parse()
    expected_value = ['http://example.org/', 'http://elpmaxe.org']
    assert sc.valueConstraint == expected_value


def test_valueConstraintType_IRIstem_parser_accepts_non_uris():
    """Parser for IRIstems does not yet check whether values are IRIs."""
    sc = TAPStatementTemplate()
    sc.propertyID = "dcterms:creator"
    sc.valueConstraintType = "IRIstem"
    sc.valueConstraint = 'example.org/ elpmaxe.org'
    sc._valueConstraintType_iristem_parse()
    expected_value = ['example.org/', 'elpmaxe.org']
    assert sc.valueConstraint == expected_value


def test_valueConstraintType_IRIstem_warns_if_not_IRIlike():
    """Warns if IRIstem value is not IRIlike."""


# def test_valueConstraintType_pattern_is_valid_regex():
#     """For valueConstraintType pattern, valueConstraint must be valid regex."""
#     sc = TAPStatementTemplate()
#     sc.propertyID = ":status"
#     sc.valueConstraintType = "pattern"
#     sc.valueConstraint = "approved_*"
#     sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
#     assert sc.valueConstraint
#     sc.valueConstraint = "/approved_*/"
#     sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
#     assert sc.valueConstraint == "/approved_*/"
#     sc.valueConstraint = "^2020 August"
#     sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
#     assert sc.valueConstraint
#     sc.valueConstraint = "'confidential'"
#     sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
#     assert sc.valueConstraint == "'confidential'"

# def test_valueConstraintType_pattern_warn_if_not_valid_regex():
#     """For valueConstraintType pattern, warns if valueConstraint not valid regex."""
#     sc = TAPStatementTemplate()
#     sc.propertyID = ":status"
#     sc.valueConstraintType = "pattern"
#     sc.valueConstraint="approved_(*"
#     sc._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
#     assert len(sc.state_warns) == 1

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
