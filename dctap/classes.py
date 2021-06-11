"""Classes for Python objects derived from CSV files."""


from dataclasses import dataclass, field
from typing import List
from .utils import is_uri_or_prefixed_uri


@dataclass
class TAPStatementConstraint:
    """Instances hold TAP/CSV elements related to statement constraints."""

    # pylint: disable=too-many-instance-attributes
    # - It's a dataclass, right?
    # pylint: disable=invalid-name
    # - propertyID, etc, do not conform to snake-case naming style.

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

    from io import StringIO as StringBuffer
    cs_warnings = StringBuffer()

    def normalize(self, config_dict=None):
        """Verifies and normalizes values of fields."""
        self._normalize_valueNodeType(config_dict)
        self._warn_about_literal_datatype_used_with_uri()
        return True

    def _normalize_value_node_type(self, config_dict=None):
        """Take valueNodeType from configurable enumerated list, case-insensitive."""
        valid_types = config_dict['value_node_types']
        if self.valueNodeType:
            if self.valueNodeType.lower not in [v.lower for v in valid_types]:
                print(f"Warning: {self.valueNodeType} is not a recognized node type.")
                self.valueNodeType = ""
        return self

    def _warn_about_literal_datatype_used_with_uri(self):
        """URIs should usually not have a datatype of Literal."""
        if self.valueDataType == "Literal":
            if is_uri_or_prefixed_uri(self.valueConstraint):
                cs_warnings.write(
                    f"{self.valueConstraint} looks like URI "
                    "but typed as {repr(self.valueDataType)}"
                )

    def get_warnings(self):
        """Dump contents of warnings buffer as list and close buffer."""
        warnings_list = cs_warnings.getvalue().splitlines()
        cs_warnings.close()
        return warnings_list


@dataclass
class TAPShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    start: bool = False
    sc_list: List[TAPStatementConstraint] = field(default_factory=list)

    def normalize(self, config_dict=None):
        """Normalize values where required."""
        self._normalize_default_shapeID(config_dict)
        return True

    def _normalize_default_shapeID(self, config_dict=None):
        """If shapeID not specified, sets default value from config."""
        if not self.shapeID:
            self.shapeID = config_dict['default_shape_name']
        return self

