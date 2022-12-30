"""Default settings."""

from functools import wraps
from .tapclasses import TAPShape, TAPStatementTemplate

CONFIGYAML = """### dctap configuration file (in YAML format)

# See https://dctap-python.readthedocs.io/en/latest/config/
# for advanced configuration options

prefixes:
    ":":        "http://example.org/"
    "dc:":      "http://purl.org/dc/elements/1.1/"
    "dcterms:": "http://purl.org/dc/terms/"
    "dct:":     "http://purl.org/dc/terms/"
    "foaf:":    "http://xmlns.com/foaf/0.1/"
    "owl:":     "http://www.w3.org/2002/07/owl#"
    "rdf:":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    "rdfs:":    "http://www.w3.org/2000/01/rdf-schema#"
    "schema:":  "http://schema.org/"
    "skos:":    "http://www.w3.org/2004/02/skos/core#"
    "skosxl:":  "http://www.w3.org/2008/05/skos-xl#"
    "wdt:":     "http://www.wikidata.org/prop/direct/"
    "xsd:":     "http://www.w3.org/2001/XMLSchema#"

### Element aliases for shorter, translated, or preferred CSV column names.
# extra_element_aliases:
#     "PropID": "propertyID"
#     "PropLabel": "propertyLabel"
#     "Value": "valueConstraint"
#     "ValueType": "valueConstraintType"
#     "DataType": "valueDataType"
#     "NodeType": "valueNodeType"
#     "ShapeRef": "valueShape"
#     "Mand": "mandatory"
#     "Rep": "repeatable"
"""


def dctap_defaults(shape_class=None, state_class=None, configfile=None, yamldoc=None):
    """Passes hard-wired default argument values to decorated function."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["shape_class"] = TAPShape
            kwargs["state_class"] = TAPStatementTemplate
            kwargs["configfile"] = "dctap.yaml"
            kwargs["yamldoc"] = """prefixes:\n "ex:": "http://example.org/"\n"""
            try:
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                raise TypeError(f"{name}() got unexpected kwarg from @{deco}") from te
        return wrapper
    return decorator


