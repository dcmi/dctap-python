"""Read CSV file and return list of rows as Python dictionaries."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _get_rows
from dctap.exceptions import NoDataError


def test_exits_if_no_data_to_process(tmp_path, capsys):
    """Exits with NoDataError if _get_rows is passed no data."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text("")
    assert Path(csvfile_path).exists()
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    with pytest.raises(NoDataError):
        actual_rows_list, actual_warnings = _get_rows(
            csvfile_obj, config_dict=config_dict
        )


def test_get_rows_when_passed_csvfile_string():
    """Get rows when passed contents of CSV file as string."""
    config_dict = get_config()
    csvfile_str = "PropertyID,PropertyLabel\ndc:creator,Creator\n"
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    (actual_rows_list, _) = _get_rows(csvfile_str=csvfile_str, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_when_header_values_are_quoted(tmp_path):
    """
    Get rows where header elements are in quotes:
    - "Text qualifier" characters (single or double quotes) must be removed
      from column header
    """
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        ('"PropertyID","PropertyLabel"\n"dc:creator","Creator"\n'), encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_where_header_elements_surrounded_by_whitespace(tmp_path):
    """Get rows where header elements are surrounded by whitespace."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (" PropertyID ,      PropertyLabel \ndc:creator,Creator\n"), encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "propertyLabel": "Creator",
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_including_header_element_not_in_DCTAP(tmp_path):
    """Get rows where one header element is not part of the DCTAP model."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "PropertyID,Ricearoni\ndc:creator,SFO treat\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "propertyID": "dc:creator",
            "ricearoni": "SFO treat",
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_minimal(tmp_path):
    """Get list of rows, as dicts, from one-row, one-column CSV."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "PropertyID\nhttp://purl.org/dc/terms/creator\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [{"propertyID": "http://purl.org/dc/terms/creator"}]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_given_customized_element_alias(tmp_path):
    """Using customized element alias, normalized for case, dashes, underscores."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "Prop_ID\nhttp://purl.org/dc/terms/creator\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    config_dict["element_aliases"].update({"propid": "propertyID"})
    expected_rows_list = [{"propertyID": "http://purl.org/dc/terms/creator"}]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_fills_in_short_headers_subsequently_with_None(tmp_path):
    """Where headers shorter than rows, extra values collected under header None."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "shapeID,propertyID,\n:a,dct:creator,URI,comment,comment two\n",
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "shapeID": ":a",
            "propertyID": "dct:creator",
            "": "URI",
            None: ["comment", "comment two"],
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_fills_in_short_headers_first_with_empty_header(tmp_path):
    """Where headers shorter than rows, adds one empty header."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "shapeID,propertyID,\n:a,dct:creator,URI\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [{"shapeID": ":a", "propertyID": "dct:creator", "": "URI"}]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_fills_in_short_rows_with_None_values(tmp_path):
    """Fills in short rows with None values."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "shapeID,propertyID,valueNodeType\n:a,dct:creator\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {"shapeID": ":a", "propertyID": "dct:creator", "valueNodeType": None}
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_raises_exception_if_first_line_has_no_propertyid(tmp_path):
    """Raises exception if first line of CSV has no propertyID."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        ("shapeID,propertyIdentifier,valueNodeType\n:a,dct:creator,URI\n"),
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    config_dict = get_config()
    with pytest.raises(SystemExit):
        _get_rows(csvfile_obj, config_dict=config_dict)


def test_get_rows_with_unknown_column(tmp_path):
    """Non-DCTAP elements kept by _get_rows (but dropped by _get_shapes)."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueConstraint,value Gestalt\n"
            ":book,dc:creator,,:author\n"
            ",dc:type,so:Book,\n"
            ":author,foaf:name,,\n"
        ),
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
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
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_with_unknown_column2(tmp_path):
    """Passes thru unknown header, lowercased."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueShape,wildCard\n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
            ":author,foaf:name,,\n"
        ),
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
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
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_with_simple_csvfile(tmp_path):
    """Another simple CSV with three columns."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueNodeType\n"
            ":a,dct:creator,URI\n"
            ":a,dct:subject,URI\n"
            ":a,dct:date,String\n"
        ),
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {"shapeID": ":a", "propertyID": "dct:creator", "valueNodeType": "URI"},
        {"shapeID": ":a", "propertyID": "dct:subject", "valueNodeType": "URI"},
        {"shapeID": ":a", "propertyID": "dct:date", "valueNodeType": "String"},
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_liststatements_with_csv_column_outside_dctap_model_are_ignored(tmp_path):
    """CSV columns not part of the DC TAP model are simply ignored."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        ("shapeID,propertyID,confidential\n:a,dct:subject,True\n"), encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {"shapeID": ":a", "propertyID": "dct:subject", "confidential": "True"},
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_correct_a_real_mess(tmp_path):
    """Messiness in headers (extra spaces, punctuation, wrong case) is corrected."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "S hape ID,pr-opertyID___,valueShape     ,wildCard    \n"
        ":book,dcterms:creator,:author,Yeah yeah yeah\n",
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "shapeID": ":book",
            "propertyID": "dcterms:creator",
            "valueShape": ":author",
            "wildcard": "Yeah yeah yeah",
        }
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list


def test_get_rows_with_complete_csvfile(tmp_path):
    """Simple CSV with all columns."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,shapeLabel,propertyID,"
            "propertyLabel,mandatory,repeatable,valueNodeType,"
            "valueDataType,valueConstraint,valueConstraintType,valueShape,note\n"
            ":a,Book,dct:creator,Creator,1,0,URI,,,,:b,Typically the author.\n"
            ":b,Person,ex:name,Name,1,0,Literal,xsd:string,,,,\n"
        ),
        encoding="utf-8",
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
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
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert isinstance(actual_rows_list, list)
    assert isinstance(expected_rows_list, list)
    assert actual_rows_list == expected_rows_list
    assert actual_rows_list[0]["mandatory"]
    assert len(actual_rows_list) == 2
    assert len(expected_rows_list) == 2
    assert len(actual_warnings) == 0


def test_warns_if_header_not_recognized(tmp_path, capsys):
    """Warns about unrecognized header, 'ricearoni'."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "propertyID,ricearoni\ndc:date,SFO treat\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        },
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list
    assert len(actual_warnings) == 1
    warning = "Non-DCTAP element 'ricearoni' not configured as extra element."
    assert warning in actual_warnings["csv"]["column"]


def test_does_not_warn_if_non_dctap_header_configured_as_extra(tmp_path):
    """But does not warn about unrecognized header if configured as extra."""
    os.chdir(tmp_path)
    config_dict = get_config()
    config_dict["extra_statement_template_elements"] = ["ricearoni"]
    config_dict["extra_shape_elements"] = ["sftreat"]
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "sftreat,propertyID,ricearoni\natreat,dc:date,SFO treat\n", encoding="utf-8"
    )
    csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "sftreat": "atreat",
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        },
    ]
    actual_rows_list, actual_warnings = _get_rows(csvfile_obj, config_dict=config_dict)
    assert actual_rows_list == expected_rows_list
    assert len(actual_warnings) == 0
    assert not actual_warnings.get("csv")
