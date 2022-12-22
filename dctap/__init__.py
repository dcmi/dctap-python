"""Normalize and debug a TAP (application profile in DCTAP format)."""

from .tapclasses import TAPShape, TAPStatementTemplate
from .csvreader import csvreader

__version__ = "0.3.13"

# Keep version number in sync with:
# - https://github.com/dcmi/dctap-python/blob/main/docs/conf.py#L28
#   ../docs/conf.py
# - https://github.com/dcmi/dctap-python/blob/main/dctap/cli.py#L20
#   ../dctap/cli.py
