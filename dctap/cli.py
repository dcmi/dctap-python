"""DC Tabular Application Profiles (DCTAP) - base module"""

import json
from dataclasses import asdict
import click
from .inspect import pprint_tapshapes, tapshapes_to_dicts
from .csvreader import csvreader
from .classes import TAPShape, TAPStatementConstraint

# pylint: disable=unused-argument,no-value-for-parameter
# => unused-argument: Allows placeholders for now.
# => no-value-for-parameter: Okay in cli.py


@click.group()
@click.version_option("0.2.1", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(context):
    """DC Tabular Application Profiles (DCTAP) - base module"""


@cli.command()
@click.argument("csvfile_name", type=click.Path(exists=True))
@click.option("--expand-prefixes", is_flag=True)
@click.option("--verbose", is_flag=True)
@click.option("--json", is_flag=True)
@click.help_option(help="Show help and exit")
@click.pass_context
def inspect(context, csvfile_name, expand_prefixes, verbose, json):
    """Inspect CSV file contents, normalized, maybe with expanded prefixes."""
    tapshapes_list = csvreader(csvfile_name)
    if not json:
        pprint_output = pprint_tapshapes(tapshapes_list)
        for line in pprint_output:
            print(line)
#     if json:
#         """Nishad's output here."""
#         json.dumps(tapshapes_to_dicts(tapshapes_list), indent=4)


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def model(context):
    """Show DCTAP model built-ins for ready reference"""

    shape_elements = list(asdict(TAPShape()))
    shape_elements.remove('sc_list')
    shape_elements.remove('start')
    tconstraint_elements = list(asdict(TAPStatementConstraint()))
    print("DCTAP instance")
    print("    Shape")
    for element in shape_elements:
        print(f"        {element}")
    print("        Statement Constraints")
    for element in tconstraint_elements:
        print(f"            {element}")
