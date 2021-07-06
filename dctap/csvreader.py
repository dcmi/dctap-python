"""Parse DCTAP/CSV, return two-item tuple: (list of shape objects, list of warnings)."""

from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from dataclasses import asdict
from typing import Dict
from .exceptions import DctapError
from .tapclasses import TAPShape, TAPStatementConstraint


def csvreader(csvfile_obj, config_dict):
    """From open CSV file object, return tuple: (shapes dict, warnings dict)."""
    rows_list = _get_rows(csvfile_obj, config_dict)
    tapshapes = _get_tapshapes(rows_list, config_dict)[0]
    tapwarnings = _get_tapshapes(rows_list, config_dict)[1]
    return (tapshapes, tapwarnings)


def _get_rows(csvfile_obj, config_dict):
    """Extract from _io.TextIOWrapper object a list of CSV file rows as dicts."""
    csvfile_contents_str = csvfile_obj.read()
    tmp_buffer = StringBuffer(csvfile_contents_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(",")
    new_header_line_list = list()
    for header in raw_header_line_list:
        header = _shorten_and_lowercase(header)
        header = _normalize_element_name(header, config_dict.get("element_aliases"))
        new_header_line_list.append(header)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    return list(DictReader(tmp_buffer2))


def _normalize_element_name(some_str, element_aliases_dict):
    """Normalize a given string (or leave unchanged)."""
    some_str = _shorten_and_lowercase(some_str)
    for key in element_aliases_dict.keys():
        if key == some_str:
            some_str = element_aliases_dict[key]
    return some_str


def _shorten_and_lowercase(some_str=None):
    """For given string, delete underscores, dashes, spaces, then lowercase."""
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.lower()
    return some_str


def _get_customized_element_aliases_from_config_dict(element_aliases_dict, config_dict):
    """Given list of element aliases, adds aliases from config dictionary."""
    element_aliases_dict_plus = dict()
    if config_dict.get("element_aliases"):
        for (key, value) in config_dict.get("element_aliases").items():
            lowerkey = _shorten_and_lowercase(key)
            element_aliases_dict_plus[lowerkey] = value
        element_aliases_dict.update(element_aliases_dict_plus)
    return element_aliases_dict


def _get_tapshapes(rows, config_dict):
    """Return tuple: list of TAPShape objects and list of any warnings."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

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
            set_shape_fields(shape, row)            # set its shape-related fields,
            first_valid_row_encountered = False     # but in first valid row only.

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

        shape.validate(config_dict)
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
#                      statement_constraints.append(sc)

        sc.validate(config_dict)                    # SC validates itself, and
        sc_warnings = sc.get_warnings()             # emits warnings on request.

        for (elem,warn) in sc_warnings.items():     # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set new key with value list,
                warnings[sh_id][elem].append(warn)  # and warning can now be added.

        tapshapes_dict = dict()                     # New dict to hold shapes as dicts.
        shape_list = list()                         # New list for TAPShapes objs, as
        tapshapes_dict["shapes"] = shape_list       # mutable value for key "shapes".
        for tapshape_obj in list(shapes.values()):  # For each TAPShape object in list:
            tapshape_dict = asdict(tapshape_obj)    # - convert object to pure dict,
            tapshape_dict[                          # - rename its field "sc_list" to
                "statement_constraints"             #   "statement_constraints"
            ] = tapshape_dict.pop("sc_list")        # - add that shape dict to mutable
            shape_list.append(tapshape_dict)        #   tapshapes_dict["shapes"]

        warnings_dict = dict(warnings)              # Save warnings as dict.

    return (                                        # Return tuple:
        tapshapes_dict,                             #   Shapes dictionary
        warnings_dict                               #   Dict of warnings, by shape
    )
    # fmt: on
