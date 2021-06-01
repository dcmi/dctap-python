"""Pretty-print CSV contents to screen."""

from dataclasses import asdict
from .csvshape import CSVShape, CSVTripleConstraint


def pprint_csvshapes(csvshapes_list, verbose=False):
    """Pretty-print CSVShape objects to console."""
    shape_elements = list(asdict(CSVShape()))
    shape_elements.remove('tc_list')
    tconstraint_elements = list(asdict(CSVTripleConstraint()))

    pprint_output = []
    pprint_output.append("DC Tabular Application Profile")
    for csvshape_obj in csvshapes_list:
        csvshape_dict = asdict(csvshape_obj)
        pprint_output.append("    Shape")
        for key in shape_elements:
            if not verbose and csvshape_dict[key]:
                pprint_output.append(8 * " " + key + ": " + str(csvshape_dict[key]))
            if verbose:
                pprint_output.append(8 * " " + key + ": " + str(csvshape_dict[key]))

        for tc_dict in csvshape_dict.get("tc_list"):
            pprint_output.append("        Statement Constraint")
            for key in tconstraint_elements:
                if not verbose and tc_dict[key]:
                    pprint_output.append(12 * " " + str(key) + ": " + str(tc_dict[key]))
                if verbose:
                    pprint_output.append(12 * " " + str(key) + ": " + str(tc_dict[key]))

    return pprint_output
