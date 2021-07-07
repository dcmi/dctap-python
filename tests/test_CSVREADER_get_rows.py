"""Read CSV file and return list of rows as Python dictionaries."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import _get_rows

def test_get_rows_minimal(tmp_path):
    """Get list of rows, as dicts, from one-row, one-column CSV."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "PropertyID\n"
            "http://purl.org/dc/terms/creator\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    config_dict = get_config()
    expected_csvrow_dicts_list = [ {'propertyID': 'http://purl.org/dc/terms/creator'} ]
    assert _get_rows(csvfile_obj, config_dict) == expected_csvrow_dicts_list

def test_get_rows_given_customized_element_alias(tmp_path):
    """Using customized element alias, normalized for case, dashes, underscores."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "Prop_ID\n"
            "http://purl.org/dc/terms/creator\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    config_dict = get_config()
    config_dict["element_aliases"].update({ "propid": "propertyID" })
    expected_csvrow_dicts_list = [ {'propertyID': 'http://purl.org/dc/terms/creator'} ]
    assert _get_rows(csvfile_obj, config_dict) == expected_csvrow_dicts_list

def test_get_rows_fills_in_short_headers_subsequently_with_None(tmp_path):
    """Where headers shorter than rows, extra values collected under header None."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
            "shapeID,propertyID,\n" 
            ":a,dct:creator,URI,comment,comment two\n"
        )
    csvfile_obj = open(csvfile_path)
    expected_output = [
        {
            'shapeID': ':a', 
            'propertyID': 'dct:creator', 
            '': 'URI', 
            None: ['comment', 'comment two']}
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_fills_in_short_headers_first_with_empty_header(tmp_path):
    """Where headers shorter than rows, adds one empty header."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,\n" 
            ":a,dct:creator,URI\n")
        )
    csvfile_obj = open(csvfile_path)
    expected_output = [
        {'shapeID': ':a', 'propertyID': 'dct:creator', '': 'URI'}
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_fills_in_short_rows_with_None_values(tmp_path):
    """Fills in short rows with None values."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueNodeType\n" 
            ":a,dct:creator\n")
        )
    csvfile_obj = open(csvfile_path)
    expected_output = [
        {'shapeID': ':a', 'propertyID': 'dct:creator', 'valueNodeType': None}
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_raises_exception_if_first_line_has_no_propertyid(tmp_path):
    """Raises exception if first line of CSV has no propertyID."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(("shapeID,propertyIdentifier,valueNodeType\n" ":a,dct:creator,URI\n"))
    csvfile_obj = open(csvfile_path)
    config_dict = get_config()
    with pytest.raises(SystemExit):
        _get_rows(csvfile_obj, config_dict)

def test_get_rows_with_unknown_column(tmp_path):
    """Non-DCTAP elements kept by _get_rows (but dropped by _get_shapes)."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueConstraint,value Gestalt\n"
            ":book,dc:creator,,:author\n"
            ",dc:type,so:Book,\n"
            ":author,foaf:name,,\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    expected_csvrow_dicts_list = [
        {
            'shapeID': ':book',
            'propertyID': 'dc:creator',
            'valueConstraint': '',
            'valuegestalt': ':author'
        }, {
            'shapeID': '',
            'propertyID': 'dc:type',
            'valueConstraint': 'so:Book',
            'valuegestalt': ''
        }, {
            'shapeID': ':author',
            'propertyID': 'foaf:name',
            'valueConstraint': '',
            'valuegestalt': ''
        }
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_csvrow_dicts_list

def test_get_rows_with_unknown_column2(tmp_path):
    """Passes thru unknown header, lowercased."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
            "shapeID,propertyID,valueShape,wildCard\n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
            ":author,foaf:name,,\n"
    )
    csvfile_obj = open(csvfile_path)
    expected_output = [
            {
             'shapeID': ':book', 
             'propertyID': 'dcterms:creator', 
             'valueShape': ':author', 
             'wildcard': 'Yeah yeah yeah'
            }, {
              'shapeID': ':author', 
              'propertyID': 'foaf:name', 
              'valueShape': '', 
              'wildcard': ''}
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_with_simple_csvfile(tmp_path):
    """Another simple CSV with three columns."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,valueNodeType\n"
            ":a,dct:creator,URI\n"
            ":a,dct:subject,URI\n"
            ":a,dct:date,String\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    expected_csvrow_dicts_list = [
        {'shapeID': ':a', 'propertyID': 'dct:creator', 'valueNodeType': 'URI'},
        {'shapeID': ':a', 'propertyID': 'dct:subject', 'valueNodeType': 'URI'},
        {'shapeID': ':a', 'propertyID': 'dct:date', 'valueNodeType': 'String'}
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_csvrow_dicts_list

def test_liststatements_with_csv_column_outside_dctap_model_are_ignored(tmp_path):
    """CSV columns not part of the DC TAP model are simply ignored."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,propertyID,confidential\n"
            ":a,dct:subject,True\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    expected_csvrow_dicts_list = [
        {"shapeID": ":a", "propertyID": "dct:subject", "confidential": "True"},
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_csvrow_dicts_list

def test_get_rows_correct_shapeID(tmp_path):
    """Corrects DCTAP headers - redundant to "real mess" test?"""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
            "SID,property-ID\n"
            ":book,dcterms:creator\n"
    )
    csvfile_obj = open(csvfile_path)
    expected_output = [
            {
             'shapeID': ':book', 
             'propertyID': 'dcterms:creator'
            }
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_correct_a_real_mess(tmp_path):
    """Messiness in headers (extra spaces, punctuation, wrong case) is corrected."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
            "S ID,pr-opertyID___,valueShape     ,wildCard    \n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
    )
    csvfile_obj = open (csvfile_path)
    expected_output = [
            { 
             'shapeID': ':book', 
             'propertyID': 'dcterms:creator',
             'valueShape': ':author',
             'wildcard': 'Yeah yeah yeah',
            }
    ]
    config_dict = get_config()
    assert _get_rows(csvfile_obj, config_dict) == expected_output

def test_get_rows_with_complete_csvfile(tmp_path):
    """Simple CSV with all columns."""
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        (
            "shapeID,shapeLabel,propertyID,"
            "propertyLabel,mandatory,repeatable,valueNodeType,"
            "valueDataType,valueConstraint,valueConstraintType,valueShape,note\n"
            ":a,Book,dct:creator,Creator,1,0,URI,,,,:b,Typically the author.\n"
            ":b,Person,ex:name,Name,1,0,Literal,xsd:string,,,,\n"
        )
    )
    csvfile_obj = open(csvfile_path)
    expected_csvrow_dicts_list = [
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
    config_dict = get_config()
    real_output = _get_rows(csvfile_obj, config_dict)
    assert isinstance(real_output, list)
    assert isinstance(expected_csvrow_dicts_list, list)
    assert real_output == expected_csvrow_dicts_list
    assert real_output[0]["mandatory"]
    assert len(real_output) == 2
    assert len(expected_csvrow_dicts_list) == 2
