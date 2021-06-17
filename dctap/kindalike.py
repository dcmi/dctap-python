"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from ruamel.yaml import YAML
from dataclasses import asdict
import click
from .inspect import pprint_tapshapes, tapshapes_to_dicts
from .csvreader import csvreader, _get_rows
from .tapclasses import TAPShape, TAPStatementConstraint
from .loggers import stderr_logger, warning_logger, debug_logger

## This will take _get_rows() output: list of dictionaries, 
## where each row is a dictionary - shape elements and statement 
## constraint elements together
#     expected_csvrow_dicts_list = [
#         {
#             'shapeID': ':book',
#             'propertyID': 'dc:creator',
#             'valueConstraint': '',
#             'valueShape': ':author'
#         }, {
#             'shapeID': '',
#             'propertyID': 'dc:type',
#             'valueConstraint': 'so:Book',
#             'valueShape': ''
#         }, {
#             'shapeID': ':author',
#             'propertyID': 'foaf:name',
#             'valueConstraint': '',
#             'valueShape': ''
#         }
#     ]

#     shape_elements = list(asdict(TAPShape()))
#     shape_elements.remove('sc_list')
#     shape_elements.remove('start')
#     shape_elements.remove('sh_warnings')
#     tconstraint_elements = list(asdict(TAPStatementConstraint()))
#     tconstraint_elements.remove('sc_warnings')
#     all_elements = shape_elements + tconstraint_elements

# Will use csvreader._get_rows()
# - note: would need to normalize "if propertyID not in..."

def normalize_dictkey(dictkey=None):
    """@@@"""
    dictkey = dictkey.replace(" ", "")
    dictkey = dictkey.replace("_", "")
    dictkey = dictkey.lower()

def string_kindalike(canonical_str=None, given_str=None):
    """Tests whether given string matches canonical as per fuzzy criteria."""
    line_number = 1
    for line in csvfile:
        if line_number == 1:
        output.append(line)
    print(output)

if __name__ == "__main__": 
    new_rowlist = list()
    for row in rows:
        new_row = dict()
        for dictkey in row.keys():
            fake_dictkey = normalize_dictkey(dictkey)
>>> from dctap import TAPShape, TAPStatementConstraint
... all_elements = list(asdict(TAPShape())) + list(asdict(TAPStatementConstraint()))
>>> abbrev_dict = dict()
>>> for elem in all_elements:
...     dict_key = "".join([ elem[0] ] + [l.lower() for l in elem if l.isupper()])
...     abbrev_dict[dict_key] = elem
...
>>> abbrev_dict
{'sid': 'shapeID', 'sl': 'shapeLabel', 's': 'sc_list', 'pid': 'propertyID', 'pl': 'propertyLabel', 'm': 'mandatory', 'r': 'repeatable', 'vnt': 'valueNodeType', 'vdt': 'valueDataType', 'vc': 'valueConstraint', 'vct': 'valueConstraintType', 'vs': 'valueShape', 'n': 'note'}
>>> abbrev_dict = dict()
>>> for elem in all_elements:
...     dict_key = "".join([ elem[0] ] + [l.lower() for l in elem.lower() if l.isupper()])
...     abbrev_dict[dict_key] = elem
...
>>> abbrev_dict = dict()
>>> for elem in all_elements:
...     dict_key = "".join([ elem[0] ] + [l.lower() for l in elem.lower() if l.isupper()])
...     abbrev_dict[dict_key] = elem
...
>>> abbrev_dict
{'s': 'sc_list', 'p': 'propertyLabel', 'm': 'mandatory', 'r': 'repeatable', 'v': 'valueShape', 'n': 'note'}
>>> abbrev_dict = dict()
>>> for elem in all_elements:
...     dict_key = "".join([ elem[0] ] + [l.lower() for l in elem if l.isupper()])
...     abbrev_dict[dict_key] = elem
...
>>> abbrev_dict
{'sid': 'shapeID', 'sl': 'shapeLabel', 's': 'sc_list', 'pid': 'propertyID', 'pl': 'propertyLabel', 'm': 'mandatory', 'r': 'repeatable', 'vnt': 'valueNodeType', 'vdt': 'valueDataType', 'vc': 'valueConstraint', 'vct': 'valueConstraintType', 'vs': 'valueShape', 'n': 'note'}
>>> elem_dict = dict()
>>> for elem in all_elements:
...     elem_dict[elem.lower()] = elem
...
>>> elem_dict
{'shapeid': 'shapeID', 'shapelabel': 'shapeLabel', 'start': 'start', 'sc_list': 'sc_list', 'propertyid': 'propertyID', 'propertylabel': 'propertyLabel', 'mandatory': 'mandatory', 'repeatable': 'repeatable', 'valuenodetype': 'valueNodeType', 'valuedatatype': 'valueDataType', 'valueconstraint': 'valueConstraint', 'valueconstrainttype': 'valueConstraintType', 'valueshape': 'valueShape', 'note': 'note'}
