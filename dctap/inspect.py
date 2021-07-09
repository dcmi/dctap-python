"""Pretty-print CSV contents to screen."""

from dataclasses import asdict
from .config import _shape_elements, _statement_constraint_elements
from .tapclasses import TAPShape, TAPStatementConstraint


def pprint_tapshapes(tapshapes_dict, config_dict):
    """Pretty-print TAPShape objects to output list, ready for printing to console."""

    shape_elements = _shape_elements(TAPShape, config_dict)
    tconstraint_elements = _statement_constraint_elements(
        TAPStatementConstraint, config_dict
    )

    pprint_output = []
    pprint_output.append("DCTAP instance")
    for tapshape_dict in tapshapes_dict.get("shapes"):
        pprint_output.append("    Shape")
        for key in shape_elements:
            indent08 = 8 * " " + key + ": "
            while len(indent08) < 33:
                indent08 += " "
            if tapshape_dict.get(key):
                pprint_output.append(indent08 + str(tapshape_dict.get(key)))

        for sc_dict in tapshape_dict.get("statement_constraints"):
            pprint_output.append("        Statement Constraint")
            for key in tconstraint_elements:
                if sc_dict.get(key):
                    indent12 = 12 * " " + key + ": "
                    while len(indent12) < 33:
                        indent12 += " "
                    pprint_output.append(indent12 + str(sc_dict.get(key)))

    return pprint_output
