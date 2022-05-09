"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from ruamel.yaml import YAML
import click
from .config import get_config, write_configfile, DEFAULT_CONFIGFILE_NAME
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
    $ dctap init                         # Write default ./dctap.yml
    $ dctap init --configfile ../dctaprc # Write non-default pathname
    Parse CSV, generate normalized view and optional warnings:
    $ dctap generate xyz.csv
    $ dctap generate --json xyz.csv
    $ dctap generate --expand-prefixes xyz.csv
    $ dctap generate --warnings xyz.csv
    $ dctap generate --configfile ../dctaprc
    """


@cli.command()
@click.argument("csvfile_obj", type=click.File(mode="r", encoding="utf-8-sig"))
@click.option(
    "--configfile",
    type=click.Path(exists=True),
    help="Pathname of (non-default) config file."
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
def generate(context, csvfile_obj, configfile, expand_prefixes, warnings, json, yaml):
    """Generate normalized text, JSON, or YAML of CSV, with warnings."""
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
    "--configfile",
    type=click.Path(exists=False),
    help="Pathname of config file to be written."
)
@click.option(
    "--terse/--verbose",
    default=False,
    help="Write config file without (or with) verbose commentary."
)
@click.help_option(help="Show help and exit")
@click.pass_context
def init(context, configfile, terse):
    """Generate customizable configuration file [default: dctap.yml]."""
    if not configfile:
        configfile = DEFAULT_CONFIGFILE_NAME
    write_configfile(configfile, terse=terse)
