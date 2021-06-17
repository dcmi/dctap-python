"""Classes for Python objects derived from CSV files."""

from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import List
from .config import get_config_dict
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
    mandatory: str = None
    repeatable: str = None
    valueNodeType: str = ""
    valueDataType: str = ""
    valueConstraint: str = ""
    valueConstraintType: str = ""
    valueShape: str = ""
    note: str = ""
    sc_warnings: dict = field(default_factory=dict)

    config_dict = get_config_dict()

    def reset_config_dict(self, external_config_dict=None):
        self.config_dict = external_config_dict

    def normalize(self):
        """Normalizes values of certain fields."""
        # self._normalize_value_node_type(config_dict)
        # self._warn_about_literal_datatype_used_with_uri()
        return True

    def validate(self):
        """Validates values of certain fields."""
        self._value_uri_should_not_have_nodetype_literal()
        self._value_node_type_is_from_enumerated_list()
        self._mandatory_and_repeatable_have_supported_boolean_value()
        self._warn_if_propertyID_and_valueShape_are_not_IRIs()
        return self

    def _value_uri_should_not_have_nodetype_literal(self):
        """IRI values should usually not have a valueNodeType of Literal."""
        if is_uri_or_prefixed_uri(self.valueConstraint):
            if "Literal" in self.valueNodeType:
                self.sc_warnings['valueNodeType'] = (
                    f"{repr(self.valueConstraint)} looks like an IRI, but "
                    f"valueNodeType is {repr(self.valueNodeType)}."
                )
        return self

    def _value_node_type_is_from_enumerated_list(self):
        """Take valueNodeType from configurable enumerated list, case-insensitive."""
        valid_types = [nt.lower() for nt in self.config_dict['value_node_types']]
        if self.valueNodeType:
            self.valueNodeType = self.valueNodeType.lower() # normalize to lowercase
            if self.valueNodeType not in valid_types:
                self.sc_warnings['valueNodeType'] = (
                    f"{repr(self.valueNodeType)} is not a valid node type."
                )
        return self

    def _mandatory_and_repeatable_have_supported_boolean_value(self):
        """mandatory or repeatable has value of "true" or "false" or "1" or "0"."""
        valid_values_for_true = [ "true", "1", None ]
        valid_values_for_false = [ "false", "0", None ]
        valid_values = valid_values_for_true + valid_values_for_false
        if self.mandatory is not None:
            local_mandatory = self.mandatory.lower() # normalize to lowercase
            if local_mandatory in valid_values_for_true:
                self.mandatory = True
            elif local_mandatory in valid_values_for_false:
                self.mandatory = False
            elif local_mandatory not in valid_values:
                self.sc_warnings['mandatory'] = (
                    f"{repr(self.mandatory)} is not a supported Boolean value."
                )
        if self.repeatable is not None:
            local_repeatable = self.repeatable.lower() # normalize to lowercase
            if local_repeatable in valid_values_for_true:
                self.repeatable = True
            elif local_repeatable in valid_values_for_false:
                self.repeatable = False
            elif local_repeatable not in valid_values:
                self.sc_warnings['repeatable'] = (
                    f"{repr(self.repeatable)} is not a supported Boolean value."
                )
        return self

    def _warn_if_propertyID_and_valueShape_are_not_IRIs(self):
        """@@@"""
        if not is_uri_or_prefixed_uri(self.propertyID):
            self.sc_warnings['propertyID'] = (
                f"{repr(self.propertyID)} is not an IRI or Compact IRI."
            )
        if self.valueShape:
            if not is_uri_or_prefixed_uri(self.valueShape):
                self.sc_warnings['valueShape'] = (
                    f"{repr(self.valueShape)} is not an IRI or Compact IRI."
                )


    def get_warnings(self):
        """Emit warnings dictionary for this instance of TAPStatementConstraint.
        -- Dictionary is populated by invoking validate() mathod."""
        return dict(self.sc_warnings)


@dataclass
class TAPShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    start: bool = False
    sc_list: List[TAPStatementConstraint] = field(default_factory=list)
    sh_warnings: dict = field(default_factory=dict)

    def validate(self, config_dict=None):
        """Normalize values where required."""
        self._normalize_default_shapeID(config_dict)
        self._warn_if_shapeID_is_not_an_IRI()
        return True

    def _normalize_default_shapeID(self, config_dict=None):
        """If shapeID not specified, sets default value from config."""
        if not self.shapeID:
            self.shapeID = config_dict['default_shape_name']
        return self

    def _warn_if_shapeID_is_not_an_IRI(self):
        """@@@"""
        if not is_uri_or_prefixed_uri(self.shapeID):
            self.sh_warnings['shapeID'] = (
                f"{repr(self.shapeID)} is not an IRI or Compact IRI."
            )

    def get_warnings(self):
        """Emit warnings dictionary for this instance of TAPShape.
        -- Dictionary is populated by invoking validate() mathod."""
        return dict(self.sh_warnings)

