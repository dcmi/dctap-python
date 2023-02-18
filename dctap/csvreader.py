"""Read CSV, return tuple: (CSV rows, warnings)."""

import re
from collections import defaultdict
from csv import DictReader
from dctap.exceptions import DctapError, NoDataError
from dctap.utils import coerce_concise


def csvreader(config_dict, csvfile_str=None, open_csvfile_obj=None):
    """Get list of CSV row dicts and related warnings."""
    if csvfile_str and open_csvfile_obj:
        raise DctapError("Cannot call with both csvfile_str and open_csvfile_obj.")

    if open_csvfile_obj:
        csvfile_str = open_csvfile_obj.read()

    if not csvfile_str:
        raise NoDataError("No data provided.")

    csvlines = [
        line.strip()
        for line in csvfile_str.splitlines()
        if not re.match("#", line.strip())
    ]
    (csvlines[0], warnings) = _normalize_header_line(csvlines[0], config_dict)

    csv_warnings = defaultdict(dict)
    csv_warnings["csv"] = {}
    csv_warnings["csv"]["header"] = []
    csv_warnings["csv"]["header"].extend(warnings)

    csv_rows = list(DictReader(csvlines))
    for row in csv_rows:
        for key, value in row.items():
            if isinstance(value, str):  # ignore if instance of, say, NoneType or list
                row[key] = value.strip()

    return (csv_rows, dict(csv_warnings))


def _list_recognized_elements(config_dict):
    """Return list of recognized elements, normalized to lowercase."""
    recognized_elements = config_dict.get("csv_elements")

    xtra_shems = config_dict.get("extra_shape_elements")
    if xtra_shems:
        recognized_elements.extend(xtra_shems)
        for element in xtra_shems:
            config_dict["element_aliases"][element.lower()] = element

    xtra_stems = config_dict.get("extra_statement_template_elements")
    if xtra_stems:
        recognized_elements.extend(xtra_stems)
        for element in xtra_stems:
            config_dict["element_aliases"][element.lower()] = element

    return [elem.lower() for elem in recognized_elements]


def _normalize_header_line(raw_header_line, config_dict):
    """Given header line, return list of normalized headers with list of warnings."""
    recognized_elements = _list_recognized_elements(config_dict)
    raw_header_line_list = [i.strip() for i in raw_header_line.split(",")]
    new_header_line_list = []
    warnings = []

    for header in raw_header_line_list:
        header = coerce_concise(header)
        header = _normalize_header_name(header, config_dict.get("element_aliases"))
        new_header_line_list.append(header)
        if header.lower() not in recognized_elements:
            warning = f"Non-DCTAP element '{header}' not configured as extra element."
            warnings.append(warning)

    if "propertyID" not in new_header_line_list:
        raise DctapError("Valid DCTAP CSV must have a 'propertyID' column.")

    new_header_line = ",".join(new_header_line_list) + "\n"
    return (new_header_line, warnings)


def _normalize_header_name(some_str, element_aliases_dict=None):
    """Given header string, return converted if aliased, else return unchanged."""
    some_str = coerce_concise(some_str)
    if element_aliases_dict:
        for key in element_aliases_dict.keys():
            if key == some_str:
                some_str = element_aliases_dict[key]
    return some_str
