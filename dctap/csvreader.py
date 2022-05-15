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

    (main_stems, xtra_stems) = get_stems(
        statement_template_class=TAPStatementTemplate, settings=config_dict
    )

    # fmt: off
    shapes = {}                             # New dict for shapeID-to-TAPShape_list.
    warns = defaultdict(dict)               # New dict for shapeID-to-warnings_list.
    first_valid_row_encountered = True      # Only one row is ever "first valid".

    for row in rows:                                # For each row:
        if row.get("shapeID"):                      # If shapeID be truthy and
            sh_id = row.get("shapeID")          #   use its value for shapeID.
            if sh_id not in list(shapes):           # If shapeID not yet in shapes dict,
                sh_obj = _make_shapeobj(row, config_dict) # init shape from row elements.
                sh_obj.normalize(config_dict)       #   normalize a few values, and add
                shapes[sh_id] = sh_obj              #   that shape to all-shapes dict,
                warns[sh_id] = {}                   #   init shape object warnings.
        elif not row.get("propertyID"):             # But if propertyID be not truthy,
            continue                                #   skip this row and move to next.

            sh_warns = sh_obj.get_warnings()        # Get warnings for shape object.
            for (elem, warn) in sh_warns.items():   # For each warning, by element,
                try:                                #   append to warnings list
                    warns[sh_id][elem].append(warn) #   the value for key "shapeID".
                except KeyError:                    # If element key does not yet exist,
                    warns[sh_id][elem] = []         #   initialize with empty list,
                    warns[sh_id][elem].append(warn) #   only then do add the warning.

        if row.get("propertyID"):                   # If propertyID be truthy
            try:                                    # then
                sh_id = list(shapes)[-1]            # use most recent listed shapeID.
            except IndexError:                      # But if shapeID not be listed,
                sh_id = row["shapeID"] = dshape     # use default shapeID.

            if sh_id not in list(shapes):           # If shapeID not yet in shapes dict,
                sh_obj = _make_shapeobj(row, config_dict) # init shape from row elements.
                sh_obj.normalize(config_dict)       #   normalize a few values, and add
                shapes[sh_id] = sh_obj              #   that shape to all-shapes dict,
                warns[sh_id] = {}                   #   init shape object warnings.

            st = TAPStatementTemplate()             # Make new ST object for the row.
            for col in row:                         # For each column in row dict,
                if col in main_stems:               # If column be ST element
                    setattr(st, col, row[col])      # assign key-value to ST object.
                elif col in xtra_stems:             # But if column defined as "extra",
                    st.extras[col] = row[col]       # add to "extras" dict on ST object.

            st.normalize(config_dict)               # Normalize some ST values, and
            shapes[sh_id].st_list.append(st)        # Add ST object to ST list.
            st_warns = st.get_warnings()            # Get warnings for ST warnings dict.

            for (elem, warn) in st_warns.items():   # For item in ST warnings dict
                try:                                # Transfer each warning to dict
                    warns[sh_id][elem].append(warn) # of all warnings (by shape),
                except KeyError:                    # but if element not already key,
                    warns[sh_id][elem] = []         # initialize that element as key,
                    warns[sh_id][elem].append(warn) # and add the warning.

            warns_dict = dict(warns)                # Make defaultdict of warns to dict,
            shapes_dict = {}                        # an empty dict for shape objs.
            list_of_shapes = []                     # Make list to hold a list of shapes,
            shapes_dict["shapes"] = list_of_shapes  # make key on dict to hold that list.

            for sh_obj in list(shapes.values()):    # Each shape-as-TAPShape-object
                sh_dict = asdict(sh_obj)            # be converted to plain dict,
                sh_dict[                            # and added to a list of
                    "statement_templates"           # statement_templates,
                ] = sh_dict.pop("st_list")          # and appended to growing list
                list_of_shapes.append(sh_dict)      # of shapes-as-dictionaries.

            shapes_dict = _simplify(shapes_dict)    # Purge anything of falsy value.

    return (shapes_dict, warns_dict)
    # fmt: on


def _make_shapeobj(row_dict=None, config_dict=None):
    """Populates shape fields of dataclass TAPShape object from dict for one row.

    Args:
        row_dict: Dictionary of all columns headers (keys) and cell values (values)
            found in a given row, with no distinction between shape elements and
            statement template elements.
        main_shape_elements: Default TAPShapefields related to shapes.
        xtra_shape_elements: Extra TAPShape fields as per optional config file.

    Returns:
        Unpopulated instance of dctap.tapclasses.TAPShape, by default:
        - TAPShape(shapeID='', shapeLabel='', st_list=[], sh_warnings={}, extras={})
        - Plus extra TAPShape fields as per config settings.
    """
    (main_shems, xtra_shems) = get_shems(shape_class=TAPShape, settings=config_dict)
    tapshape_obj = TAPShape()
    for key in row_dict:
        if key in main_shems:
            setattr(tapshape_obj, key, row_dict[key])
        elif key in xtra_shems:
            tapshape_obj.extras[key] = row_dict[key]
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
    """Remove elements from shapes dictionary with falsy values."""
    for shape in shapes_dict["shapes"]:
        for st in shape["statement_templates"]:
            if st.get("extras"):
                for (k, v) in st["extras"].items():
                    st[k] = v
                    del st["extras"]
            if st.get("st_warnings"):
                del st["st_warnings"]
            for empty_element in [key for key in st if not st[key]]:
                del st[empty_element]
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


#            if first_valid_row_encountered:         # If row IS "first valid" found,
#                if row.get("shapeID"):              #   and shapeID be truthy,
#                    sh_id = row.get("shapeID")      #   use its value for shapeID.
#                else:                               # Else shapeID be not truthy,
#                    sh_id = row["shapeID"] = dshape #   use default shapeID.
#                first_valid_row_encountered = False # May future rows be not "first".
#            elif not first_valid_row_encountered:   # But if row be NOT "first valid",
#                if row.get("shapeID"):              #   and shapeID be truthy,
#                    sh_id = row["shapeID"]          #   use its value for shapeID.
#                else:                               # Else shapeID be not truthy, then
#                    so_far = list(shapes)           #   then from shapeIDs used so far,
#                    sh_id = list(shapes)[-1]        #   use the most recent.
