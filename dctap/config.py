"""Default settings."""

import os
import sys
from pathlib import Path
import ruamel.yaml as yaml
from .exceptions import ConfigError
from .loggers import stderr_logger, warning_logger, debug_logger


DEFAULT_CONFIG_YAML = """\
default_shape_name: ":default"

configfile_name: ".dctaprc"

prefixes:
    ":": "http://example.org/"
    "dcterms:": "http://purl.org/dc/terms/"
"""

DEFAULT_CONFIGFILE_NAME = ".dctaprc"


def get_config(configfile=None):
    """Get config dict from file if found, else get built-in defaults."""
    if not configfile:
        file_to_try = DEFAULT_CONFIGFILE_NAME
    bad_form = f"{repr(file_to_try)} is badly formed: fix, re-generate, or delete."
    not_found = f"{repr(file_to_try)} not found or not readable."
    try:
        return yaml.safe_load(Path(file_to_try).read_text())
    except (FileNotFoundError, PermissionError):
        if configfile:  # if one was specified as an argument
            raise ConfigError(not_found)
        else:
            pass
    except (yaml.YAMLError, yaml.scanner.ScannerError):
        raise ConfigError(bad_form)
    return yaml.safe_load(DEFAULT_CONFIG_YAML)


def write_configfile(configfile=None):
    """Write initial config file, by default to CWD, or exit if already exists."""
    if not configfile:
        configfile = DEFAULT_CONFIGFILE_NAME
    if Path(configfile).exists():
        raise ConfigError(f"{repr(configfile)} already exists - will not overwrite.")
    try:
        with open(configfile, "w", encoding="utf-8") as outfile:
            outfile.write(DEFAULT_CONFIG_YAML)
            print(
                f"Built-in settings written to {str(configfile)} - edit as needed.",
                file=sys.stderr,
            )
    except FileNotFoundError:
        raise ConfigError(f"{repr(configfile)} is not writeable - try different name.")
