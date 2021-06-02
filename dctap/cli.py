"""DC Tabular Application Profiles (DCTAP) - base module"""

from dataclasses import asdict
import click
from .inspect import pprint_csvshapes
from .csvreader import csvreader
from .csvshape import CSVShape, CSVStatementConstraint

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
@click.help_option(help="Show help and exit")
@click.pass_context
def inspect(context, csvfile_name, expand_prefixes, verbose):
    """Inspect CSV file contents, normalized, maybe with expanded prefixes."""
    csvshapes_list = csvreader(csvfile_name)
    pprint_output = pprint_csvshapes(csvshapes_list)
    for line in pprint_output:
        print(line)


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def model(context):
    """Show DCTAP model built-ins for ready reference"""

    shape_elements = list(asdict(CSVShape()))
    shape_elements.remove('sc_list')
    tconstraint_elements = list(asdict(CSVStatementConstraint()))
    print("DC Tabular Application Profile")
    print("    Shape elements:")
    for element in shape_elements:
        print(f"        {element}")
    print("        Statement Constraint elements:")
    for element in tconstraint_elements:
        print(f"            {element}")
