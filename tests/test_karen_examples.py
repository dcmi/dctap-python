"""Tests from https://github.com/dcmi/dctap/tree/main/tests ."""

import os
import pytest
from urllib.request import urlopen
from dctap.csvreader import _get_csvshapes, _get_rows
from dctap.csvshape import CSVShape, CSVStatementConstraint


def read_from_url_saveas(url, saveas="local.txt"):
    """Read text file from https://raw.githubusercontent.com, save locally."""
    with open(saveas, 'w') as fout:
        fout.writelines([line.decode('utf-8') for line in urlopen(url)])


def test_karen_propIDonly_PASSES(tmp_path):
    """Minimal application profile can have propertyID column only."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/propIDonly.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    assert _get_csvshapes(rows)


def test_karen_noPropertyID_RAISES_EXCEPTION(tmp_path):
    """Exits if no propertyID column - not a valid DCTAP instance."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/noPropertyID.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    with pytest.raises(SystemExit):
        _get_rows(local_file)


def test_karen_propsBeforeShape_PASSES(tmp_path):
    """Order of columns does not matter."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/propsBeforeShape.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    assert _get_csvshapes(rows)


def test_karen_twoSameShape_PASSES(tmp_path):
    """shapeID appears more than once, but without intervening shapes."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/twoSameShape.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    assert _get_csvshapes(rows)
    assert len(_get_csvshapes(rows)) == 2


def test_karen_mixOfEmptyCells_PASSES(tmp_path):
    """shapeID appears more than once, but with intervening shapes."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/mixOfEmptyCells.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    assert _get_csvshapes(rows)
    assert len(_get_csvshapes(rows)) == 2


def test_karen_valueNodeTypeLowercase_PASSES(tmp_path):
    """valueNodeType in lower case."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeLowercase.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    shapes_list = _get_csvshapes(rows)
    config_dict = dict()
    config_dict['value_node_types'] = ["URI", "BNode", "literal"]
    assert _get_csvshapes(rows)
    for shape in shapes_list:
        for statconstraint in shape.sc_list:
            statconstraint._normalize_value_node_type(config_dict)
            if statconstraint.valueNodeType:
                assert statconstraint.valueNodeType

""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/IRIwithLiteralDatatype.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/bothBlankAndFilledShapeID.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/literalWithoutDatatype.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/propIDonly.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/shapeNotReferenced.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/shapewithoutShapeID.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueDataTypeWrong.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeTwice.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeWrong.csv """
