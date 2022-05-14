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

    for row in rows:                                # Examine each row in turn:
        if row.get("shapeID"):                      # If shapeID exists, and is truthy,
            pass                                    # proceed. Alternatively:
        elif not row.get("propertyID"):             # If propertyID does not exist,
            continue                                # or is not truthy, skip the row.

        if not first_valid_row_encountered:         # In each "post-first valid" row,
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row["shapeID"]              # use its value for shapeID.
            else:                                   # If no truthy shapeID be found,
                so_far = list(shapes)               # then from shapeIDs used so far,
                sh_id = so_far[-1]                  # use most recent for shapeID.

        if first_valid_row_encountered:             # In "first valid" row:
            if row.get("shapeID"):                  # if truthy shapeID be found,
                sh_id = row.get("shapeID")          # use its value for shapeID.
            else:                                   # If no truthy shapeID be found,
                sh_id = row["shapeID"] = dshape     # use default value for shapeID.
            first_valid_row_encountered = False     # Future rows be not "first valid".

        if sh_id not in shapes:                     # If shapeID not yet in shapes dict,
            new_shape = shapes[sh_id] = TAPShape()  # make a new TAPShape object,
            shape = _set_shape_fields(              # add to shapes dict with shapeID
                tapshape_obj=new_shape,
                row_dict=row,
                main_shape_elements=main_shems,
                xtra_shape_elements=xtra_shems,
            )
            warnings[sh_id] = {}                    # use as key in warnings dict.

        shape.normalize(config_dict)
        shape_warnings = shape.get_warnings()

        for (elem, warn) in shape_warnings.items(): # Iterate Shape warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings, by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = []          # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        sc = TAPStatementTemplate()                 # For this row make a new
        for key in row:                             # Statement Template object,
            if key in main_stems:                   # then iterate the row dict keys.
                try:                                # If given key be found among
                    setattr(sc, key, row[key])      # Statement Template elements,
                except KeyError:                    # then assign it as field of
                    pass                            # Statement Template object.
            elif key in xtra_stems:                 # If given key defined as "extra",
                sc.extras[key] = row[key]           # assign it to an "extras" dict.

        shapes[sh_id].st_list.append(sc)            # Append Template object to a list.

        sc.normalize(config_dict)                   # SC normalizes itself, and
        st_warnings = sc.get_warnings()             # emits warnings on request.

        for (elem, warn) in st_warnings.items():    # Iterate SC instance warnings.
            try:                                    # Try to add each warning to dict
                warnings[sh_id][elem].append(warn)  # of all warnings by shape,
            except KeyError:                        # but if needed key not found,
                warnings[sh_id][elem] = []          # set value of empty list,
                warnings[sh_id][elem].append(warn)  # and add the warning.

        warnings_dict = dict(warnings)              # Result: dictionary of warnings.

        tapshapes_dict = {}                         # In dict above: TAPShape objects.
        shape_list = []                             # In this new dict: dict objects,
        tapshapes_dict["shapes"] = shape_list       # held in a list of shapes.

        for tapshape_obj in list(shapes.values()):  # Each shape-as-TAPShape-object
            tapshape_dict = asdict(tapshape_obj)    # is converted to plain dictionary,
            tapshape_dict[                          # and added to list of
                "statement_templates"               # statement_templates,
            ] = tapshape_dict.pop("st_list")        # and appended to growing list
            shape_list.append(tapshape_dict)        # of shapes-as-dictionaries.

        tapshapes_dict = _simplify(tapshapes_dict)  # Purge items with falsy values.

    return (tapshapes_dict, warnings_dict)
    # fmt: on


def _set_shape_fields(
    tapshape_obj=None,
    row_dict=None,
    main_shape_elements=None,
    xtra_shape_elements=None,
):
    """Populates shape fields of dataclass TAPShape object from dict for one row.

    Args:
        tapshape_obj: Unpopulated instance of dctap.tapclasses.TAPShape:
            TAPShape(shapeID='', shapeLabel='', st_list=[], sh_warnings={}, extras={})
        row_dict: Dictionary of all columns headers (keys) and cell values (values)
            found in a given row, with no distinction between shape elements and
            statement template elements.
        main_shape_elements: Default TAPClass fields related to shapes.
        xtra_shape_elements: Extra TAPClass fields as per optional config file.

    Returns:
        TAPShape object with shape fields set.
    """
    for key in row_dict:
        if key in main_shape_elements:
            try:
                setattr(tapshape_obj, key, row_dict[key])
            except KeyError:
                pass
        elif key in xtra_shape_elements:
            try:
                tapshape_obj.extras[key] = row_dict[key]
            except KeyError:
                pass
    return tapshape_obj


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


def _simplify(shapes_dict):
    """Iteratively remove elements from shapes dictionary with falsy values."""
    for shape in shapes_dict["shapes"]:
        for sc in shape["statement_templates"]:
            if sc.get("extras"):
                for (k, v) in sc["extras"].items():
                    sc[k] = v
                    del sc["extras"]
            if sc.get("st_warnings"):
                del sc["st_warnings"]
            for empty_element in [key for key in sc if not sc[key]]:
                del sc[empty_element]
        if shape.get("extras"):
            for (k, v) in shape["extras"].items():
                shape[k] = v
                del shape["extras"]
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
