"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from ruamel.yaml import YAML
import click
from .config import get_config, write_configfile
from .defaults import DEFAULT_CONFIGFILE_NAME, DEFAULT_HIDDEN_CONFIGFILE_NAME
from .inspect import pprint_tapshapes, print_warnings
from .csvreader import csvreader
from .loggers import stderr_logger
from .utils import expand_uri_prefixes

# pylint: disable=unused-argument,no-value-for-parameter
# => unused-argument: Allows placeholders for now.
# => no-value-for-parameter: Okay in cli.py


@click.group()
@click.version_option("0.3.3", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(context):
    """DC Tabular Application Profiles parser and base module

    Examples (see https://dctap-python.rtfd.io):

    \b
    Write editable configuration file:
    $ dctap init                             # Default dctap.yml
    $ dctap init --hidden-configfile         # Default .dctaprc
    $ dctap init --configfile ../taprc       # Custom path
    Parse CSV, generate normalized view, show warnings:
    $ dctap read x.csv                       # Show in plain text
    $ dctap read --json x.csv                # Show in JSON
    $ dctap read --yaml x.csv                # Show in YAML
    $ dctap read --expand-prefixes x.csv     # Expand prefixes
    $ dctap read --warnings x.csv            # Show warnings
    $ dctap read --configfile ../taprc x.csv # Use custom path
    """


@cli.command()
@click.argument("csvfile_obj", type=click.File(mode="r", encoding="utf-8-sig"))
@click.option(
    "--configfile",
    type=click.Path(exists=True),
    help="Pathname of (non-default) config file.",
)
@click.option(
    "--expand-prefixes",
    is_flag=True,
    help="Compact to full IRI with prefixes mapped to namespaces.",
)
@click.option("--warnings", is_flag=True, help="Print warnings to stderr.")
@click.option("--json", is_flag=True, help="Print JSON to stdout.")
@click.option("--yaml", is_flag=True, help="Print YAML to stdout.")
@click.help_option(help="Show help and exit")
@click.pass_context
def read(context, csvfile_obj, configfile, expand_prefixes, warnings, json, yaml):
    """Read CSV and generate normalized text, JSON, or YAML, with warnings."""
    # pylint: disable=too-many-locals,too-many-arguments

    config_dict = get_config(configfile)
    csvreader_output = csvreader(csvfile_obj, config_dict)
    (tapshapes_dict, warnings_dict) = csvreader_output
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
    "--hidden-configfile/--configfile",
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
def init(context, hidden_configfile, terse):
    """Write customizable config file [default: dctap.yml]."""
    if hidden_configfile:
        configfile = DEFAULT_HIDDEN_CONFIGFILE_NAME
    else:
        configfile = DEFAULT_CONFIGFILE_NAME
    write_configfile(configfile, terse=terse)
