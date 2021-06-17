"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from ruamel.yaml import YAML
from dataclasses import asdict
import click
from .inspect import pprint_tapshapes, tapshapes_to_dicts
from .csvreader import csvreader
from .tapclasses import TAPShape, TAPStatementConstraint
from .loggers import stderr_logger, warning_logger, debug_logger

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
@click.option("--warnings", is_flag=True)
@click.option("--verbose", is_flag=True)
@click.option("--json", is_flag=True)
@click.option("--yaml", is_flag=True)
@click.help_option(help="Show help and exit")
@click.pass_context
def inspect(context, csvfile_name, expand_prefixes, warnings, verbose, json, yaml):
    """Output CSV contents to text, JSON, or YAML, with warnings"""
    csvreader_output = csvreader(csvfile_name)
    tapshapes_list = csvreader_output[0]
    warnings_dict = csvreader_output[1]

    if (json and yaml):
        # Quick fix for mutually exclusive options, a better fix in future. 
        echo = stderr_logger()
        echo.warning('Please use either --json or --yaml')
        click.Context.exit(0)

    if json:
        json_output = j.dumps(tapshapes_to_dicts(tapshapes_list), indent=4)
        print(json_output)

    if yaml:
        y = YAML()
        y.indent(mapping=2, sequence=4, offset=2)
        y.dump(tapshapes_to_dicts(tapshapes_list), sys.stdout)

    if not (json or yaml):
        pprint_output = pprint_tapshapes(tapshapes_list)
        for line in pprint_output:
            print(line, file=sys.stderr)
        if warnings:
            print("", file=sys.stderr)
            echo = stderr_logger()
            for (shapeid,warnings) in warnings_dict.items():
                for (elem,warn_list) in warnings.items():
                    for warning in warn_list:
                        echo.warning(f"Shape {shapeid} => {elem}: {warning}")




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
