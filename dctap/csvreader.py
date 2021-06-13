"""Read DCTAP/CSV (expand prefixes?). Write and read config file."""

from collections import defaultdict
from csv import DictReader
from dataclasses import asdict
from itertools import chain
from operator import methodcaller
from typing import Dict, List
from pathlib import Path
from .exceptions import CsvError
from .classes import TAPShape, TAPStatementConstraint
from .utils import is_uri_or_prefixed_uri

DEFAULT_SHAPE_NAME = ":default"  # replace with call to config reader

def csvreader(csvfile):
    """Return list of TAPShape objects from CSV file."""
    rows = _get_rows(csvfile)
    tapshapes = _get_tapshapes(rows)[0]
    tapwarnings = _get_tapshapes(rows)[1]
    return (tapshapes, tapwarnings)


def _get_rows(csvfile):
    """Return list of row dicts from CSV file."""
    try:
        reader = DictReader(Path(csvfile).open(newline="", encoding="utf-8-sig"))
    except IsADirectoryError:
        raise CsvError("Must be a CSV file.")
    rows = list(reader)
    if "propertyID" not in reader.fieldnames:
        raise CsvError("Valid DCTAP CSV must have a 'propertyID' column.")
    return rows


def _get_tapshapes(rows=None, default=DEFAULT_SHAPE_NAME) -> List[TAPShape]:
    """Return tuple: list of TAPShape objects and list of any warnings."""

    # fmt: off
    shapes: Dict[str, TAPShape] = dict()            # To make dict for TAPShapes,
    first_valid_row_encountered = True              # read CSV rows as list of dicts.
    warnings = defaultdict(dict)                    # Make defaultdict for warnings.
    # or just dict()?

    def set_shape_fields(shape=None, row=None):     # To set shape-related keys,
        tapshape_keys = list(asdict(TAPShape()))    # make a list of those keys,
        tapshape_keys.remove("start")               # remove start and sc_list,
        tapshape_keys.remove("sc_list")             # as both are set elsewhere.
        for key in tapshape_keys:                   # Iterate remaining keys, to
            try:                                    # populate tapshape fields 
                setattr(shape, key, row[key])       # with values from row dict.
            except KeyError:                        # Keys not found in dict,
                pass                                # are simply skipped.
        return shape                                # Return shape with fields set.

    for row in rows:                                # For each row
        if not row["propertyID"]:                   # where no propertyID be found,
            continue                                # ignore and move to next.

        if first_valid_row_encountered:             # In first valid row,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row.get("shapeID")          # use it as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                sh_id = row["shapeID"] = default    # use default as shapeID and key.
            shape = shapes[sh_id] = TAPShape()      # Add a TAPShape to the dict and
            set_shape_fields(shape, row)            # set its shape-related fields, and
            shapes[sh_id].start = True              # set it as the "start" shape,
            first_valid_row_encountered = False     # the one and only.

        if not first_valid_row_encountered:         # In every valid row thereafter,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row["shapeID"]              # use it as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                so_far = list(shapes)               # see list of shapeIDs used so far,
                sh_id = so_far[-1]                  # and may the latest one be key.

        if sh_id not in shapes:                     # If shape ID not in shapes dict,
            shape = shapes[sh_id] = TAPShape()      # add it with value TAPShape, and
            set_shape_fields(shape, row)            # set its shape-related fields, and
            warnings[sh_id] = dict()                # give it key in warnings dict.

        sc = TAPStatementConstraint()               # Instantiate SC for this row.

        for key in list(asdict(sc)):                # Iterate SC fields, to
            try:                                    # populate the SC instance
                setattr(sc, key, row[key])          # with values from the row dict,
            except KeyError:                        # while fields not found in SC
                pass                                # are simply skipped (yes?).

        shapes[sh_id].sc_list.append(sc)            # Add SC to SC list in shapes dict.

        #sc.normalize()                             # SC instance normalizes itself and
        sc.validate()                               # collects warnings, then provides
        sc_warnings = sc.get_warnings()             # those warnings on request.

        for (elem,warn) in sc_warnings.items():     # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set new key with value list,
                warnings[sh_id][elem].append(warn)  # and warning can now be added.

    return (                                        # Return tuple:
        list(shapes.values()),                      #   List of shapes
        dict(warnings)                              #   Dict of warnings, by shape
    )
    # fmt: on
