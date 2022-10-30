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

    (main_stems, xtra_stems) = get_stems(TAPStatementTemplate, config_dict)

    # fmt: off
    shapes = {}                             # Dict for shapeID-to-TAPShape_list.
    warns = defaultdict(dict)               # Dict for shapeID-to-warnings_list.

    for row in rows:
        sh_id = ""
        if row.get("propertyID"):
            if row.get("shapeID"):
                sh_id = row.get("shapeID")
            elif not row.get("shapeID"):
                try:
                    sh_id = list(shapes)[-1]
                except IndexError:
                    sh_id = row["shapeID"] = dshape
        elif row.get("shapeID"):
            sh_id = row.get("shapeID")

        if sh_id:
            if sh_id not in list(shapes):
                sh_obj = _mkshape(row, config_dict)
                sh_obj.normalize(config_dict)
                shapes[sh_id] = sh_obj
                warns[sh_id] = {}

            sh_warns = sh_obj.get_warnings()
            for (elem, warn) in sh_warns.items():
                try:
                    warns[sh_id][elem].append(warn)
                except KeyError:
                    warns[sh_id][elem] = []
                    warns[sh_id][elem].append(warn)

        if not row.get("propertyID"):
            continue

        st = TAPStatementTemplate()
        for col in row:
            if col in main_stems:
                setattr(st, col, row[col])
            elif col in xtra_stems:
                st.state_extras[col] = row[col]

        st.normalize(config_dict)
        shapes[sh_id].state_list.append(st)
        st_warns = st.get_warnings()

        for (elem, warn) in st_warns.items():
            try:
                warns[sh_id][elem].append(warn)
            except KeyError:
                warns[sh_id][elem] = []
                warns[sh_id][elem].append(warn)

        warns_dict = dict(warns)
        shapes_dict = {}
        list_of_shapes = []
        shapes_dict["shapes"] = list_of_shapes

        for sh_obj in list(shapes.values()):
            sh_dict = asdict(sh_obj)
            sh_dict[
                "statement_templates"
            ] = sh_dict.pop("state_list")
            list_of_shapes.append(sh_dict)

        shapes_dict = _simplify(shapes_dict)

    return (shapes_dict, warns_dict)
    # fmt: on


def _mkshape(row_dict=None, config_dict=None):
    """Populates shape fields of dataclass TAPShape object from dict for one row.

    Args:
        row_dict: Dictionary of all columns headers (keys) and cell values (values)
            found in a given row, with no distinction between shape elements and
            statement template elements.
        config_dict: Dictionary of settings, built-in or as read from config file.

    Returns:
        Unpopulated instance of dctap.tapclasses.TAPShape, by default:
        - TAPShape(shapeID='', shapeLabel='', state_list=[], shape_warns={}, state_extras={})
        - Plus extra TAPShape fields as per config settings.
    """
    (main_shems, xtra_shems) = get_shems(shape_class=TAPShape, settings=config_dict)
    tapshape_obj = TAPShape()
    for key in row_dict:
        if key in main_shems:
            setattr(tapshape_obj, key, row_dict[key])
        elif key in xtra_shems:
            tapshape_obj.shape_extras[key] = row_dict[key]
    return tapshape_obj


def _lowercase_despace_depunctuate(some_str=None):
    """
    For given string:
    - delete spaces, underscores, dashes, commas
    - lowercase
    - delete surrounding single and double quotes
    """
    some_str = some_str.replace(" ", "")
    some_str = some_str.replace("_", "")
    some_str = some_str.replace("-", "")
    some_str = some_str.replace(",", "")
    some_str = some_str.lower()
    some_str = some_str.strip('"')
    some_str = some_str.strip("'")
    return some_str


def _normalize_element_name(some_str, element_aliases_dict=None):
    """Normalize a given element string, if recognized; if not, leave unchanged)."""
    some_str = _lowercase_despace_depunctuate(some_str)
    if element_aliases_dict:
        for key in element_aliases_dict.keys():
            if key == some_str:
                some_str = element_aliases_dict[key]
    return some_str


def _simplify(shapes_dict):
    """Remove elements from shapes dictionary with falsy values."""
    for shape in shapes_dict["shapes"]:
        for state in shape["statement_templates"]:
            if state.get("state_extras"):
                for (k, v) in state["state_extras"].items():
                    state[k] = v
                del state["state_extras"]
            if state.get("state_warns"):
                del state["state_warns"]
            for empty_element in [key for key in state if not state[key]]:
                del state[empty_element]
        if shape.get("shape_extras"):
            for (k, v) in shape["shape_extras"].items():
                shape[k] = v
            del shape["shape_extras"]
        if shape.get("shape_warns"):
            del shape["shape_warns"]
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

    for column in raw_header_line_list:
        column = _lowercase_despace_depunctuate(column)
        column = _normalize_element_name(column, config_dict.get("element_aliases"))
        new_header_line_list.append(column)
    csv_warns = defaultdict(dict)

    for column in new_header_line_list:
        if column.lower() not in recognized_elements:
            warn = f"Non-DCTAP element {repr(column)} not configured as extra element."
            csv_warns["csv"] = {}
            csv_warns["csv"]["column"] = []
            csv_warns["csv"]["column"].append(warn)
    new_header_line_str = ",".join(new_header_line_list)
    csvlines_stripped[0] = new_header_line_str
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")
    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    csv_rows = list(DictReader(tmp_buffer2))
    csv_warns = dict(csv_warns)
    return (csv_rows, csv_warns)
