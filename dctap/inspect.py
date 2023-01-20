"""Print CSV contents and warnings."""

import sys
from dctap.loggers import stderr_logger


def pprint_tapshapes(tapshapes_dict=None, config_dict=None):
    """Pretty-print TAPShape objects to output list, ready for printing to console."""
    # pylint: disable=too-many-branches
    main_shems = config_dict.get("shape_elements")
    xtra_shems = config_dict.get("extra_shape_elements")
    main_stems = config_dict.get("statement_template_elements")
    xtra_stems = config_dict.get("extra_statement_template_elements")
    pprint_output = []
    pprint_output.append("Tabular Application Profile (TAP)")
    for tapshape_dict in tapshapes_dict.get("shapes"):
        pprint_output.append("    Shape")
        for key in main_shems:
            indent08 = 8 * " " + key + " "
            while len(indent08) < 33:
                indent08 += " "
            if tapshape_dict.get(key):
                pprint_output.append(indent08 + str(tapshape_dict.get(key)))
        for key in xtra_shems:
            indent08 = 8 * " " + "[" + key + "] "
            while len(indent08) < 33:
                indent08 += " "
            if tapshape_dict.get(key):
                pprint_output.append(indent08 + str(tapshape_dict.get(key)))

        for sc_dict in tapshape_dict.get("statement_templates"):
            pprint_output.append("        Statement Template")
            for key in main_stems:
                if sc_dict.get(key):
                    indent12 = 12 * " " + key + " "
                    while len(indent12) < 33:
                        indent12 += " "
                    pprint_output.append(indent12 + str(sc_dict.get(key)))
            for key in xtra_stems:
                indent08 = 12 * " " + "[" + key + "] "
                while len(indent08) < 33:
                    indent08 += " "
                if sc_dict.get(key):
                    pprint_output.append(indent08 + str(sc_dict.get(key)))

    return pprint_output


def print_warnings(warnings_dict):
    """Print warnings to stdout."""
    # pylint: disable=logging-fstring-interpolation
    print("", file=sys.stderr)
    echo = stderr_logger()
    for (shapeid, warns) in warnings_dict.items():
        for (elem, warn_list) in warns.items():
            for warning in warn_list:
                echo.warning(f"[{shapeid}/{elem}] {warning}")
