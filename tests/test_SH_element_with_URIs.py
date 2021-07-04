"""Test for elements mandatory and repeatable."""

from dctap.tapclasses import TAPShape


def test_warn_if_shapeID_not_URI():
    """@@@."""
    shap = TAPShape()
    shap.shapeID = "book"
    shap.sc_list = []
    shap.sc_list.append({"propertyID": "dct:creator"})
    shap._warn_if_shapeID_is_not_an_IRI()
    assert len(shap.sh_warnings) == 1
