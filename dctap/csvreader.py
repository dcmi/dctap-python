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
    (csvrows, csvwarns) = _get_rows(open_csvfile_obj, config_dict)
    (tapshapes, tapwarns) = _get_tapshapes(csvrows, config_dict)
    tapwarns = {**csvwarns, **tapwarns}
    return (tapshapes, tapwarns)


def _get_tapshapes(rows, config_dict):
    """Return tuple: (shapes dict, warnings dict)."""
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
    shapes = {}                             # New dict for shapeID-to-TAPShapes.
    warns = defaultdict(dict)               # New dict for shapeID-to-warnings.
    first_valid_row_encountered = True      # Only one row can be "first valid".

    for row in rows:                        # For each row:
        if row.get("shapeID"):                  # If shapeID be truthy and
            if first_valid_row_encountered:         # If row IS "first valid" found,
                if row.get("shapeID"):              #   and shapeID be truthy,
                    sh_id = row.get("shapeID")      #   use its value for shapeID.
                else:                               # Else shapeID be not truthy,
                    sh_id = row["shapeID"] = dshape #   use default shapeID.
                first_valid_row_encountered = False # May future rows be not "first".
            elif not first_valid_row_encountered:   # But if row be NOT "first valid",
                if row.get("shapeID"):              #   and shapeID be truthy,
                    sh_id = row["shapeID"]          #   use its value for shapeID.
                else:                               # Else shapeID be not truthy, then
                    so_far = list(shapes)           #   then from shapeIDs used so far,
                    sh_id = so_far[-1]              #   use the most recent.

            if sh_id not in shapes:                 # If shapeID not yet in shapes dict,
                shape = shapes[sh_id] = TAPShape()  #   make new TAPShape object,
                shape = _set_shape_fields(          #   and add it to shapes dict, so:
                    tapshape_obj=shape,             #   - key: shapeID
                    row_dict=row,                   #   - value: TAPShape object
                    main_shape_elements=main_shems,
                    xtra_shape_elements=xtra_shems, # Then add to warnings dict:
                    )                               # - key: shapeID
                warns[sh_id] = {}                   # - value: empty dict

            shape.normalize(config_dict)            # Normalize some shape values.
            sh_warns = shape.get_warnings()         # Populate the shape warnings dict.

            for (elem, warn) in sh_warns.items():   # Iterate Shape warnings.
                try:                                # Try to add each warning to dict
                    warns[sh_id][elem].append(warn) # of all warnings, by shape,
                except KeyError:                    # but if needed key not found,
                    warns[sh_id][elem] = []         # set value of empty list,
                    warns[sh_id][elem].append(warn) # and add the warning.

        st = TAPStatementTemplate()             # Make new ST object for the row.
        for col in row:                         # For each column in row dict,
            if col in main_stems:               # If column be ST element
                setattr(st, col, row[col])      # assign key-value to ST object.
            elif col in xtra_stems:             # But if column defined as "extra",
                st.extras[col] = row[col]       # add to "extras" dict on ST object.

        shapes[sh_id].st_list.append(st)        # Append Template object to a list.

        st.normalize(config_dict)               # Normalize some ST values, and
        st_warns = st.get_warnings()            # populate the ST warnings dict.

        for (elem, warn) in st_warns.items():   # For item in ST warnings dict
            try:                                # Try to add each warning to dict
                warns[sh_id][elem].append(warn) # of all warnings by shape,
            except KeyError:                    # but if needed key not found,
                warns[sh_id][elem] = []         # set value of empty list,
                warns[sh_id][elem].append(warn) # and add the warning.

        warns_dict = dict(warns)                # Result: dictionary of warnings.

        shapes_dict = {}                        # In dict above: TAPShape objects.
        list_of_shapes = []                     # In this new dict: dict objects,
        shapes_dict["shapes"] = list_of_shapes  # held in a list of shapes.

        for sh_obj in list(shapes.values()):    # Each shape-as-TAPShape-object
            sh_dict = asdict(sh_obj)            # is converted to plain dictionary,
            sh_dict[                            # and added to list of
                "statement_templates"           # statement_templates,
            ] = sh_dict.pop("st_list")          # and appended to growing list
            list_of_shapes.append(sh_dict)      # of shapes-as-dictionaries.

        shapes_dict = _simplify(shapes_dict)    # Purge items with falsy values.

    return (shapes_dict, warns_dict)
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
        for st in shape["statement_templates"]:
            if st.get("extras"):
                for (k, v) in st["extras"].items():
                    st[k] = v
                    del st["extras"]
            if st.get("st_warns"):
                del st["st_warns"]
            for empty_element in [key for key in st if not st[key]]:
                del st[empty_element]
        if shape.get("extras"):
            for (k, v) in shape["extras"].items():
                shape[k] = v
                del shape["extras"]
        if shape.get("sh_warns"):
            del shape["sh_warns"]
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
    csv_warns = defaultdict(dict)

    for header in new_header_line_list:
        if header.lower() not in recognized_elements:
            warn = f"Non-DCTAP element {repr(header)} not configured as extra element."
            csv_warns["csv"] = {}
            csv_warns["csv"]["header"] = []
            csv_warns["csv"]["header"].append(warn)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    csv_rows = list(DictReader(tmp_buffer2))
    csv_warns = dict(csv_warns)
    return (csv_rows, csv_warns)
