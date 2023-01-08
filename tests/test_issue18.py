"""See https://github.com/dcmi/dctap-python/issues/18#issue-1274937034 ."""

import _io
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from dctap.config import get_config
from dctap.csvreader import (
    csvreader,
    _get_rows,
    _get_tapshapes,
    _add_tapwarns,
    _add_namespaces,
)
from dctap.defaults import CONFIGYAML, CONFIGFILE
from dctap.tapclasses import TAPShape, TAPStatementTemplate

ISSUE18_CONFIGYAML = """### dctap configuration file (in YAML format)
extra_statement_template_elements:
- severity

element_aliases:
     "Mand": "mandatory"
     "Rep": "repeatable"
"""


def test_get_config_from_issue18_yamldoc(tmp_path):
    """Get config dict when passed Issue 18 YAML."""
    os.chdir(tmp_path)
    Path(CONFIGFILE).write_text(ISSUE18_CONFIGYAML)
    assert Path(CONFIGFILE).is_file()
    config_dict = get_config()
    assert config_dict["element_aliases"] == {"Mand": "mandatory", "Rep": "repeatable"}
    assert config_dict["extra_statement_template_elements"] == ["severity"]


def test_get_element_aliases_from_default_yamldoc(tmp_path):
    """Get config dict (with element aliases) directly from built-in defaults."""
    os.chdir(tmp_path)
    config_dict = get_config(default_configyaml_str=CONFIGYAML)
    assert config_dict["element_aliases"]["propertyid"] == "propertyID"
    assert config_dict["element_aliases"]["mandatory"] == "mandatory"
    assert config_dict["element_aliases"]["repeatable"] == "repeatable"


def test_extra_statement_template_elements(tmp_path):
    """@@@."""
    os.chdir(tmp_path)
    nondefault_configyaml_str = """
    extra_statement_template_elements:
    - severity
    """
    config_dict = get_config(nondefault_configyaml_str=nondefault_configyaml_str)
    assert config_dict["extra_statement_template_elements"] == ["severity"]

    contents = """propertyID,severity\ncreator,True\n"""
    Path("somecsv.csv").write_text(contents)
    csvfile_path = Path("somecsv.csv")
    assert csvfile_path.is_file()
    assert csvfile_path.read_text() == contents
    open_csvfile_obj = Path(csvfile_path).open(encoding="utf-8")
    assert isinstance(open_csvfile_obj, _io.TextIOWrapper)

    expected_tapshapes = {
        "shapes": [
            {
                "shapeID": "default",
                "statement_templates": [{"propertyID": "creator", "severity": "True"}],
            }
        ],
        "namespaces": {},
        "warnings": {
            "default": {"shapeID": ["Value 'default' does not look like a URI."]}
        },
    }
    assert isinstance(expected_tapshapes, dict)

    actual_tapshapes = csvreader(
        open_csvfile_obj=open_csvfile_obj,
        config_dict=config_dict,
        shape_class=TAPShape,
        state_class=TAPStatementTemplate,
    )
    assert actual_tapshapes == expected_tapshapes
