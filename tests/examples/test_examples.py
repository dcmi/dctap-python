"""Read CSV file and return list of rows as Python dictionaries."""

import pytest
from pathlib import Path
from dctap.inspect import pprint_csvshapes
from dctap.csvreader import csvreader


def test_absolute_minimal_profile():
    """Absolute minimal profile: just one propertyID column."""
    csvshapes_list = csvreader("absolute_minimal_profile.csv")
    output_computed = pprint_csvshapes(csvshapes_list)
    output_ondisk = [l for l in Path("absolute_minimal_profile.inspect").read_text().split('\n') if l]
    assert output_computed == output_ondisk


