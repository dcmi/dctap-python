"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from pathlib import Path
from dctap.inspect import pprint_csvshapes
from dctap.csvreader import csvreader

INSPECTFILE_BASENAMES = [str(f).removesuffix(".inspect") for f in Path('examples').rglob('*.inspect')]


def compare_csvfile_to_inspectoutput(csvfile_basename=None):
    csvfile_fullname = csvfile_basename + ".csv"
    print(f"Testing {csvfile_fullname}")
    inspectfile_fullname = csvfile_basename + ".inspect"
    csvshapes_list = csvreader(csvfile_fullname)
    output_computed = pprint_csvshapes(csvshapes_list)
    output_ondisk = [j for j in Path(inspectfile_fullname).read_text().split('\n') if j]
    assert output_computed == output_ondisk


#def test_good_example():
#    compare_csvfile_to_inspectoutput('absolute_minimal_profile')


def test_good_examples():
    for basename in INSPECTFILE_BASENAMES:
        compare_csvfile_to_inspectoutput(basename)


