"""Normalize list of header elements (column names)."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _normalize_header_line
from dctap.exceptions import DctapError


def test_normal_header_line_returned_unchanged_without_warnings(capsys):
    """Given raw header line, return normalized but with no warnings."""
    config_dict = get_config()
    input_header_line = "propertyID,value Constraint\n"
    expected_header_line = "propertyID,valueConstraint\n"
    expected_warnings_list = []
    (actual_header_line, actual_warnings_list) = _normalize_header_line(
        input_header_line, config_dict
    )
    assert actual_header_line == expected_header_line
    assert actual_warnings_list == expected_warnings_list

def test_messy_header_line_returned_unchanged_without_warnings(capsys):
    """Given messy header line, return normalized."""
    config_dict = get_config()
    input_header_line = "S hape ID,pr-opertyID___,valueShape\n"
    expected_header_line = "shapeID,propertyID,valueShape\n"
    expected_warnings_list = []
    (actual_header_line, actual_warnings_list) = _normalize_header_line(
        input_header_line, config_dict
    )
    assert actual_header_line == expected_header_line
    assert actual_warnings_list == expected_warnings_list

def test_header_line_with_unrecognized_header_return_with_warning(capsys):
    """Given line with unrecognized headers, return lowercased with warnings."""
    config_dict = get_config()
    input_header_line = "propertyID,Status,Length\n"
    expected_header_line = "propertyID,status,length\n"
    expected_warnings_list = [
        "Non-DCTAP element 'status' not configured as extra element.",
        "Non-DCTAP element 'length' not configured as extra element."
    ]
    (actual_header_line, actual_warnings_list) = _normalize_header_line(
        input_header_line, config_dict
    )
    assert actual_header_line == expected_header_line
    assert actual_warnings_list == expected_warnings_list
    # with capsys.disabled():
    #     print()
    #     # print("actual_header_line: ", actual_header_line)
    #     print("actual_warnings_list: ", actual_warnings_list)

def test_header_line_with_recognized_aliased_header_returned_normalized(capsys):
    """Recognized aliased header returned normalized."""
    nondefault_configyaml_str = """
    extra_element_aliases:
        "ShapID": "shapeID"
    """
    config_dict = get_config(nondefault_configyaml_str=nondefault_configyaml_str)
    input_header_line = "ShapID,propertyID\n"
    expected_header_line = "shapeID,propertyID\n"
    expected_warnings_list = []
    (actual_header_line, actual_warnings_list) = _normalize_header_line(
        input_header_line, config_dict
    )
    assert actual_header_line == expected_header_line
    assert actual_warnings_list == expected_warnings_list

def test_extra_statement_template_element_triggers_no_warning(capsys):
    """'Recognized' element is normalized to lowercase but triggers no warning."""
    nondefault_configyaml_str = """
    extra_statement_template_elements:
    - status
    """
    config_dict = get_config(nondefault_configyaml_str=nondefault_configyaml_str)
    input_header_line = "propertyID,stATUS\n"
    expected_header_line = "propertyID,status\n"
    expected_warnings_list = []
    (actual_header_line, actual_warnings_list) = _normalize_header_line(
        input_header_line, config_dict
    )
    assert actual_header_line == expected_header_line
    assert actual_warnings_list == expected_warnings_list

def test_dctaperror_if_first_line_has_no_propertyid():
    """Raises DctapError if first line of CSV has no propertyID."""
    config_dict = get_config()
    input_header_line = "shapeID,propertyIdentifier\n"
    with pytest.raises(DctapError):
        (x, y) = _normalize_header_line(input_header_line, config_dict)
