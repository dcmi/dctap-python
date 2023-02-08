"""Read CSV file and return list of rows as Python dictionaries."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _get_rows
from dctap.exceptions import NoDataError, DctapError

def test_rows_starting_with_comment_hash_are_ignored(tmp_path):
    """CSV rows starting with a comment hash are ignored."""
    config_dict = get_config()
    csvfile_str = """\
        # Comment
        PropertyID
        # Another comment line
        dc:creator
    """
    expected_rows_list = [{"propertyID": "dc:creator"}]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_from_csv_passed_as_string_or_as_open_csvfile_object(tmp_path):
    """CSV can be passed as string or as open file object."""
    config_dict = get_config()
    csvfile_str = 'PropertyID\ndc:creator\n'
    expected_rows_list = [{"propertyID": "dc:creator"}]
    # 
    # Passed as string
    # 
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    #
    # Passed as open file object
    # 
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(csvfile_str, encoding="utf-8")
    open_csvfile_obj = open(csvfile_path, encoding="utf-8")
    (actual_rows_list, actual_warnings) = _get_rows(
        open_csvfile_obj=open_csvfile_obj, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_exits_if_passed_empty_string_or_open_file_with_empty_string(tmp_path):
    """NoDataError if passed empty string (or open file with empty string)."""
    config_dict = get_config()
    csvfile_str = ""
    with pytest.raises(NoDataError):
        (actual_rows_list, actual_warnings) = _get_rows(
            csvfile_str=csvfile_str,
            config_dict=config_dict
        )

def test_exits_if_header_passed_but_no_data_rows(tmp_path):
    """NoDataError if passed header row but no data rows."""
    config_dict = get_config()
    csvfile_str = "propertyID,propertyLabel"
    with pytest.raises(NoDataError):
        (actual_rows_list, actual_warnings) = _get_rows(
            csvfile_str=csvfile_str,
            config_dict=config_dict
        )

def test_get_rows_fills_in_short_headers_subsequently_with_none(tmp_path):
    """Where headers shorter than rows, extra values collected under header None."""
    config_dict = get_config()
    csvfile_str = 'shapeID,propertyID,\n:a,dct:creator,URI,comment,comment two\n'
    expected_rows_list = [
        {
            "shapeID": ":a",
            "propertyID": "dct:creator",
            "": "URI",
            None: ["comment", "comment two"],
        }
    ]
    (actual_rows_list, _) = _get_rows(csvfile_str=csvfile_str, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list

def test_get_short_rows_are_filled_with_none_values(tmp_path):
    """Fills in short rows with None values."""
    config_dict = get_config()
    csvfile_str = 'shapeID,propertyID,valueNodeType\n:a,dct:creator\n'
    expected_rows_list = [
        {
            "shapeID": ":a", 
            "propertyID": "dct:creator", 
            "valueNodeType": None
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_row_values_are_stripped_of_surrounding_whitespace(tmp_path):
    """Whitespace around CSV values is stripped."""
    config_dict = get_config()
    csvfile_str = "     PropertyID  , PropertyLabel\n dc:creator  , Creator \n"
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    (actual_rows_list, _) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_header_values_are_stripped_of_surrounding_whitespace(tmp_path):
    """Get rows where header elements are surrounded by whitespace."""
    config_dict = get_config()
    csvfile_str = ' PropertyID ,      PropertyLabel \ndc:creator,Creator\n'
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(
        csvfile_str=csvfile_str,
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_single_and_double_quotes_are_stripped_from_header_values(tmp_path):
    """
    Single and double quotes are stripped from header values.
    - "Text qualifier characters" (the quotes) must be removed from column header.
    - Column headers better not contain commas.
    """
    config_dict = get_config()
    csvfile_str = '"PropertyID","PropertyLabel"\n"dc:creator","Creator"\n'
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_even_if_has_header_value_not_found_in_dctap_model(tmp_path):
    """Get rows where one header element is not part of the DCTAP model."""
    config_dict = get_config()
    csvfile_str = 'PropertyID,Ricearoni\ndc:creator,SFO treat\n'
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "ricearoni": "SFO treat",
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str,
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_given_customized_element_alias(tmp_path):
    """Using customized element alias, normalized for case, dashes, underscores."""
    config_dict = get_config()
    config_dict["element_aliases"].update({"propid": "propertyID"})
    csvfile_str = 'Prop_ID\nhttp://purl.org/dc/terms/creator\n'
    expected_rows_list = [
        {
            "propertyID": "http://purl.org/dc/terms/creator"
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_fills_in_short_headers_first_with_empty_header(tmp_path):
    """Where headers shorter than rows, adds one empty header."""
    config_dict = get_config()
    csvfile_str = 'shapeID,propertyID,\n:a,dct:creator,URI\n'
    expected_rows_list = [
        {
            "shapeID": ":a", 
            "propertyID": "dct:creator", 
            "": "URI"
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_raises_exception_if_first_line_has_no_propertyid(tmp_path):
    """Raises exception if first line of CSV has no propertyID."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyIdentifier,valueNodeType\n:a,dct:creator,URI\n"
    with pytest.raises(DctapError):
        _get_rows(
            csvfile_str=csvfile_str, 
            config_dict=config_dict
        )

def test_get_rows_with_unknown_column(tmp_path):
    """Non-DCTAP elements kept by _get_rows, but will be dropped by _get_shapes."""
    config_dict = get_config()
    csvfile_str = (
        "shapeID,propertyID,valueConstraint,value Gestalt\n"
        ":book,dc:creator,,:author\n"
        ",dc:type,so:Book,\n"
        ":author,foaf:name,,\n"
    )
    expected_rows_list = [
        {
            "shapeID": ":book",
            "propertyID": "dc:creator",
            "valueConstraint": "",
            "valuegestalt": ":author",
        },
        {
            "shapeID": "",
            "propertyID": "dc:type",
            "valueConstraint": "so:Book",
            "valuegestalt": "",
        },
        {
            "shapeID": ":author",
            "propertyID": "foaf:name",
            "valueConstraint": "",
            "valuegestalt": "",
        },
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_with_unknown_column2(tmp_path):
    """Passes thru unknown header column, lowercased."""
    config_dict = get_config()
    csvfile_str = (
        "shapeID,propertyID,valueShape,wildCard\n"
        ":book,dcterms:creator,:author,Yeah yeah yeah\n"
        ":author,foaf:name,,\n"
    )
    expected_rows_list = [
        {
            "shapeID": ":book",
            "propertyID": "dcterms:creator",
            "valueShape": ":author",
            "wildcard": "Yeah yeah yeah",
        },
        {
            "shapeID": ":author",
            "propertyID": "foaf:name",
            "valueShape": "",
            "wildcard": "",
        },
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_with_simple_csvfile(tmp_path):
    """Another simple CSV with three columns."""
    config_dict = get_config()
    csvfile_str = (
        "shapeID,propertyID,valueNodeType\n"
        ":a,dct:creator,URI\n"
        ":a,dct:subject,URI\n"
        ":a,dct:date,String\n"
    )
    expected_rows_list = [
        {"shapeID": ":a", "propertyID": "dct:creator", "valueNodeType": "URI"},
        {"shapeID": ":a", "propertyID": "dct:subject", "valueNodeType": "URI"},
        {"shapeID": ":a", "propertyID": "dct:date", "valueNodeType": "String"},
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_csv_columns_outside_dctap_model_are_ignored(tmp_path):
    """CSV columns not part of DCTAP model and not configured as extra are ignored."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyID,confidential\n:a,dct:subject,True\n"
    expected_rows_list = [
        {
            "shapeID": ":a", 
            "propertyID": "dct:subject", 
            "confidential": "True"
        }
    ]
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_correct_a_real_mess(tmp_path):
    """Messiness in headers (extra spaces, punctuation, wrong case) is corrected."""
    config_dict = get_config()
    csvfile_str = (
        "S hape ID,pr-opertyID___,valueShape     ,wildCard    \n"
        ":book,dcterms:creator,:author,Yeah yeah yeah\n"
    )
    expected_rows_list = [
        {
            "shapeID": ":book",
            "propertyID": "dcterms:creator",
            "valueShape": ":author",
            "wildcard": "Yeah yeah yeah",
        }
    ]
    #
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_get_rows_with_complete_csvfile(tmp_path):
    """Simple CSV with all columns."""
    config_dict = get_config()
    csvfile_str = (
        "shapeID,shapeLabel,propertyID,"
        "propertyLabel,mandatory,repeatable,valueNodeType,"
        "valueDataType,valueConstraint,valueConstraintType,valueShape,note\n"
        ":a,Book,dct:creator,Creator,1,0,URI,,,,:b,Typically the author.\n"
        ":b,Person,ex:name,Name,1,0,Literal,xsd:string,,,,\n"
    )
    expected_rows_list = [
        {
            "shapeID": ":a",
            "shapeLabel": "Book",
            "propertyID": "dct:creator",
            "propertyLabel": "Creator",
            "mandatory": "1",
            "repeatable": "0",
            "valueNodeType": "URI",
            "valueDataType": "",
            "valueConstraint": "",
            "valueConstraintType": "",
            "valueShape": ":b",
            "note": "Typically the author.",
        },
        {
            "shapeID": ":b",
            "shapeLabel": "Person",
            "propertyID": "ex:name",
            "propertyLabel": "Name",
            "mandatory": "1",
            "repeatable": "0",
            "valueNodeType": "Literal",
            "valueDataType": "xsd:string",
            "valueConstraint": "",
            "valueConstraintType": "",
            "valueShape": "",
            "note": "",
        },
    ]
    #
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert isinstance(actual_rows_list, list)
    assert isinstance(expected_rows_list, list)
    assert actual_rows_list[0]["mandatory"]
    assert len(actual_rows_list) == 2
    assert len(expected_rows_list) == 2
    assert len(actual_warnings) == 0

def test_warns_if_header_value_not_recognized(tmp_path, capsys):
    """Warns about unrecognized header value, 'ricearoni'."""
    config_dict = get_config()
    csvfile_str = (
        "propertyID,ricearoni\n"
        "dc:date,SFO treat\n"
    )
    expected_rows_list = [
        {
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        },
    ]
    #
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert len(actual_warnings) == 1
    warning = "Non-DCTAP element 'ricearoni' not configured as extra element."
    assert warning in actual_warnings["csv"]["column"]

def test_does_not_warn_if_non_dctap_header_value_configured_as_extra(tmp_path):
    """But does not warn about unrecognized header if configured as extra."""
    config_dict = get_config()
    config_dict["extra_statement_template_elements"] = ["ricearoni"]
    config_dict["extra_shape_elements"] = ["sftreat"]
    csvfile_str = (
        "sftreat,propertyID,ricearoni\n"
        "atreat,dc:date,SFO treat\n"
    )
    expected_rows_list = [
        {
            "sftreat": "atreat",
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        }
    ]
    #
    (actual_rows_list, actual_warnings) = _get_rows(
        csvfile_str=csvfile_str, 
        config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
