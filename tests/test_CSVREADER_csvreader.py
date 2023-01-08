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


def test_manually_steps_through_csvreader_from_files_to_tapshapes(tmp_path):
    """Step by step from config and csv files to tapshapes."""
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "propertyID,ricearoni\ndc:date,SFO treat\n", encoding="utf-8"
    )
    open_csvfile_obj = open(csvfile_path, encoding="utf-8")
    expected_rows_list = [
        {
            "propertyID": "dc:date",
            "ricearoni": "SFO treat",
        },
    ]
    csvrows, csvwarns = _get_rows(open_csvfile_obj, config_dict)
    assert csvrows == expected_rows_list
    assert len(csvwarns) == 1
    warning = "Non-DCTAP element 'ricearoni' not configured as extra element."
    assert warning in csvwarns["csv"]["column"]
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
    os.chdir(tmp_path)
    config_dict = get_config()
    csvfile_path = Path(tmp_path).joinpath("some.csv")
    csvfile_path.write_text(
        "propertyID,ricearoni\ndc:date,SFO treat\n", encoding="utf-8"
    )
    open_csvfile_obj = Path(csvfile_path).open(encoding="utf-8")
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
    actual_tapshapes = csvreader(
        open_csvfile_obj=open_csvfile_obj,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    assert actual_tapshapes == tapshapes_expected
