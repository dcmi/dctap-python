"""DC Tabular Application Profiles (DCTAP) - base module"""

import sys
import json as j
from ruamel.yaml import YAML
import click
from .config import get_config, write_configfile
from .inspect import pprint_tapshapes
from .csvreader import csvreader
from .loggers import stderr_logger
from .utils import expand_uri_prefixes

# pylint: disable=unused-argument,no-value-for-parameter
# => unused-argument: Allows placeholders for now.
# => no-value-for-parameter: Okay in cli.py


@click.group()
@click.version_option("0.2.2", help="Show version and exit")
@click.help_option(help="Show help and exit")
@click.pass_context
def cli(context):
    """DC Tabular Application Profiles (DCTAP) - base module"""


@cli.command()
@click.argument("csvfile_name", type=click.File(mode="r", encoding="utf-8-sig"))
@click.option(
    "--configfile", type=click.Path(exists=True), help="Pathname of configuration file."
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
def generate(context, csvfile_name, configfile, expand_prefixes, warnings, json, yaml):
    """Given CSV, generate text, JSON, or YAML, with warnings."""
    # pylint: disable=too-many-locals,too-many-arguments

    config_dict = get_config(configfile)
    csvreader_output = csvreader(csvfile_name, config_dict)
    tapshapes_dict = csvreader_output[0]
    if expand_prefixes:
        tapshapes_dict = expand_uri_prefixes(tapshapes_dict, config_dict)
    warnings_dict = csvreader_output[1]

    if json and yaml:
        # Quick fix for mutually exclusive options, a better fix in future.
        echo = stderr_logger()
        echo.warning("Please use either --json or --yaml")
        click.Context.exit(0)

    if json:
        json_output = j.dumps(tapshapes_dict, indent=4)
        print(json_output)

    if yaml:
        y = YAML()
        y.indent(mapping=2, sequence=4, offset=2)
        y.dump(tapshapes_dict, sys.stdout)

    # pylint: disable=logging-fstring-interpolation
    if not (json or yaml):
        pprint_output = pprint_tapshapes(tapshapes_dict)
        for line in pprint_output:
            print(line, file=sys.stdout)
        if warnings:
            print("", file=sys.stderr)
            echo = stderr_logger()
            for (shapeid, warns) in warnings_dict.items():
                for (elem, warn_list) in warns.items():
                    for warning in warn_list:
                        echo.warning(f"[{shapeid}/{elem}] {warning}")

@cli.command()
@click.argument("configfile", type=click.Path(), required=False)
@click.help_option(help="Show help and exit")
@click.pass_context
def init(context, configfile):
    """Write out starter config file [default: dctap.yml]"""
    write_configfile(configfile)
