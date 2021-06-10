"""Read DCTAP/CSV (expand prefixes?). Write and read config file."""

from csv import DictReader
from dataclasses import asdict
from typing import Dict, List
from pathlib import Path
from .exceptions import CsvError
from .classes import TAPShape, TAPStatementConstraint

DEFAULT_SHAPE_NAME = ":default"  # replace with call to config reader


def csvreader(csvfile):
    """Return list of TAPShape objects from CSV file."""
    rows = _get_rows(csvfile)
    csvshapes = _get_csvshapes(rows)
    return csvshapes


def _get_rows(csvfile):
    """Return list of row dicts from CSV file."""
    try:
        reader = DictReader(Path(csvfile).open(newline="", encoding="utf-8-sig"))
    except IsADirectoryError:
        raise CsvError("Must be a CSV file")
    rows = list(reader)
    if "propertyID" not in reader.fieldnames:
        raise CsvError("Valid DCTAP CSV must have a 'propertyID' column.")
    return rows


def _get_csvshapes(rows=None, default=DEFAULT_SHAPE_NAME) -> List[TAPShape]:
    """Return list of TAPShape objects from list of row dicts."""

    # fmt: off
    shapes: Dict[str, TAPShape] = dict()          # To make dict indexing TAPShapes,
    first_valid_row_encountered = True              # read CSV rows as list of dicts.

    def set_shape_fields(shape=None, row=None):     # To set shape-related keys,
        csvshape_keys = list(asdict(TAPShape()))  # make a list of those keys,
        csvshape_keys.remove("start")               # remove start and sc_list,
        csvshape_keys.remove("sc_list")             # as both are set elsewhere.
        for key in csvshape_keys:                   # Iterate remaining keys, to
            try:                                    # populate csvshape fields
                setattr(shape, key, row[key])       # with values from the row dict.
            except KeyError:                        # Keys not found in dict,
                pass                                # are simply skipped.
        return shape                                # Return shape with fields set.

    for row in rows:                                # For each row,
        if not row["propertyID"]:                   # where no propertyID be found,
            continue                                # ignore it and move to next.

        if first_valid_row_encountered:             # In first valid row,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row.get("shapeID")          # be it a key for the shapes dict.
            else:                                   # If no truthy shapeID be found,
                sh_id = row["shapeID"] = default    # may default be the key.
            shape = shapes[sh_id] = TAPShape()    # Add a TAPShape to the dict and
            set_shape_fields(shape, row)            # set its shape-related fields, and
            shapes[sh_id].start = True              # set it be the "start" shape,
            first_valid_row_encountered = False     # the one and only.

        if not first_valid_row_encountered:         # In every valid row thereafter,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row["shapeID"]              # be it a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                so_far = list(shapes)               # see list of shapeIDs used so far,
                sh_id = so_far[-1]                  # and may the latest one be key.

        if sh_id not in shapes:                     # If shape key not be found in dict,
            shape = shapes[sh_id] = TAPShape()    # add it with value TAPShape, and
            set_shape_fields(shape, row)            # set its shape-related fields.

        sc = TAPStatementConstraint()             # Make a new SC object, and
        for key in list(asdict(sc)):                # iterate SC-related keys, to
            try:                                    # populate that object,
                setattr(sc, key, row[key])          # with values from the row dict,
            except KeyError:                        # while keys not used in dict
                pass                                # are simply skipped.

        shapes[sh_id].sc_list.append(sc)            # Add SC to SCs list in shapes dict.

    return list(shapes.values())                    # Return list of shapes.
    # fmt: on
