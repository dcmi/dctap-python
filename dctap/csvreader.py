"""Parse DCTAP/CSV, return two-item tuple: (list of shape objects, list of warnings)."""

from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from dataclasses import asdict
from dctap.config import shape_elements, statement_constraint_elements
from dctap.exceptions import DctapError
from dctap.tapclasses import TAPShape, TAPStatementConstraint


def csvreader(open_csvfile_obj, config_dict):
    """From open CSV file object, return tuple: (shapes dict, warnings dict)."""
    csvrows, csvwarnings = _get_rows(open_csvfile_obj, config_dict)
    tapshapes, tapwarnings  = _get_tapshapes(csvrows, config_dict)
    tapwarnings = { **csvwarnings, **tapwarnings }
    return (tapshapes, tapwarnings)


def _get_tapshapes(rows, config_dict):
    """Return tuple: { shape objects as dicts : warnings as dicts }."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    try:
        dshape = config_dict.get("default_shape_identifier")
    except KeyError:
        dshape = "default"

    sh_elements, xtra_sh_elements = shape_elements(
        shape_class=TAPShape, settings=config_dict
    )
    sc_elements, xtra_sc_elements = statement_constraint_elements(
        statement_constraint_class=TAPStatementConstraint, settings=config_dict
    )

    # fmt: off
    shapes = dict()                                 # Init a dict for TAPShapes,
    first_valid_row_encountered = True              # read CSV rows as list of dicts.
    warnings = defaultdict(dict)                    # Init defaultdict for warnings.

    def set_shape_fields(shape=None, row=None):     # To set shape-related keys,
        for col in row:                             # Iterate remaining keys, to
            if col in sh_elements:
                try:                                    # populate tapshape fields
                    setattr(shape, col, row[col])       # with values from row dict.
                except KeyError:                        # Values not found in row dict,
                    pass                                # are simply skipped.
            elif col in xtra_sh_elements:
                shape.extra_elements[col] = row[col]
        return shape                                # Return shape with fields set.

    for row in rows:                                # For each row
        if not row["propertyID"]:                   # where no propertyID be found,
            continue                                # ignore and move to next.

        if first_valid_row_encountered:             # In very "first" valid row,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row.get("shapeID")          # use as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                sh_id = row["shapeID"] = dshape     # use default shapeID as key.
            shape = shapes[sh_id] = TAPShape()      # Add TAPShape obj to shapes dict,
            set_shape_fields(shape, row)            # populate its shape elements, and
            first_valid_row_encountered = False     # may future rows be not "first".

        if not first_valid_row_encountered:         # In each valid row thereafter,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row["shapeID"]              # use as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                so_far = list(shapes)               # from shapeIDs used so far,
                sh_id = so_far[-1]                  # use the most recent as key.

        if sh_id not in shapes:                     # If shape ID not in shapes dict,
            shape = shapes[sh_id] = TAPShape()      # give it value TAPShape object,
            set_shape_fields(shape, row)            # populate its shape elements, and
            warnings[sh_id] = dict()                # use as key in warnings dict.

        shape.normalize(config_dict)
        shape_warnings = shape.get_warnings()

        for (elem,warn) in shape_warnings.items():  # Iterate Shape warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings, by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        # breakpoint(context=5)
        sc = TAPStatementConstraint()               # Instantiate SC for this row.

        for col in row:
            if col in sc_elements:
                try:
                    setattr(sc, col, row[col])
                except KeyError:
                    pass
            elif col in xtra_sc_elements:
                sc.extra_elements[col] = row[col]

        shapes[sh_id].sc_list.append(sc)            # Add SC to SC list in shapes dict.

        sc.normalize(config_dict)                   # SC normalizes itself, and
        sc_warnings = sc.get_warnings()             # emits warnings on request.

        for (elem, warn) in sc_warnings.items():    # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = list()      # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        tapshapes_dict = dict()                     # Dict will hold shapes as dicts.

        shape_list = list()                         # New list for TAPShapes objs, to
        tapshapes_dict["shapes"] = shape_list       # hold on tapshapes_dict["shapes"].

        # breakpoint(context=5)
        for tapshape_obj in list(shapes.values()):  # For each TAPShape object in list:
            tapshape_dict = asdict(tapshape_obj)    # - convert object to pure dict,
            tapshape_dict[                          # - rename its field "sc_list" to
                "statement_constraints"             #   "statement_constraints"
            ] = tapshape_dict.pop("sc_list")        # - add that shape dict to mutable
            shape_list.append(tapshape_dict)        #   tapshapes_dict["shapes"]

        warnings_dict = dict(warnings)              # Save defaultdict warnings as dict.

    return (                                        # Return tuple:
	_reduce_shapesdict(tapshapes_dict),         #   Shapes dict, empties removed
        warnings_dict                               #   Dict of warnings, by shape
    )
    # fmt: on


def _lowercase_despace_depunctuate(some_str=None):
    """For given string, delete underscores, dashes, spaces, then lowercase."""
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.lower()
    return some_str


def _normalize_element_name(some_str, element_aliases_dict=None):
    """Normalize a given string (or leave unchanged)."""
    some_str = _lowercase_despace_depunctuate(some_str)
    if element_aliases_dict:
        for key in element_aliases_dict.keys():
            if key == some_str:
                some_str = element_aliases_dict[key]
    return some_str


def _reduce_shapesdict(shapes_dict):
    """Iteratively remove elements from shapes dictionary with falsy values."""
    for shape in shapes_dict["shapes"]:
        for sc in shape["statement_constraints"]:
            if sc.get("extra_elements"):
                for (k, v) in sc["extra_elements"].items():
                    sc[k] = v
                    del sc["extra_elements"]
            if sc.get("sc_warnings"):
                del sc["sc_warnings"]
            for empty_element in [key for key in sc if not sc[key]]:
                del sc[empty_element]
        if shape.get("extra_elements"):
            for (k, v) in shape["extra_elements"].items():
                shape[k] = v
                del shape["extra_elements"]
        if shape.get("sh_warnings"):
            del shape["sh_warnings"]
        for empty_element in [key for key in shape if not shape[key]]:
            del shape[empty_element]
    return shapes_dict


def _get_rows(open_csvfile_obj, config_dict):
    """Extract from _io.TextIOWrapper object a list of CSV file rows as dicts."""
    csvfile_contents_str = open_csvfile_obj.read()
    tmp_buffer = StringBuffer(csvfile_contents_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(",")
    new_header_line_list = list()
    for header in raw_header_line_list:
        header = _lowercase_despace_depunctuate(header)
        header = _normalize_element_name(header, config_dict.get("element_aliases"))
        new_header_line_list.append(header)
    csv_warnings = dict()
    extra_sc_elements = config_dict.get("extra_statement_constraint_elements")
    recognized_elements = config_dict.get("csv_elements")
    if config_dict.get("extra_shape_elements"):
        recognized_elements.extend(config_dict.get("extra_shape_elements"))
    if config_dict.get("extra_statement_constraint_elements"):
        recognized_elements.extend(config_dict.get("extra_statement_constraint_elements"))
    breakpoint(context=5)
    for header in new_header_line_list:
        if header not in config_dict.get("csv_elements"):
           csv_warnings["csv_warnings"] = list()
           csv_warnings["csv_warnings"].append(
                f"{repr(header)} not recognized as DCTAP element "
                "or configured as 'extra' element"
           )
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    return (
        list(DictReader(tmp_buffer2)),
        csv_warnings
    )

