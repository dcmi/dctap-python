"""Classes for Python objects derived from CSV files."""

import re
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
    mandatory: str = None
    repeatable: str = None
    valueNodeType: str = ""
    valueDataType: str = ""
    valueConstraint: str = ""
    valueConstraintType: str = ""
    valueShape: str = ""
    note: str = ""
    sc_warnings: dict = field(default_factory=dict)

    def validate(self, config_dict):
        """Validates specific fields."""
        # pylint: disable=attribute-defined-outside-init
        self.config_dict = config_dict
        self._elements_taking_IRIs_warn_if_not_IRIs()
        self._mandatory_repeatable_have_supported_boolean_values()
        self._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
        self._valueConstraintType_iristem_warn_if_valueConstraint_not_is_not_an_IRI()
        self._valueConstraintType_picklist_parse()
        self._valueConstraintType_languageTag_parse()
        self._valueConstraintType_warn_if_used_without_valueConstraint()
        self._valueDataType_warn_if_used_with_valueNodeType_IRI()
        self._valueNodeType_is_from_enumerated_list()
        return self

    def _elements_taking_IRIs_warn_if_not_IRIs(self):
        """@@@"""
        if not is_uri_or_prefixed_uri(self.propertyID):
            self.sc_warnings[
                "propertyID"
            ] = f"{repr(self.propertyID)} is not an IRI or Compact IRI."
        if self.valueShape:
            if not is_uri_or_prefixed_uri(self.valueShape):
                self.sc_warnings[
                    "valueShape"
                ] = f"{repr(self.valueShape)} is not an IRI or Compact IRI."
        if self.valueDataType:
            if not is_uri_or_prefixed_uri(self.valueDataType):
                self.sc_warnings[
                    "valueDataType"
                ] = f"{repr(self.valueDataType)} is not an IRI or Compact IRI."

    def _mandatory_repeatable_have_supported_boolean_values(self):
        """Booleans take true/false (case-insensitive) or 1/0, default None."""

        valid_values_for_true = ["true", "1"]
        valid_values_for_false = ["false", "0"]
        valid_values = valid_values_for_true + valid_values_for_false + [None]

        # pylint: disable=singleton-comparison
        if self.mandatory != None:
            # breakpoint(context=5)
            mand = self.mandatory.lower()
            if mand not in valid_values and mand != "":
                self.sc_warnings[
                    "mandatory"
                ] = f"{repr(self.mandatory)} is not a supported Boolean value."
            if mand in valid_values_for_true:
                self.mandatory = True
            elif mand in valid_values_for_false:
                self.mandatory = False

        if self.repeatable != None:
            # breakpoint(context=5)
            repeat = self.repeatable.lower()
            if repeat not in valid_values and repeat != "":
                self.sc_warnings[
                    "repeatable"
                ] = f"{repr(self.repeatable)} is not a supported Boolean value."
            if repeat in valid_values_for_true:
                self.repeatable = True
            elif repeat in valid_values_for_false:
                self.repeatable = False

        return self

    def _valueConstraintType_iristem_warn_if_valueConstraint_not_is_not_an_IRI(self):
        """If valueConstraintType IRIStem, warn if valueConstraint not an IRI."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "iristem":
            if not is_uri_or_prefixed_uri(self.valueConstraint):
                self.sc_warnings["valueConstraint"] = (
                    f"Value constraint type is {repr(self.valueConstraintType)}, but "
                    f"{repr(self.valueConstraint)} does not look like an IRI or "
                    "Compact IRI."
                )
        return self

    def _valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex(self):
        """If valueConstraintType Pattern, warn if valueConstraint not valid regex."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "pattern":
            try:
                re.compile(self.valueConstraint)
            except (re.error, TypeError):
                self.sc_warnings["valueConstraint"] = (
                    f"Value constraint type is {repr(self.valueConstraintType)}, but "
                    f"{repr(self.valueConstraint)} is not a valid regular expression."
                )
        return self

    def _valueConstraintType_languageTag_parse(self):
        """For valueConstraintType languageTag, splits valueConstraint on whitespace."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "languagetag":
            if self.valueConstraint:
                self.valueConstraint = self.valueConstraint.split()
        return self

    def _valueConstraintType_picklist_parse(self):
        """If valueConstraintType is Picklist, splits valueConstraint on whitespace."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "picklist":
            if self.valueConstraint:
                self.valueConstraint = self.valueConstraint.split()
        return self

    def _valueConstraintType_warn_if_used_without_valueConstraint(self):
        """Warns if valueConstraintType used without valueConstraint."""
        if self.valueConstraintType:
            if not self.valueConstraint:
                self.sc_warnings["valueConstraint"] = (
                    f"Value constraint type is {repr(self.valueConstraintType)}, but "
                    f"value constraint is empty."
                )
        return self

    def _valueNodeType_is_from_enumerated_list(self):
        """Take valueNodeType from configurable enumerated list, case-insensitive."""
        if self.config_dict["value_node_types"]:
            valid_types = [vnt.lower() for vnt in self.config_dict["value_node_types"]]
        else:
            valid_types = ["iri", "bnode", "literal"]
        if self.valueNodeType:
            self.valueNodeType = self.valueNodeType.lower()  # normalize to lowercase
            if self.valueNodeType not in valid_types:
                self.sc_warnings[
                    "valueNodeType"
                ] = f"{repr(self.valueNodeType)} is not a valid node type."
        return self

    def _valueDataType_warn_if_used_with_valueNodeType_IRI(self):
        """@@@"""
        node_type = self.valueNodeType.lower()
        if node_type in ('iri', 'uri', 'bnode'):
            if self.valueDataType:
                self.sc_warnings["valueDataType"] = (
                    f"Datatypes are only for literals, "
                    f"so node type should not be {repr(self.valueNodeType)}."
                )

    def get_warnings(self):
        """Emit warnings dictionary self.sc_warnings, populated by validate() method."""
        return dict(self.sc_warnings)


@dataclass
class TAPShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    sc_list: List[TAPStatementConstraint] = field(default_factory=list)
#    statement_constraints: List[TAPStatementConstraint] = field(default_factory=list)
    sh_warnings: dict = field(default_factory=dict)

    def validate(self, config_dict=None):
        """Normalize values where required."""
        self._normalize_default_shapeID(config_dict)
        self._warn_if_shapeID_is_not_an_IRI()
        return True

    def _normalize_default_shapeID(self, config_dict=None):
        """If shapeID not specified, sets default value from config."""
        if not self.shapeID:
            self.shapeID = config_dict["default_shape_name"]
        return self

    def _warn_if_shapeID_is_not_an_IRI(self):
        """@@@"""
        if not is_uri_or_prefixed_uri(self.shapeID):
            self.sh_warnings[
                "shapeID"
            ] = f"{repr(self.shapeID)} is not an IRI or Compact IRI."

    def get_warnings(self):
        """Emit warnings dictionary self.sh_warnings, populated by validate() method."""
        return dict(self.sh_warnings)
