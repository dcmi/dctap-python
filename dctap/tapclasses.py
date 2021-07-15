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
    mandatory: str = ""
    repeatable: str = ""
    valueNodeType: str = ""
    valueDataType: str = ""
    valueConstraint: str = ""
    valueConstraintType: str = ""
    valueShape: str = ""
    note: str = ""
    sc_warnings: dict = field(default_factory=dict)
    extra_elements: dict = field(default_factory=dict)

    def normalize(self, settings):
        """Normalizes specific fields."""
        # pylint: disable=attribute-defined-outside-init
        self._warn_if_propertyID_or_valueDataType_not_IRIlike()
        self._normalize_booleans_mandatory_repeatable()
        self._valueConstraintType_pattern_warn_if_valueConstraint_not_valid_regex()
        self._valueConstraintType_pattern_warn_if_used_with_value_shape()
        self._valueConstraintType_iristem_parse()
        self._valueConstraintType_iristem_warn_if_list_items_not_IRIs()
        self._valueConstraintType_languageTag_parse(settings)
        self._valueConstraintType_warn_if_used_without_valueConstraint()
        self._valueDataType_warn_if_used_with_valueNodeType_IRI()
        self._valueDataType_warn_if_valueNodeType_literal_used_with_any_valueShape()
        self._valueConstraintType_picklist_parse(settings)
        self._valueNodeType_is_from_enumerated_list(settings)
        self._parse_elements_listed_in_configfile_as_lists(settings)
        return self

    def _warn_if_propertyID_or_valueDataType_not_IRIlike(self):
        """@@@"""
        if not is_uri_or_prefixed_uri(self.propertyID):
            self.sc_warnings[
                "propertyID"
            ] = f"{repr(self.propertyID)} is not an IRI or Compact IRI."
        if self.valueDataType:
            if not is_uri_or_prefixed_uri(self.valueDataType):
                self.sc_warnings[
                    "valueDataType"
                ] = f"{repr(self.valueDataType)} is not an IRI or Compact IRI."

    def _normalize_booleans_mandatory_repeatable(self):
        """Booleans take true/false (case-insensitive) or 1/0, default None."""

        valid_values_for_true = ["true", "1"]
        valid_values_for_false = ["false", "0"]
        valid_values = valid_values_for_true + valid_values_for_false

        # pylint: disable=singleton-comparison
        if self.mandatory:
            mand = self.mandatory.lower()
            if mand not in valid_values:
                self.sc_warnings[
                    "mandatory"
                ] = f"{repr(self.mandatory)} is not a supported Boolean value."
            if mand in valid_values_for_true:
                self.mandatory = "True"
            elif mand in valid_values_for_false:
                self.mandatory = "False"

        if self.repeatable:
            repeat = self.repeatable.lower()
            if repeat not in valid_values:
                self.sc_warnings[
                    "repeatable"
                ] = f"{repr(self.repeatable)} is not a supported Boolean value."
            if repeat in valid_values_for_true:
                self.repeatable = "True"
            elif repeat in valid_values_for_false:
                self.repeatable = "False"

        return self

    def _valueConstraintType_iristem_parse(self):
        """If valueConstraintType is Iristem, split valueConstraint on whitespace."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "iristem":
            if self.valueConstraint:
                self.valueConstraint = self.valueConstraint.split()
        return self

    def _valueConstraintType_iristem_warn_if_list_items_not_IRIs(self):
        """If IRIStem, warn if valueConstraint list items do not look like IRIs."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "iristem":
            for list_item in self.valueConstraint:
                if not is_uri_or_prefixed_uri(list_item):
                    self.sc_warnings["valueConstraint"] = (
                        f"Value constraint type is {repr(self.valueConstraintType)}, "
                        f"but {repr(list_item)} does not look like an IRI or "
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

    def _valueConstraintType_pattern_warn_if_used_with_value_shape(self):
        """Regular expressions cannot conform to value shapes."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if self.valueConstraintType == "pattern":
            if self.valueShape:
                self.sc_warnings["valueConstraintType"] = (
                    f"Value constraint type "
                    f"({repr(self.valueConstraintType)}) "
                    "cannot conform to a value shape."
                )

    def _valueConstraintType_languageTag_parse(self, settings):
        """For valueConstraintType languageTag, splits valueConstraint on whitespace."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if settings.get("picklist_item_separator"):
            sep = settings.get("picklist_item_separator")
        else:
            sep = " "
        if self.valueConstraintType == "languagetag":
            if self.valueConstraint:
                self.valueConstraint = self.valueConstraint.split(sep)
                self.valueConstraint = [x.strip() for x in self.valueConstraint if x]
        return self

    def _valueConstraintType_warn_if_used_without_valueConstraint(self):
        """Warns if valueConstraintType used without valueConstraint."""
        if self.valueConstraintType:
            if not self.valueConstraint:
                self.sc_warnings["valueConstraint"] = (
                    f"Value constraint type "
                    f"({repr(self.valueConstraintType)}) "
                    "but no value constraint."
                )
        return self

    def _valueConstraintType_picklist_parse(self, settings):
        """If valueConstraintType is Picklist, split valueConstraint on whitespace."""
        self.valueConstraintType = self.valueConstraintType.lower()
        if settings.get("picklist_item_separator"):
            sep = settings.get("picklist_item_separator")
        else:
            sep = " "
        if self.valueConstraintType == "picklist":
            if self.valueConstraint:
                self.valueConstraint = self.valueConstraint.split(sep)
                self.valueConstraint = [x.strip() for x in self.valueConstraint if x]
        return self

    def _valueNodeType_is_from_enumerated_list(self, settings):
        """Take valueNodeType from configurable enumerated list, case-insensitive."""
        valid_types = ["iri", "bnode", "literal"]
        if settings.get("value_node_types"):
            valid_types += [vnt.lower() for vnt in settings["value_node_types"]]
        if self.valueNodeType:
            self.valueNodeType = self.valueNodeType.lower()  # normalize to lowercase
            if self.valueNodeType not in valid_types:
                self.sc_warnings[
                    "valueNodeType"
                ] = f"{repr(self.valueNodeType)} is not a valid node type."
        return self

    def _valueDataType_warn_if_valueNodeType_literal_used_with_any_valueShape(self):
        """Value with node type Literal cannot conform to a value shape."""
        self.valueNodeType = self.valueNodeType.lower()
        if self.valueShape:
            if self.valueNodeType == "literal":
                self.sc_warnings["valueDataType"] = (
                    "Datatypes are only for literals, "
                    "which cannot conform to a value shape."
                )

    def _valueDataType_warn_if_used_with_valueShape(self):
        """Value with any datatype cannot conform to a value shape."""
        if self.valueShape:
            if self.valueDataType:
                self.sc_warnings["valueDataType"] = (
                    "Datatypes are only for literals, "
                    "which cannot conform to a value shape."
                )

    def _valueDataType_warn_if_used_with_valueNodeType_IRI(self):
        """Value with datatype implies Literal and cannot be node type IRI."""
        node_type = self.valueNodeType.lower()
        if node_type in ("iri", "uri", "bnode"):
            if self.valueDataType:
                self.sc_warnings["valueDataType"] = (
                    f"Datatypes are only for literals, "
                    f"so node type should not be {repr(self.valueNodeType)}."
                )

    def _parse_elements_listed_in_configfile_as_lists(self, settings):
        """@@@"""
        if settings.get("picklist_item_separator"):
            sep = settings.get("picklist_item_separator")
        else:
            sep = " "
        # breakpoint(context=5)
        if settings.get("elements_parsed_as_lists"):
            elements_to_parse_as_lists = settings.get("elements_parsed_as_lists")

        for element in elements_to_parse_as_lists:
            if element == "propertyID":
                if self.propertyID:
                    self.propertyID = self.propertyID.split(sep)
                    self.propertyID = [x.strip() for x in self.propertyID if x]
            if element == "propertyLabel":
                if self.propertyLabel:
                    self.propertyLabel = self.propertyLabel.split(sep)
                    self.propertyLabel = [x.strip() for x in self.propertyLabel if x]
            if element == "valueNodeType":
                if self.valueNodeType:
                    self.valueNodeType = self.valueNodeType.split(sep)
                    self.valueNodeType = [x.strip() for x in self.valueNodeType if x]
            if element == "valueDataType":
                if self.valueDataType:
                    self.valueDataType = self.valueDataType.split(sep)
                    self.valueDataType = [x.strip() for x in self.valueDataType if x]
            if element == "valueShape":
                if self.valueShape:
                    self.valueShape = self.valueShape.split(sep)
                    self.valueShape = [x.strip() for x in self.valueShape if x]
            if element == "note":
                if self.note:
                    self.note = self.note.split(sep)
                    self.note = [x.strip() for x in self.note if x]
        return self

    def get_warnings(self):
        """Emit warnings dictionary self.sc_warnings, populated by normalize() method."""
        return dict(self.sc_warnings)


@dataclass
class TAPShape:
    """Instances hold TAP/CSV row elements related to shapes."""

    # pylint: disable=invalid-name
    # True that propertyID, etc, do not conform to snake-case naming style.

    shapeID: str = ""
    shapeLabel: str = ""
    sc_list: List[TAPStatementConstraint] = field(default_factory=list)
    sh_warnings: dict = field(default_factory=dict)
    extra_elements: dict = field(default_factory=dict)

    def normalize(self, settings):
        """Normalize values where required."""
        self._normalize_default_shapeID(settings)
#        self._parse_elements_listed_in_configfile_as_lists(settings)
        return True

    def _normalize_default_shapeID(self, settings):
        """If shapeID not specified, looks first in config, else sets "default"."""
        if not self.shapeID:
            if settings.get("default_shape_identifier"):
                self.shapeID = settings.get("default_shape_identifier")
            else:
                self.shapeID = "default"
        return self

#    def _parse_elements_listed_in_configfile_as_lists(self, settings):
#        """@@@"""
#        if settings.get("picklist_item_separator"):
#            sep = settings.get("picklist_item_separator")
#        else:
#            sep = " "
#
#        if settings.get("elements_parsed_as_lists"):
#            elements_to_parse_as_lists = settings.get("elements_parsed_as_lists")
#
#        for element in elements_to_parse_as_lists:
#            if element == "shapeLabel":
#                if self.shapeLabel:
#                    self.shapeLabel = self.shapeLabel.split(sep)
#                    self.shapeLabel = [x.strip() for x in self.shapeLabel if x]
#        return self


    def get_warnings(self):
        """Emit warnings dictionary self.sh_warnings, populated by normalize() method."""
        return dict(self.sh_warnings)
