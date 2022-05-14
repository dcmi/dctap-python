"""Parse DCTAP/CSV, return two-item tuple: (list of shape objects, list of warnings)."""

from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from dataclasses import asdict
from dctap.config import get_shems, get_stems
from dctap.exceptions import DctapError
from dctap.tapclasses import TAPShape, TAPStatementTemplate


def csvreader(open_csvfile_obj, config_dict):
    """From open CSV file object, return tuple: (shapes dict, warnings dict)."""
    (csvrows, csvwarnings) = _get_rows(open_csvfile_obj, config_dict)
    (tapshapes, tapwarnings) = _get_tapshapes(csvrows, config_dict)
    tapwarnings = {**csvwarnings, **tapwarnings}
    return (tapshapes, tapwarnings)


def _get_tapshapes(rows, config_dict):
    """Return tuple: (shapes dict: warnings dict)."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    try:
        dshape = config_dict.get("default_shape_identifier")
    except KeyError:
        dshape = "default"

    (main_shems, xtra_shems) = get_shems(shape_class=TAPShape, settings=config_dict)
    (main_stems, xtra_stems) = get_stems(
        statement_template_class=TAPStatementTemplate, settings=config_dict
    )

    # fmt: off
    shapes = {}                                     # New dict will hold TAPShapes.
    warnings = defaultdict(dict)                    # New dict will hold warnings.
    first_valid_row_encountered = True              # Only one row can be "first valid".

    for row in rows:                                # For each row
        if not row["propertyID"]:                   # where no propertyID be found,
            continue                                # ignore and move to next.

        if first_valid_row_encountered:             # In very "first" valid row,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row.get("shapeID")          # use as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                sh_id = row["shapeID"] = dshape     # use default shapeID as key.
            new_shape = shapes[sh_id] = TAPShape()  # Add TAPShape obj to shapes dict,
            shape = _set_shape_keys(
                shape_instance=new_shape,
                row_dict=row,
                main_shape_elements=main_shems,
                xtra_shape_elements=xtra_shems,
            )
            first_valid_row_encountered = False     # may future rows be not "first".

        if not first_valid_row_encountered:         # In each valid row thereafter,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row["shapeID"]              # use as a key for shapes dict.
            else:                                   # If no truthy shapeID be found,
                so_far = list(shapes)               # from shapeIDs used so far,
                sh_id = so_far[-1]                  # use the most recent as key.

        if sh_id not in shapes:                     # If shape ID not in shapes dict,
            new_shape = shapes[sh_id] = TAPShape()  # give it value TAPShape object,
            shape = _set_shape_keys(
                shape_instance=new_shape,
                row_dict=row,
                main_shape_elements=main_shems,
                xtra_shape_elements=xtra_shems,
            )
            warnings[sh_id] = {}                    # use as key in warnings dict.

        shape.normalize(config_dict)
        shape_warnings = shape.get_warnings()

        for (elem,warn) in shape_warnings.items():  # Iterate Shape warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings, by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = []          # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        sc = TAPStatementTemplate()                 # Instantiate SC for this row.

        for k in row:
            if k in main_stems:
                try:
                    setattr(sc, k, row[k])
                except KeyError:
                    pass
            elif k in xtra_stems:
                sc.extra_elements[k] = row[k]

        shapes[sh_id].st_list.append(sc)            # Add SC to SC list in shapes dict.

        sc.normalize(config_dict)                   # SC normalizes itself, and
        st_warnings = sc.get_warnings()             # emits warnings on request.

        for (elem, warn) in st_warnings.items():    # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = []          # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        tapshapes_dict = {}                         # Dict will hold shapes as dicts.

        shape_list = []                             # New list for TAPShapes objs, to
        tapshapes_dict["shapes"] = shape_list       # hold on tapshapes_dict["shapes"].

        for tapshape_obj in list(shapes.values()):  # For each TAPShape object in list:
            tapshape_dict = asdict(tapshape_obj)    # - convert object to pure dict,
            tapshape_dict[                          # - rename its field "st_list" to
                "statement_templates"               #   "statement_templates"
            ] = tapshape_dict.pop("st_list")        # - add that shape dict to mutable
            shape_list.append(tapshape_dict)        #   tapshapes_dict["shapes"]

        warnings_dict = dict(warnings)              # Save defaultdict warnings as dict.

    return (                                        # Return tuple:
	_reduce_shapesdict(tapshapes_dict),             #   Shapes dict, empties removed
        warnings_dict                               #   Dict of warnings, by shape
    )
    # fmt: on


def _set_shape_keys(
    shape_instance=None,
    row_dict=None,
    main_shape_elements=None,
    xtra_shape_elements=None,
):
    """
    Populate shape-related keys of dictionary for a named instance of TAPShape.
    Iterate columns, and if header is found to be among default shems, add
    key-value to TAPShape dict. Skip any keys not found in row. Or if header is
    found among extra shape elements, add key-value to list of extra elements on
    TAPShape instance, skipping extra keys not found. Return TAPShape dict.
    """
    for key in row_dict:
        if key in main_shape_elements:
            try:
                setattr(shape_instance, key, row_dict[key])
            except KeyError:
                pass
        elif key in xtra_shape_elements:
            try:
                shape.extra_elements[key] = row_dict[key]
            except KeyError:
                pass
    return shape_instance


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
        for sc in shape["statement_templates"]:
            if sc.get("extra_elements"):
                for (k, v) in sc["extra_elements"].items():
                    sc[k] = v
                    del sc["extra_elements"]
            if sc.get("st_warnings"):
                del sc["st_warnings"]
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
    # pylint: disable=too-many-locals
    csvfile_contents_str = open_csvfile_obj.read()
    tmp_buffer = StringBuffer(csvfile_contents_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    raw_header_line_list = csvlines_stripped[0].split(",")
    new_header_line_list = []

    recognized_elements = config_dict.get("csv_elements")
    xtra_shems = config_dict.get("extra_shape_elements")
    xtra_stems = config_dict.get("extra_statement_template_elements")
    if xtra_shems:
        recognized_elements.extend(xtra_shems)
        for element in xtra_shems:
            config_dict["element_aliases"][element.lower()] = element
    if xtra_stems:
        recognized_elements.extend(xtra_stems)
        for element in xtra_stems:
            config_dict["element_aliases"][element.lower()] = element
    recognized_elements = [elem.lower() for elem in recognized_elements]

    for header in raw_header_line_list:
        header = _lowercase_despace_depunctuate(header)
        header = _normalize_element_name(header, config_dict.get("element_aliases"))
        new_header_line_list.append(header)
    csv_warnings = defaultdict(dict)

    for header in new_header_line_list:
        if header.lower() not in recognized_elements:
            warn = f"Non-DCTAP element {repr(header)} not configured as extra element."
            csv_warnings["csv"] = {}
            csv_warnings["csv"]["header"] = []
            csv_warnings["csv"]["header"].append(warn)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    csv_rows = list(DictReader(tmp_buffer2))
    csv_warnings = dict(csv_warnings)
    return (csv_rows, csv_warnings)
