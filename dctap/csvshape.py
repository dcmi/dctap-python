"""Class for Python objects derived from CSV files."""


from dataclasses import dataclass, field
from typing import List


@dataclass
class CSVStatementConstraint:
    """Instances hold TAP/CSV elements related to statement constraints."""

    # pylint: disable=too-many-instance-attributes
    # It's a dataclass, right?
    # pylint: disable=invalid-name
    # propertyID, etc, do not conform to snake-case naming style.

    propertyID: str = ""
    propertyLabel: str = ""
    mandatory: str = False
    repeatable: str = False
    valueNodeType: str = ""
    valueDataType: str = ""
    valueConstraint: str = ""
    valueConstraintType: str = ""
    valueShape: str = ""
    note: str = ""


@dataclass
class CSVShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    shapeClosed: str = ""
    start: bool = False
    sc_list: List[CSVStatementConstraint] = field(default_factory=list)


@dataclass
class CSVSchema:
    """List of CSVShape instances"""

    csvshapes_list: List[CSVShape] = field(default_factory=list)
