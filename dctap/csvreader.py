"""Parse DCTAP/CSV, return two-item tuple: list of shape objects, list of warnings."""

from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from pathlib import Path
from dataclasses import asdict
from typing import Dict, List
from pathlib import Path
from .config import get_config
from .exceptions import DctapError
from .tapclasses import TAPShape, TAPStatementConstraint
from .utils import is_uri_or_prefixed_uri


def csvreader(csvfile_obj, config_dict):
    """Passed _io.TextIOWrapper object, return list of TAPShape objects."""
    rows_list = _get_rows(csvfile_obj)
    tapshapes = _get_tapshapes(rows_list, config_dict)[0]
    tapwarnings = _get_tapshapes(rows_list, config_dict)[1]
    return (tapshapes, tapwarnings)


def _get_rows(csvfile_obj):
    """Passed _io.TextIOWrapper object, return list of CSV file rows as dicts."""
    csv_elements_list = _make_csv_elements_list()
    element_aliases_dict = _make_element_aliases(csv_elements_list)
    csvfile_str = csvfile_obj.read()
    tmp_buffer = StringBuffer(csvfile_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(",")
    new_header_line_list = list()
    for header in raw_header_line_list:
        header = _shorten_and_lowercase(header)
        header = _canonicalize_string(header, element_aliases_dict)
        new_header_line_list.append(header)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    new_buffer = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    return list(DictReader(new_buffer))


def _canonicalize_string(some_str, element_aliases_dict):
    """Given some string, returns canonical string or actual string."""
    some_str = _shorten_and_lowercase(some_str)
    for key in element_aliases_dict.keys():
        if key == some_str:
            some_str = element_aliases_dict[key]
    return some_str


def _shorten_and_lowercase(some_str=None):
    """Deletes underscores, dashes, spaces, then lowercases."""
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.lower()
    return some_str


def _make_csv_elements_list():
    """Derives list of CSV row elements from the TAP dataclasses."""
    shape_elements = list(asdict(TAPShape()))
    shape_elements.remove("sc_list")
    shape_elements.remove("start")
    shape_elements.remove("sh_warnings")
    tconstraint_elements = list(asdict(TAPStatementConstraint()))
    tconstraint_elements.remove("sc_warnings")
    return shape_elements + tconstraint_elements


def _make_element_aliases(csv_elements_list=None):
    """From list of CSV row elements: { shortkey/lowerkey: element }."""
    element_aliases_dict = dict()
    for csv_elem in csv_elements_list:
        # shortkey: initial letter (lowercase) + each uppercase letter, lowercased
        shortkey = "".join([csv_elem[0]] + [l.lower() for l in csv_elem if l.isupper()])
        lowerkey = csv_elem.lower()
        element_aliases_dict[shortkey] = csv_elem  # { shortkey: camelcasedValue }
        element_aliases_dict[lowerkey] = csv_elem  # { lowerkey: camelcasedValue }
    return element_aliases_dict


def _get_tapshapes(rows, config_dict) -> List[TAPShape]:
    """Return tuple: list of TAPShape objects and list of any warnings."""
    try:
        dshape = config_dict.get("default_shape_name")
    except KeyError:
        dshape = ":default"

    # fmt: off
    shapes: Dict[str, TAPShape] = dict()            # To make dict for TAPShapes,
    first_valid_row_encountered = True              # read CSV rows as list of dicts.
    warnings = defaultdict(dict)                    # Make defaultdict for warnings.
    # or just dict()?

    def set_shape_fields(shape=None, row=None):     # To set shape-related keys,
        tapshape_keys = list(asdict(TAPShape()))    # make a list of those keys,
        tapshape_keys.remove("start")               # remove start, sc_list, and
        tapshape_keys.remove("sc_list")             # sh_warnings - not
        tapshape_keys.remove("sh_warnings")         # shape fields.
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
                sh_id = row["shapeID"] = dshape     # use default as shapeID and key.
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

        shape.validate()
        shape_warnings = shape.get_warnings()
        for (elem,warn) in shape_warnings.items():  # Iterate Shape warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set new key with value list,
                warnings[sh_id][elem].append(warn)  # and warning can now be added.

        sc = TAPStatementConstraint()               # Instantiate SC for this row.

        for key in list(asdict(sc)):                # Iterate SC fields, to
            try:                                    # populate the SC instance
                setattr(sc, key, row[key])          # with values from the row dict,
            except KeyError:                        # while fields not found in SC
                pass                                # are simply skipped (yes?).

        shapes[sh_id].sc_list.append(sc)            # Add SC to SC list in shapes dict.

        sc.validate()                               # SC validates itself, and 
        sc_warnings = sc.get_warnings()             # emits warnings on request.

        for (elem,warn) in sc_warnings.items():     # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set new key with value list,
                warnings[sh_id][elem].append(warn)  # and warning can now be added.

        tapshapes_dict = _tapshapes_to_dicts(list(shapes.values()))
        warnings_dict = dict(warnings)

    return (                                        # Return tuple:
        tapshapes_dict,                             #   Shapes dictionary
        warnings_dict                               #   Dict of warnings, by shape
    )
    # fmt: on


def _tapshapes_to_dicts(tapshapes_list, verbose=False):
    """Converting TAPShape objects to dicts for generating JSON and YAML."""
    dict_output = {}
    shape_list = []
    dict_output["shapes"] = shape_list
    for tapshape_obj in tapshapes_list:
        tapshape_dict = asdict(tapshape_obj)
        # Removing 'start' for now, not yet part of official DCTAP spec.
        tapshape_dict.pop("start")
        tapshape_dict["statement_constraints"] = tapshape_dict.pop("sc_list")
        shape_list.append(tapshape_dict)

    return dict_output
