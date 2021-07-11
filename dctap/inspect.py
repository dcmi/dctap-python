"""Pretty-print CSV contents to screen."""

from .config import shape_elements, statement_constraint_elements
from .tapclasses import TAPShape, TAPStatementConstraint


def pprint_tapshapes(tapshapes_dict, config_dict):
    """Pretty-print TAPShape objects to output list, ready for printing to console."""
    # pylint: disable=too-many-branches

    only_shape_elements, xtra_shape_elements = shape_elements(TAPShape, config_dict)
    only_sc_elements, xtra_sc_elements = statement_constraint_elements(
        TAPStatementConstraint, config_dict
    )
    print(f"Extra shape elements: {xtra_shape_elements}")
    print(f"Extra sc elements: {xtra_sc_elements}")
    print(f"Tapshapes_dict: {tapshapes_dict}")

    pprint_output = []
    pprint_output.append("DCTAP instance")
    for tapshape_dict in tapshapes_dict.get("shapes"):
        pprint_output.append("    Shape")
        for key in only_shape_elements:
            indent08 = 8 * " " + key + ": "
            while len(indent08) < 33:
                indent08 += " "
            if tapshape_dict.get(key):
                pprint_output.append(indent08 + str(tapshape_dict.get(key)))
        for key in xtra_shape_elements:
            indent08 = 8 * " " + "[" + key + "]: "
            while len(indent08) < 33:
                indent08 += " "
            if tapshape_dict.get(key):
                pprint_output.append(indent08 + str(tapshape_dict.get(key)))

        for sc_dict in tapshape_dict.get("statement_constraints"):
            pprint_output.append("        Statement Constraint")
            for key in only_sc_elements:
                if sc_dict.get(key):
                    indent12 = 12 * " " + key + ": "
                    while len(indent12) < 33:
                        indent12 += " "
                    pprint_output.append(indent12 + str(sc_dict.get(key)))
            for key in xtra_sc_elements:
                indent08 = 12 * " " + "[" + key + "]: "
                while len(indent08) < 33:
                    indent08 += " "
                if sc_dict.get(key):
                    pprint_output.append(indent08 + str(sc_dict.get(key)))

    return pprint_output
