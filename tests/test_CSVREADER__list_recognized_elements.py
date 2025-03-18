"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from dctap.config import get_config
from dctap.csvreader import _list_recognized_elements


def test_list_headers_builtins():
    """Return list of builtin headers."""
    config_dict = get_config()
    expected_builtin_csv_elements = [
        "shapeID",
        "shapeLabel",
        "propertyID",
        "propertyLabel",
        "mandatory",
        "repeatable",
        "valueNodeType",
        "valueDataType",
        "valueConstraint",
        "valueConstraintType",
        "valueShape",
        "note",
    ]
    actual_builtin_csv_elements = config_dict.get("csv_elements")
    assert actual_builtin_csv_elements == expected_builtin_csv_elements
    assert config_dict.get("extra_shape_elements") == []
    assert config_dict.get("extra_statement_template_elements") == []
    actual_recognized_elements = _list_recognized_elements(config_dict)
    expected_recognized_csv_elements = [
        "shapeid",
        "shapelabel",
        "propertyid",
        "propertylabel",
        "mandatory",
        "repeatable",
        "valuenodetype",
        "valuedatatype",
        "valueconstraint",
        "valueconstrainttype",
        "valueshape",
        "note",
    ]
    assert actual_recognized_elements == expected_recognized_csv_elements


def test_list_headers_builtins_plus_extras():
    """Return list of builtin headers plus extras."""
    config_dict = get_config()
    config_dict["extra_shape_elements"] = ["closed"]
    config_dict["extra_statement_template_elements"] = ["status"]
    builtin_csv_elements = [
        "shapeID",
        "shapeLabel",
        "propertyID",
        "propertyLabel",
        "mandatory",
        "repeatable",
        "valueNodeType",
        "valueDataType",
        "valueConstraint",
        "valueConstraintType",
        "valueShape",
        "note",
    ]
    expected_csv_elements = builtin_csv_elements + ["closed", "status"]
    assert config_dict.get("extra_shape_elements") == ["closed"]
    assert config_dict.get("extra_statement_template_elements") == ["status"]
    actual_recognized_elements = _list_recognized_elements(config_dict=config_dict)
    expected_recognized_elements = [
        "shapeid",
        "shapelabel",
        "propertyid",
        "propertylabel",
        "mandatory",
        "repeatable",
        "valuenodetype",
        "valuedatatype",
        "valueconstraint",
        "valueconstrainttype",
        "valueshape",
        "note",
        "closed",
        "status",
    ]
    assert actual_recognized_elements == expected_recognized_elements
