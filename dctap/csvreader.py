"""Read CSV, return tuple: (CSV rows, warnings)."""

import re
from collections import defaultdict
from csv import DictReader
from io import StringIO as StringBuffer
from dataclasses import asdict
from dctap.exceptions import DctapError, NoDataError
from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.utils import coerce_concise


def csvreader(
    csvfile_str=None,
    config_dict=None,
    open_csvfile_obj=None,
    shape_class=TAPShape,
    state_class=TAPStatementTemplate,
):
    """Get list of CSV row dicts and related warnings."""
    if open_csvfile_obj:
        csvfile_contents_str = open_csvfile_obj.read()
    elif csvfile_str:
        csvfile_contents_str = csvfile_str
    else:
        raise NoDataError("No data to process.")

    tmp_buffer = StringBuffer(csvfile_contents_str)
    csvlines_stripped = [line.strip() for line in tmp_buffer]
    csvlines_stripped = [
        line for line in csvlines_stripped if not re.match("#", line.strip())
    ]
    if len(csvlines_stripped) < 2:
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
    if not csvlines_stripped[0]:
        raise NoDataError("No data to process.")
    if "propertyID" not in csvlines_stripped[0]:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")

    tmp_buffer2 = StringBuffer("".join([line + "\n" for line in csvlines_stripped]))
    csv_rows = list(DictReader(tmp_buffer2))
    for row in csv_rows:
        for key, value in row.items():
            if isinstance(value, str):  # ignore if instance of NoneType or list
                row[key] = value.strip()
    csv_warns = dict(csv_warns)

    return (csv_rows, csv_warns)


def _normalize_element_name(some_str, element_aliases_dict=None):
    """Given header string, return converted if aliased, else return unchanged."""
    some_str = coerce_concise(some_str)
    if element_aliases_dict:
        for key in element_aliases_dict.keys():
            if key == some_str:
                some_str = element_aliases_dict[key]
    return some_str
