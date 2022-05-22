"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from dataclasses import asdict
from ruamel.yaml import YAML
import click
from .config import get_config, write_configfile
from .defaults import DEFAULT_CONFIGFILE_NAME, DEFAULT_HIDDEN_CONFIGFILE_NAME
from .inspect import pprint_tapshapes, print_warnings
from .csvreader import csvreader
from .loggers import stderr_logger
from .tapclasses import TAPShape, TAPStatementTemplate
from .utils import expand_uri_prefixes

# pylint: disable=unused-argument,no-value-for-parameter
# => unused-argument: Allows placeholders for now.
# => no-value-for-parameter: Okay in cli.py


@click.group()
@click.version_option("0.3.4", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(context):
    """DC Tabular Application Profiles parser and base module

    Examples (see https://dctap-python.rtfd.io):

    \b
    Write an editable configuration file:
    $ dctap init                           # Write dctap.yaml
    $ dctap init --hidden                  # Write .dctaprc
    \b
    Parse a CSV and generate a normalized view:
    $ dctap read x.csv                     # Plain text output
    $ dctap read --json x.csv              # JSON output
    $ dctap read --yaml x.csv              # YAML output
    $ dctap read --expand-prefixes x.csv   # Expand prefixes
    $ dctap read --warnings x.csv          # Show warnings
    $ dctap read --config ../taprc x.csv   # Use custom configfile
    """


@cli.command()
@click.argument("csvfile_obj", type=click.File(mode="r", encoding="utf-8-sig"))
@click.option("--config",
    type=click.Path(exists=True),
    help="Path to alternative config file.",
)
@click.option("--expand-prefixes", is_flag=True, help="Expand compact to full IRIs.")
@click.option("--warnings", is_flag=True, help="Print warnings to stderr.")
@click.option("--json", is_flag=True, help="Print JSON to stdout.")
@click.option("--yaml", is_flag=True, help="Print YAML to stdout.")
@click.help_option(help="Show help and exit")
@click.pass_context
def read(context, csvfile_obj, config, expand_prefixes, warnings, json, yaml):
    """Read CSV and generate normalized text, JSON, or YAML, with warnings."""
    # pylint: disable=too-many-locals,too-many-arguments

    config_dict = get_config(configfile_name=config)
    (tapshapes_dict, warnings_dict) = csvreader(csvfile_obj, config_dict)
    if expand_prefixes:
        tapshapes_dict = expand_uri_prefixes(tapshapes_dict, config_dict)

    if json and yaml:
        # Quick fix for mutually exclusive options, a better fix in future.
        echo = stderr_logger()
        echo.warning("Please use either --json or --yaml")
        click.Context.exit(0)

    if json:
        json_output = j.dumps(tapshapes_dict, indent=4)
        print(json_output)
        if warnings:
            print_warnings(warnings_dict)

    if yaml:
        y = YAML()
        y.indent(mapping=2, sequence=4, offset=2)
        y.dump(tapshapes_dict, sys.stdout)
        if warnings:
            print_warnings(warnings_dict)

    if not (json or yaml):
        pprint_output = pprint_tapshapes(tapshapes_dict, config_dict)
        for line in pprint_output:
            print(line, file=sys.stdout)
        if warnings:
            print_warnings(warnings_dict)


@cli.command()
@click.option(
    "--hidden/--visible",
    default=False,
    help="Write config to hidden file [.dctaprc].",
)
@click.option(
    "--terse/--verbose",
    default=False,
    help="Omit verbose commentary from config file.",
)
@click.help_option(help="Show help and exit")
@click.pass_context
def init(context, hidden, terse):
    """Write customizable config file [default: dctap.yaml]."""
    if hidden:
        configfile = DEFAULT_HIDDEN_CONFIGFILE_NAME
    else:
        configfile = DEFAULT_CONFIGFILE_NAME
    write_configfile(configfile, terse=terse)


@cli.command()
@click.help_option(help="Show help and exit")
@click.pass_context
def model(context):
    """Show DCTAP model built-ins for ready reference"""

    shape_elements = list(asdict(TAPShape()))
    # shape_elements.remove('tc_list')
    state_elements = list(asdict(TAPStatementTemplate()))
    print("DC Tabular Application Profile")
    print("    Shape elements:")
    for element in shape_elements:
        print(f"        {element}")
    print("        Statement Template elements:")
    for element in state_elements:
        print(f"            {element}")
