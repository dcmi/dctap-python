"""Pretty-print CSV contents to screen."""

from dataclasses import asdict
from .tapclasses import TAPShape, TAPStatementConstraint


def pprint_tapshapes(tapshapes_dict):
    """Pretty-print TAPShape objects to output list, ready for printing to console."""

    shape_elements = list(asdict(TAPShape()))
    shape_elements.remove("sc_list")
    shape_elements.remove("sh_warnings")
    tconstraint_elements = list(asdict(TAPStatementConstraint()))
    tconstraint_elements.remove("sc_warnings")

    pprint_output = []
    pprint_output.append("DCTAP instance")
    for tapshape_dict in tapshapes_dict["shapes"]:
        pprint_output.append("    Shape")
        for key in shape_elements:
            indent08 = 8 * " " + key + ": "
            while len(indent08) < 33:
                indent08 = indent08 + " "
            if tapshape_dict[key]:
                pprint_output.append(indent08 + str(tapshape_dict[key]))

        for sc_dict in tapshape_dict.get("statement_constraints"):
            pprint_output.append("        Statement Constraint")
            for key in tconstraint_elements:
                indent12 = 12 * " " + key + ": "
                while len(indent12) < 33:
                    indent12 = indent12 + " "
                # pylint: disable=singleton-comparison
                if sc_dict[key] == True:
                    sc_dict[key] = "True"
                if sc_dict[key] == False:
                    sc_dict[key] = "False"
                if sc_dict[key]:
                    pprint_output.append(indent12 + str(sc_dict[key]))

    return pprint_output
