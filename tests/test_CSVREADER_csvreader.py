"""dctap.csvreader.csvreader."""

import os
from pathlib import Path
import pytest
from dctap.config import get_config
from dctap.csvreader import (
    csvreader,
    _get_prefixes_actually_used,
    _add_namespaces,
    _get_tapshapes,
    _get_rows,
    _add_tapwarns,
)
from dctap.tapclasses import TAPShape, TAPStatementTemplate

NONDEFAULT_CONFIGYAML = """\
prefixes:
    'xsd:': 'http://www.w3.org/2001/XMLSchema#'
    'ex:': 'http://ex.example/#'
    'foaf:': 'http://xmlns.com/foaf/0.1/'
    'my:': 'http://my.example/#'
    'ui:': 'http://ui.example/#'
"""


def test_csvstring_from_tapshex(capsys):
    """CSV string from tapshex project."""
    config_dict = get_config(nondefault_configyaml_str=NONDEFAULT_CONFIGYAML)
    # fmt: off
    #
    csvfile_str = """\
    shapeID            , propertyID      , valueDataType , valueConstraint          , valueConstraintType , valueShape
    my:IssueShape      , ex:state        ,               , ui:accepted ui:resolved  , picklist            ,
                       , ex:reproducedBy ,               ,                          ,                     , my:TesterShape
                       , ex:reproducedBy ,               ,                          ,                     , my:ProgrammerShape
    my:TesterShape     , foaf:name       , xsd:string    ,                          ,                     ,
                       , ex:role         ,               , ex:testingRole           ,                     ,
    my:ProgrammerShape , foaf:name       , xsd:string    ,                          ,                     ,
                       , ex:department   ,               , ex:ProgrammingDepartment ,                     ,
    """
    #
    # fmt: on
    (csvrows, csvwarnings) = _get_rows(csvfile_str=csvfile_str, config_dict=config_dict)
    expected_prefixes = ["my:", "ex:", "xsd:", "foaf:", "ui:"]
    # assert sorted(_get_prefixes_actually_used(csvrows)) == sorted(expected_prefixes)
    expected_dict = {
        "shapes": [
            {
                "shapeID": "my:IssueShape",
                "statement_templates": [
                    {
                        "propertyID": "ex:state",
                        "valueConstraint": ["ui:accepted", "ui:resolved"],
                        "valueConstraintType": "picklist",
                    },
                    {"propertyID": "ex:reproducedBy", "valueShape": "my:TesterShape"},
                    {
                        "propertyID": "ex:reproducedBy",
                        "valueShape": "my:ProgrammerShape",
                    },
                ],
            },
            {
                "shapeID": "my:TesterShape",
                "statement_templates": [
                    {"propertyID": "foaf:name", "valueDataType": "xsd:string"},
                    {
                        "propertyID": "ex:role",
                        "valueConstraint": "ex:testingRole",
                    },
                ],
            },
            {
                "shapeID": "my:ProgrammerShape",
                "statement_templates": [
                    {"propertyID": "foaf:name", "valueDataType": "xsd:string"},
                    {
                        "propertyID": "ex:department",
                        "valueConstraint": "ex:ProgrammingDepartment",
                    },
                ],
            },
        ],
        "namespaces": {
            "xsd:": "http://www.w3.org/2001/XMLSchema#",
            "ex:": "http://ex.example/#",
            "foaf:": "http://xmlns.com/foaf/0.1/",
            "my:": "http://my.example/#",
            "ui:": "http://ui.example/#",
        },
        "warnings": {
            "my:IssueShape": {},
            "my:TesterShape": {},
            "my:ProgrammerShape": {},
        },
    }
    # pylint: disable=invalid-name
    actual_dict = csvreader(
        csvfile_str=csvfile_str,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    assert isinstance(actual_dict, dict)
    assert isinstance(actual_dict["namespaces"], dict)
    assert sorted(actual_dict["namespaces"]) == sorted(expected_dict["namespaces"])
    assert actual_dict["warnings"] == expected_dict["warnings"]
    assert actual_dict["shapes"][1] == expected_dict["shapes"][1]
    assert actual_dict["shapes"][2] == expected_dict["shapes"][2]
    assert actual_dict["shapes"][0] == expected_dict["shapes"][0]
    assert actual_dict == expected_dict
    # with capsys.disabled():
    #     print()
    #     print(sorted(actual_dict["shapes"][0]))
    #     print()
    #     print(sorted(expected_dict["shapes"][0]))


def test_manually_steps_through_csvreader_from_files_to_tapshapes(tmp_path):
    """Step by step from config and csv files to tapshapes."""
    config_dict = get_config()
    csvfile_str = "propertyID,ricearoni\n" "dc:date,SFO treat\n"
    expected_rows_list = [
        {
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        },
    ]
    #
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(csvfile_str, encoding="utf-8")
    open_csvfile_obj = open(csvfile_path, encoding="utf-8")
    (csvrows, csvwarns) = _get_rows(
        open_csvfile_obj=open_csvfile_obj, config_dict=config_dict
    )
    assert csvrows == expected_rows_list
    assert len(csvwarns) == 1
    warning = "Non-DCTAP element 'ricearoni' not configured as extra element."
    assert warning in csvwarns["csv"]["column"]
    #
    (tapshapes, tapwarns) = _get_tapshapes(
        rows=csvrows,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    expected_tapshapes = {
        "shapes": [
            {"shapeID": "default", "statement_templates": [{"propertyID": "dc:date"}]}
        ]
    }
    assert tapshapes == expected_tapshapes
    tapwarns = {**csvwarns, **tapwarns}
    prefixes_used = _get_prefixes_actually_used(csvrows)
    tapshapes = _add_namespaces(
        tapshapes=tapshapes, config_dict=config_dict, prefixes_used=prefixes_used
    )
    tapshapes = _add_tapwarns(tapshapes, tapwarns)
    expected_tapshapes2 = {
        "shapes": [
            {
                "shapeID": "default",
                "statement_templates": [{"propertyID": "dc:date"}],
            }
        ],
        "namespaces": {"dc:": "http://purl.org/dc/elements/1.1/"},
        "warnings": {
            "csv": {
                "column": [
                    "Non-DCTAP element 'ricearoni' not configured as extra element."
                ]
            },
            "default": {"shapeID": ["Value 'default' does not look like a URI."]},
        },
    }
    assert tapshapes == expected_tapshapes2


def test_csvreader_to_tapshapes(tmp_path):
    """From config and csv files to tapshapes with csvreader()."""
    config_dict = get_config()
    csvfile_str = "propertyID,ricearoni\n" "dc:date,SFO treat\n"
    tapshapes_expected = {
        "namespaces": {"dc:": "http://purl.org/dc/elements/1.1/"},
        "shapes": [
            {"shapeID": "default", "statement_templates": [{"propertyID": "dc:date"}]}
        ],
        "warnings": {
            "csv": {
                "column": [
                    "Non-DCTAP element 'ricearoni' not configured as extra element."
                ]
            },
            "default": {"shapeID": ["Value 'default' does not look like a URI."]},
        },
    }
    #
    actual_tapshapes = csvreader(
        csvfile_str=csvfile_str,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    assert actual_tapshapes == tapshapes_expected
    #
    os.chdir(tmp_path)
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(csvfile_str, encoding="utf-8")
    open_csvfile_obj = Path(csvfile_path).open(encoding="utf-8")
    actual_tapshapes = csvreader(
        open_csvfile_obj=open_csvfile_obj,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    assert actual_tapshapes == tapshapes_expected
