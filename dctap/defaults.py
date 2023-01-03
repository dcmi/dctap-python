"""Default settings."""

from functools import wraps
from .exceptions import DecoratorError
from .tapclasses import TAPShape, TAPStatementTemplate


CONFIGFILE = "dctap.yaml"
CONFIGYAML = """\
# dctap configuration file (in YAML format)
# See https://dctap-python.readthedocs.io/en/latest/config/ for more options

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
"""


def dctap_defaults():
    """Decorator that passes dctap package defaults."""
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            kwargs["shapeclass"] = TAPShape
            kwargs["stateclass"] = TAPStatementTemplate
            kwargs["configyaml"] = CONFIGYAML
            kwargs["configfile"] = CONFIGFILE
            try:  # if decorated function is not set up to receive **kwargs
                return func(**kwargs)
            except TypeError as te:
                name = func.__name__
                deco = dctap_defaults.__name__
                message = f"@{deco}-only kwarg explicitly passed to {name}()."
                raise DecoratorError(message) from te
        return wrapper
    return decorator
