"""Read CSV file and return list of rows as Python dictionaries."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import csvreader
from dctap.exceptions import NoDataError, DctapError


def test_csvreader_with_simple_csvfile():
    """Here: simple CSV with three columns."""
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
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_csv_passed_as_string_or_open_csvfile_object(tmp_path):
    """CSV can be passed as string or as open file object."""
    config_dict = get_config()
    csvfile_str = "PropertyID\ndc:creator\n"
    expected_rows_list = [{"propertyID": "dc:creator"}]
    #
    # Passed as string
    #
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    #
    # Passed as open file object
    #
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(csvfile_str, encoding="utf-8")
    open_csvfile_obj = open(csvfile_path, encoding="utf-8")
    (actual_rows_list, actual_warnings) = csvreader(
        open_csvfile_obj=open_csvfile_obj, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_unrecognized_headers_passed_thru_lowercased_with_warning():
    """Unrecognized headers passed thru, lowercased, with warning."""
    config_dict = get_config()
    csvfile_str = "PropertyID,Status\ndc:creator,lost or missing\n"
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "status": "lost or missing",
        }
    ]
    expected_warnings_dict = {
        "csv": {
            "header": ["Non-DCTAP element 'status' not configured as extra element."]
        }
    }
    (actual_rows_list, actual_warnings_dict) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert actual_warnings_dict == expected_warnings_dict


def test_headers_stripped_of_single_and_double_quotes():
    """
    Single and double quotes are stripped from header values.
    - "Text qualifier characters" (quotes) must be removed from column header.
    - Column headers must not contain commas.
    """
    config_dict = get_config()
    csvfile_str = '"PropertyID","PropertyLabel"\n"dc:creator","Creator"\n'
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_rows_starting_with_comment_hash_are_ignored():
    """CSV rows starting with comment (hash as first non-blank) are ignored."""
    config_dict = get_config()
    csvfile_str = """\
        # Comment
        PropertyID
             # Another comment line
        dc:creator
    """
    expected_rows_list = [{"propertyID": "dc:creator"}]
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_when_header_too_short_first_added_header_is_empty_string():
    """Where headers shorter than rows, adds one empty header."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyID,\n:a,dct:creator,URI\n"
    expected_rows_list = [{"shapeID": ":a", "propertyID": "dct:creator", "": "URI"}]
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_when_header_too_short_second_added_header_none_collects_all_extras():
    """When headers shorter than rows, extra values collected under header None."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyID,\n:a,dct:creator,URI,comment,comment two\n"
    expected_rows_list = [
        {
            "shapeID": ":a",
            "propertyID": "dct:creator",
            "": "URI",
            None: ["comment", "comment two"],
        }
    ]
    (actual_rows_list, _) = csvreader(csvfile_str=csvfile_str, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_when_rows_too_short_filled_out_with_nones():
    """Short rows are filled out with None values."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyID,valueNodeType\n:a,dct:creator\n"
    expected_rows_list = [
        {"shapeID": ":a", "propertyID": "dct:creator", "valueNodeType": None}
    ]
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_header_cells_stripped_of_surrounding_whitespace():
    """Whitespace around CSV header cells is stripped."""
    config_dict = get_config()
    csvfile_str = " PropertyID ,      PropertyLabel \ndc:creator,Creator\n"
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    actual_rows_list, actual_warnings = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_row_cells_stripped_of_surrounding_whitespace():
    """Whitespace around CSV row cells is stripped."""
    config_dict = get_config()
    csvfile_str = "     PropertyID  , PropertyLabel\n dc:creator  , Creator \n"
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    (actual_rows_list, _) = csvreader(csvfile_str=csvfile_str, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_headers_recognized_when_aliased():
    """Headers may be aliased and are normalized for case, dashes, underscores."""
    config_dict = get_config()
    config_dict["element_aliases"].update({"propid": "propertyID"})
    csvfile_str = "Prop_ID\nhttp://purl.org/dc/terms/creator\n"
    expected_rows_list = [{"propertyID": "http://purl.org/dc/terms/creator"}]
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list


def test_nodataerror_if_passed_empty_string_or_open_file_with_empty_string():
    """NoDataError if passed empty string (or open file with empty string)."""
    config_dict = get_config()
    csvfile_str = ""
    with pytest.raises(NoDataError):
        (actual_rows_list, actual_warnings) = csvreader(
            csvfile_str=csvfile_str, config_dict=config_dict
        )


def test_nodataerror_if_header_passed_but_no_data_rows():
    """NoDataError if passed header row but no data rows."""
    config_dict = get_config()
    csvfile_str = "propertyID,propertyLabel"
    with pytest.raises(NoDataError):
        (actual_rows_list, actual_warnings) = csvreader(
            csvfile_str=csvfile_str, config_dict=config_dict
        )


def test_dctaperror_if_first_line_has_no_propertyid():
    """Raises exception if first line of CSV has no propertyID."""
    config_dict = get_config()
    csvfile_str = "shapeID,propertyIdentifier,valueNodeType\n:a,dct:creator,URI\n"
    with pytest.raises(DctapError):
        csvreader(csvfile_str=csvfile_str, config_dict=config_dict)


def test_messiness_in_headers_cleaned_up():
    """Messiness in headers (extra spaces, punctuation, wrong case) is cleaned up."""
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
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list

def test_warns_when_header_unrecognized():
    """Warns when header is unrecognized (ie, not configured as extra)."""
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed"]
    csvfile_str = "closed,propertyID,status\ntrue,dc:date,lost or found\n"
    expected_rows_list = [
        {
            "closed": "true",
            "propertyID": "dc:date",
            "status": "lost or found",
        }
    ]
    expected_warnings_dict = {
        'csv': {
            'header': ["Non-DCTAP element 'status' not configured as extra element."]
        }
    }
    #
    (actual_rows_list, actual_warnings_dict) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert actual_warnings_dict == expected_warnings_dict

def test_no_warns_when_nondctap_header_configured_as_extra(capsys):
    """But does not warn about unrecognized header if configured as extra."""
    config_dict = get_config()
    config_dict["extra_statement_template_elements"] = ["status"]
    config_dict["extra_shape_elements"] = ["closed"]
    csvfile_str = "closed,propertyID,status\ntrue,dc:date,lost or found\n"
    expected_rows_list = [
        {
            "closed": "true",
            "propertyID": "dc:date",
            "status": "lost or found",
        }
    ]
    expected_warnings_dict = {}
    #
    (actual_rows_list, actual_warnings_dict) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert actual_warnings_dict == expected_warnings_dict
    # with capsys.disabled():
    #     print()
    #     print(actual_warnings_dict)


@pytest.mark.now
def test_csvreader_with_complete_csvfile(capsys):
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
    (actual_rows_list, actual_warnings) = csvreader(
        csvfile_str=csvfile_str, config_dict=config_dict
    )
    assert actual_rows_list == expected_rows_list
    assert isinstance(actual_rows_list, list)
    assert isinstance(expected_rows_list, list)
    assert actual_rows_list[0]["mandatory"]
    assert len(actual_rows_list) == 2
    assert len(expected_rows_list) == 2
    assert len(actual_warnings) == 0
    # with capsys.disabled():
    #     print()
    #     print(actual_warnings)
