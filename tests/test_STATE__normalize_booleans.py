"""Test for elements mandatory and repeatable."""

from textwrap import dedent
import pytest
from dctap.config import get_config
from dctap.tapclasses import TAPStatementTemplate
from dctap.inspect import pprint_tapshapes

def test_mandatory_repeatable_true_given_supported_boolean_values():
    """Literal 'True' (case-insensitive) is a supported Boolean value."""
    st = TAPStatementTemplate()
    st.mandatory = "true"
    st.repeatable = "FALSE"
    st._normalize_booleans()
    assert st.mandatory == "true"
    assert st.repeatable == "false"

def test_mandatory_and_repeatable_one_zero_normalized_to_true_false():
    """The integers 0 and 1 are supported Boolean values."""
    st = TAPStatementTemplate()
    st.mandatory = "1"
    st.repeatable = "0"
    st._normalize_booleans()
    assert st.mandatory == "true"
    assert st.repeatable == "false"

def test_mandatory_and_repeatable_default_to_empty_strings():
    """The Boolean elements remain empty strings if no value is declared."""
    st = TAPStatementTemplate()
    st._normalize_booleans()
    assert st.mandatory == ""
    assert st.repeatable == ""

def test_mandatory_and_repeatable_raise_warn_unsupported_boolean_values():
    """Warn about unsupported Boolean values."""
    st = TAPStatementTemplate()
    st.mandatory = "WAHR"
    st.repeatable = "FALSCH"
    st._normalize_booleans()
    assert len(st.state_warns) == 2
    assert st.mandatory == "WAHR"
    assert st.repeatable == "FALSCH"
    assert st.state_warns 
    warning_for_true = "'WAHR' is not a supported Boolean value."
    warning_for_false = "'FALSCH' is not a supported Boolean value."
