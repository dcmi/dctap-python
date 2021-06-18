"""Corrective lens for headers:

Under development:
*   _canonicalize_string(some_str, element_aliases_dict)
     Takes 

Done:
*   _shorten_and_lowercase(csvelement)          
     Deletes underscores, dashes, spaces, then lowercases.

*   _make_csv_elements_list()
     Derives list of CSV row elements from the TAP dataclasses.
     No arguments are passed
     csv_elements_list is returned
     csv_elements_list is passed to _make_element_aliases.

*   _make_element_aliases(csv_elements_list)
     From list of CSV row elements: { shortkey/lowerkey: element }.
     csv_elements_list is passed
     element_aliases_dict is returned
     element_aliases_dict is passed to _canonicalize_string

Note: If a dictionary is declared with two identical keys, 
the second key/value declared will clobber the first.
The CSV DictReader will also clobber the key/value pair of the 
first of two items with identical keys.
"""

import os
from csv import DictReader
from io import StringIO as StringBuffer
from pathlib import Path
import pytest
from dataclasses import asdict
from .inspect import pprint_tapshapes, tapshapes_to_dicts
from .csvreader import csvreader
from .tapclasses import TAPShape, TAPStatementConstraint


def _new_get_rows(csvfile):
    """@@"""
    csv_elements_list = _make_csv_elements_list()
    element_aliases_dict = _make_element_aliases(csv_elements_list)
    tmp_buffer = StringBuffer(Path(csvfile).open().read())
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(',')
    new_header_line_list = list()
    for header in raw_header_line_list:
        header = _shorten_and_lowercase(header)
        header = _canonicalize_string(header, element_aliases_dict)
        new_header_line_list.append(header)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    new_buffer = StringBuffer("".join([line + '\n' for line in csvlines_stripped]))
    return list(DictReader(new_buffer))

def test_new_get_rows_correct_shapeID(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shape ID,property-ID\n"
            ":book,dcterms:creator\n"
    )
    expected_output = [
            {'shapeID': ':book', 
             'propertyID': 'dcterms:creator'
            }
    ]
    assert _new_get_rows(csvfile_name) == expected_output


def test_new_get_rows_correct_a_real_mess(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "S ID,pr-opertyID___,valueShape     ,wildCard    \n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
    )
    expected_output = [
            {'shapeID': ':book', 
             'propertyID': 'dcterms:creator',
             'valueShape': ':author',
             'wildcard': 'Yeah yeah yeah',
            }
    ]
    assert _new_get_rows(csvfile_name) == expected_output

#####################################################################


def test_new_get_rows(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shapeID,propertyID,valueShape,wildCard\n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
            ":author,foaf:name,,\n"
    )
    expected_output = [
            {'shapeID': ':book', 
             'propertyID': 'dcterms:creator', 
             'valueShape': ':author', 
             'wildcard': 'Yeah yeah yeah'
            }, {
              'shapeID': ':author', 
              'propertyID': 'foaf:name', 
              'valueShape': '', 
              'wildcard': ''}
    ]
    assert _new_get_rows(csvfile_name) == expected_output


#####################################################################


def _canonicalize_string(some_str, element_aliases_dict):
    """Given some string, returns canonical string or actual string."""
    some_str = _shorten_and_lowercase(some_str)
    for key in element_aliases_dict.keys():
        if key == some_str:
            some_str = element_aliases_dict[key]
    return some_str


def _shorten_and_lowercase(some_str=None):
    """Deletes underscores, dashes, spaces, then lowercases."""
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.lower()
    return some_str


def _make_csv_elements_list():
    """Derives list of CSV row elements from the TAP dataclasses."""
    shape_elements = list(asdict(TAPShape()))
    shape_elements.remove('sc_list')
    shape_elements.remove('start')
    shape_elements.remove('sh_warnings')
    tconstraint_elements = list(asdict(TAPStatementConstraint()))
    tconstraint_elements.remove('sc_warnings')
    return shape_elements + tconstraint_elements


def _make_element_aliases(csv_elements_list=None):
    """From list of CSV row elements: { shortkey/lowerkey: element }."""
    element_aliases_dict = dict()
    for csv_elem in csv_elements_list:
        # shortkey: initial letter (lowercase) + each uppercase letter, lowercased
        shortkey = "".join([ csv_elem[0] ] + [l.lower() for l in csv_elem if l.isupper()])
        lowerkey = csv_elem.lower()
        element_aliases_dict[shortkey] = csv_elem     # { shortkey: camelcasedValue }
        element_aliases_dict[lowerkey] = csv_elem     # { lowerkey: camelcasedValue }
    return element_aliases_dict


#####################################################################
#####################################################################


def test_canonicalize_string():
    """@@@"""
    csv_elements_list = _make_csv_elements_list()
    element_aliases_dict = _make_element_aliases(csv_elements_list)
    assert _canonicalize_string("sid", element_aliases_dict) == "shapeID"
    assert _canonicalize_string("SHAPE ID", element_aliases_dict) == "shapeID"
    assert _canonicalize_string("SHAPE___ID", element_aliases_dict) == "shapeID"
    assert _canonicalize_string("rid", element_aliases_dict) == "rid"


def test_make_element_aliases():
    """@@@"""
    expected_element_aliases_dict = {
        'sid': 'shapeID', 
        'sl': 'shapeLabel', 
        'pid': 'propertyID', 
        'pl': 'propertyLabel', 
        'm': 'mandatory', 
        'r': 'repeatable', 
        'vnt': 'valueNodeType', 
        'vdt': 'valueDataType', 
        'vc': 'valueConstraint', 
        'vct': 'valueConstraintType', 
        'vs': 'valueShape', 
        'n': 'note',
        'shapeid': 'shapeID', 
        'shapelabel': 'shapeLabel', 
        'propertyid': 'propertyID', 
        'propertylabel': 'propertyLabel', 
        'mandatory': 'mandatory', 
        'repeatable': 'repeatable', 
        'valuenodetype': 'valueNodeType', 
        'valuedatatype': 'valueDataType', 
        'valueconstraint': 'valueConstraint', 
        'valueconstrainttype': 'valueConstraintType', 
        'valueshape': 'valueShape', 
        'note': 'note',
    }
    csv_elements_list = _make_csv_elements_list()
    assert _make_element_aliases(csv_elements_list) == expected_element_aliases_dict


def test_shorten_and_lowercase():
    """@@@"""
    assert _shorten_and_lowercase("Property ID") == "propertyid"
    assert _shorten_and_lowercase("Property__ID") == "propertyid"
    assert _shorten_and_lowercase("Property-ID") == "propertyid"


def test_new_get_rows(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shapeID,propertyID,valueShape,wildCard\n"
            ":book,dcterms:creator,:author,Yeah yeah yeah\n"
            ":author,foaf:name,,\n"
    )
    expected_output = [
            {'shapeID': ':book', 
             'propertyID': 'dcterms:creator', 
             'valueShape': ':author', 
             'wildcard': 'Yeah yeah yeah'
            }, {
              'shapeID': ':author', 
              'propertyID': 'foaf:name', 
              'valueShape': '', 
              'wildcard': ''
            }
    ]
    assert _new_get_rows(csvfile_name) == expected_output


def test_new_get_rows_even_if_incorrect(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "SID,property ID\n"
            ":book,dcterms:creator\n"
    )
    expected_output = [
            {'shapeID': ':book', 
             'propertyID': 'dcterms:creator'
            }
    ]
    assert _new_get_rows(csvfile_name) == expected_output


#####################################################################

def _preprocess_csvfile_thisworks_better(csvfile):
    """@@@"""
    tmp_buffer = StringBuffer(Path(csvfile).open().read())
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(',')
    new_header_line_list = list()
    for header in raw_header_line_list:
        new_header_line_list.append(header)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    return "".join([line + '\n' for line in csvlines_stripped])


def test_preprocess_csvfile_thisworks_better_too(tmp_path):
    """Is this identical to the one below?"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    expected_output = (
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    assert _preprocess_csvfile_thisworks_better(csvfile_name) == expected_output


def test_preprocess_csvfile_thisworks_better(tmp_path):
    """Is this identical to the one above?"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    expected_output = (
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    assert _preprocess_csvfile_thisworks_better(csvfile_name) == expected_output

#####################################################################

def _preprocess_csvfile_thisworks(csvfile):
    """@@@"""
    tmp_buffer = StringBuffer(Path(csvfile).open().read())
    some_list = list(tmp_buffer)
    # some_list: ['shapeID,propertyID\n', ':book,dcterms:creator\n']
    return "".join(some_list)

def test_preprocess_csvfile_thisworks(tmp_path):
    """@@@"""
    os.chdir(tmp_path)
    csvfile_name = Path(tmp_path).joinpath("some.csv")
    csvfile_name.write_text(
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    expected_output = (
            "shapeID,propertyID\n"
            ":book,dcterms:creator\n"
    )
    assert _preprocess_csvfile_thisworks(csvfile_name) == expected_output

