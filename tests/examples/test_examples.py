"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from pathlib import Path
from dctap.inspect import pprint_csvshapes
from dctap.csvreader import csvreader


# def compare_csvfile_to_inspectoutput(input_file=None, output_file=None):
#     csvshapes_list = csvreader(input_file)
#     output_computed = pprint_csvshapes(csvshapes_list)
#     output_ondisk = [j for j in Path(output_file).read_text().split('\n') if j]
#     assert output_computed == output_ondisk


def compare_csvfile_to_inspectoutput(csvfile_basename=None):
    csvfile_fullname = csvfile_basename + ".csv"
    inspectfile_fullname = csvfile_basename + ".inspect"
    csvshapes_list = csvreader(csvfile_fullname)
    output_computed = pprint_csvshapes(csvshapes_list)
    output_ondisk = [j for j in Path(inspectfile_fullname).read_text().split('\n') if j]
    assert output_computed == output_ondisk


def test_absolute_minimal_profile():
    """Absolute minimal profile: just one propertyID column."""
    csvshapes_list = csvreader("absolute_minimal_profile.csv")
    output_computed = pprint_csvshapes(csvshapes_list)
    output_ondisk = [l for l in Path("absolute_minimal_profile.inspect").read_text().split('\n') if l]
    assert output_computed == output_ondisk

#def test_absolute_minimal_profile2():
#    compare_csvfile_to_inspectoutput('absolute_minimal_profile.csv', 'absolute_minimal_profile.inspect')

def test_absolute_minimal_profile2():
    compare_csvfile_to_inspectoutput('absolute_minimal_profile')

