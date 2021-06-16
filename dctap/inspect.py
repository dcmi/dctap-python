"""Pretty-print CSV contents to screen."""

from dataclasses import asdict
from .tapclasses import TAPShape, TAPStatementConstraint


def pprint_tapshapes(tapshapes_list, verbose=False):
    """Pretty-print TAPShape objects to output list, ready for printing to console."""
    shape_elements = list(asdict(TAPShape()))
    shape_elements.remove('sc_list')
    # 2021-06-09 Removing 'start' for now, not yet part of official DCTAP spec.
    shape_elements.remove('start')
    tconstraint_elements = list(asdict(TAPStatementConstraint()))

    pprint_output = []
    pprint_output.append("DCTAP instance")
    for tapshape_obj in tapshapes_list:
        tapshape_dict = asdict(tapshape_obj)
        pprint_output.append("    Shape")
        for key in shape_elements:
            indent08 = (8 * " " + key + ": ")
            while len(indent08) < 33:
                indent08 = indent08 + " "
            if not verbose and tapshape_dict[key]:
                pprint_output.append(indent08 + str(tapshape_dict[key]))
            if verbose:
                pprint_output.append(indent08 + str(tapshape_dict[key]))

        for tc_dict in tapshape_dict.get("sc_list"):
            pprint_output.append("        Statement Constraint")
            for key in tconstraint_elements:
                indent12 = (12 * " " + key + ": ")
                while len(indent12) < 33:
                    indent12 = indent12 + " "
                if not verbose and tc_dict[key]:
                    pprint_output.append(indent12 + str(tc_dict[key]))
                if verbose:
                    pprint_output.append(indent12 + str(tc_dict[key]))

    return pprint_output


def tapshapes_to_dicts(tapshapes_list, verbose=False):
    """Converting TAPShape objects to dictionaries, ready for generating JSON and YAML."""
    dict_output = {}
    shape_list = []
    dict_output['shapes'] = shape_list
    for tapshape_obj in tapshapes_list:
        tapshape_dict = asdict(tapshape_obj)
        # Removing 'start' for now, not yet part of official DCTAP spec.
        tapshape_dict.pop('start')
        tapshape_dict['statement_constraints'] = tapshape_dict.pop('sc_list')
        shape_list.append(tapshape_dict)

    return dict_output

