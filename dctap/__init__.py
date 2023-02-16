"""Convert a Tabular Application Profile from CSV into JSON."""

from dctap.tapclasses import TAPShape, TAPStatementTemplate
from dctap.csvreader import csvreader

__version__ = "0.4.5"

# Keep version number in sync with:
# - https://github.com/dcmi/dctap-python/blob/main/docs/conf.py#L28
#   ../docs/conf.py
# - https://github.com/dcmi/dctap-python/blob/main/dctap/cli.py#L20
#   ../dctap/cli.py
