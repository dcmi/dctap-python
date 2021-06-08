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


def test_dctap_tests_propIDonly(tmp_path):
    """Minimal application profile can have propertyID column only."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/propIDonly.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    rows = _get_rows(local_file)
    assert _get_csvshapes(rows)

def test_dctap_tests_noPropertyID(tmp_path):
    """Exits if no propertyID column - not a valid DCTAP instance."""
    url = "https://raw.githubusercontent.com/dcmi/dctap/main/tests/noPropertyID.csv"
    local_file="local.csv"
    os.chdir(tmp_path)
    read_from_url_saveas(url, local_file)
    with pytest.raises(SystemExit):
        _get_rows(local_file)

""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/IRIwithLiteralDatatype.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/bothBlankAndFilledShapeID.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/literalWithoutDatatype.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/mixOfEmptyCells.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/propIDonly.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/propsBeforeShape.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/readme.md """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/shapeNotReferenced.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/shapewithoutShapeID.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/twoSameShape.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueDataTypeWrong.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeLowercase.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeTwice.csv """
""" https://raw.githubusercontent.com/dcmi/dctap/main/tests/valueNodeTypeWrong.csv """
