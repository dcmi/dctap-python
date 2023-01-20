"""Parse TAP, return two-item tuple: (list of shape objects, list of warnings)."""

import re
from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from dataclasses import asdict
from dctap.exceptions import DctapError, NoDataError
from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.utils import coerce_concise


def csvreader(
    open_csvfile_obj=None,
    config_dict=None,
    shape_class=TAPShape,
    state_class=TAPStatementTemplate,
):
    """From open CSV file object, return shapes dict."""
    (csvrows, csvwarns) = _get_rows(open_csvfile_obj, config_dict)
    (tapshapes, tapwarns) = _get_tapshapes(
        rows=csvrows,
        config_dict=config_dict,
        shape_class=shape_class,
        state_class=state_class,
    )
    tapwarns = {**csvwarns, **tapwarns}
    prefixes_used = _get_prefixes_actually_used(csvrows)
    tapshapes = _add_namespaces(tapshapes, config_dict, prefixes_used)
    tapshapes = _add_tapwarns(tapshapes, tapwarns)
    return tapshapes


def _add_namespaces(tapshapes=None, config_dict=None, prefixes_used=None):
    """Adds key 'namespaces' to tapshapes dict."""
    tapshapes["namespaces"] = {}
    if config_dict.get("prefixes"):
        for prefix in prefixes_used:
            if config_dict["prefixes"].get(prefix):
                tapshapes["namespaces"][prefix] = config_dict["prefixes"].get(prefix)
    return tapshapes


def _add_tapwarns(tapshapes=None, tapwarns=None):
    """Adds key 'warnings' to tapshapes dict."""
    tapshapes["warnings"] = tapwarns
    return tapshapes


def _get_prefixes_actually_used(csvrows):
    """List strings before colon in values of elements that could take URI prefixes."""
    prefixes = set()
    for row in csvrows:
        for element in [
            "shapeID",
            "propertyID",
            "valueDataType",
            "shapeID",
            "valueShape",
        ]:
            if row.get(element):
                prefix_plus_uri_pair = re.match(r"(.*:)", row.get(element))
                if prefix_plus_uri_pair:  # there must be at least one
                    prefix_as_provided = prefix_plus_uri_pair.group(0)
                    prefixes.add(prefix_as_provided)
    return list(prefixes)


def _get_rows(open_csvfile_obj, config_dict):
    """Extract from _io.TextIOWrapper object a list of CSV file rows as dicts."""
    # pylint: disable=too-many-locals
    csvfile_contents_str = open_csvfile_obj.read()
    tmp_buffer = StringBuffer(csvfile_contents_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    if not csvlines_stripped:
        raise NoDataError("No data to process.")
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
        column = coerce_concise(column)
        column = _normalize_element_name(column, config_dict.get("element_aliases"))
        new_header_line_list.append(column)

    csv_warns = defaultdict(dict)
    for column in new_header_line_list:
        if column.lower() not in recognized_elements:
            warn = f"Non-DCTAP element '{column}' not configured as extra element."
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


def _get_tapshapes(rows=None, config_dict=None, shape_class=None, state_class=None):
    """Return tuple: (shapes dict, warnings dict)."""
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    default_shape_id = config_dict["default_shape_identifier"]
    main_stems = config_dict.get("statement_template_elements")
    xtra_stems = config_dict.get("extra_statement_template_elements")
    shapes = {}  # dict for shapeID-to-TAPShape_list
    warns = defaultdict(dict)  # dict for shapeID-to-warnings_list

    for row in rows:
        shape_id = ""
        if row.get("propertyID"):
            if row.get("shapeID"):
                shape_id = row.get("shapeID")
            elif not row.get("shapeID"):
                try:
                    shape_id = list(shapes)[-1]
                except IndexError:
                    shape_id = row["shapeID"] = default_shape_id
        elif row.get("shapeID"):
            shape_id = row.get("shapeID")

        if shape_id:
            if shape_id not in list(shapes):
                shape_obj = _make_shape(
                    row_dict=row,
                    config_dict=config_dict,
                    shape_class=shape_class,
                )
                shape_obj.normalize(config_dict)
                shapes[shape_id] = shape_obj
                warns[shape_id] = {}

            shape_warnings = shape_obj.get_warnings()
            for (elem, warn) in shape_warnings.items():
                try:
                    warns[shape_id][elem].append(warn)
                except KeyError:
                    warns[shape_id][elem] = []
                    warns[shape_id][elem].append(warn)

        if not row.get("propertyID"):
            continue

        state_class_obj = state_class()
        for col in row:
            if col in main_stems:
                setattr(state_class_obj, col, row[col])
            elif col in xtra_stems:
                state_class_obj.state_extras[col] = row[col]

        state_class_obj.normalize(config_dict)
        shapes[shape_id].state_list.append(state_class_obj)

        warns_dict = dict(warns)
        shapes_dict = {}
        shapes_dict["shapes"] = []

        for shape_obj in list(shapes.values()):
            sh_dict = asdict(shape_obj)
            sh_dict["statement_templates"] = sh_dict.pop("state_list")
            shapes_dict["shapes"].append(sh_dict)

        shapes_dict = _simplify(shapes_dict)

    return (shapes_dict, warns_dict)


def _make_shape(row_dict=None, config_dict=None, shape_class=None):
    """Populates shape fields of dataclass shape object from dict for one row.

    Args:
        row_dict: Dictionary of all columns headers (keys) and cell values (values)
            found in a given row, with no distinction between shape elements and
            statement template elements.
        config_dict: Dictionary of settings, built-in or as read from config file.

    Returns:
        Unpopulated instance of shape class, for example:
        TAPShape(shapeID='', state_list=[], shape_warns={}, state_extras={}, ...)
    """
    main_shems = config_dict.get("shape_elements")
    xtra_shems = config_dict.get("extra_shape_elements")
    tapshape_obj = shape_class()
    for key in row_dict:
        if key in main_shems:
            setattr(tapshape_obj, key, row_dict[key])
        elif key in xtra_shems:
            tapshape_obj.shape_extras[key] = row_dict[key]
    return tapshape_obj


def _normalize_element_name(some_str, element_aliases_dict=None):
    """Given header string, return converted if aliased, else return unchanged."""
    some_str = coerce_concise(some_str)
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
