"""Default settings."""

DEFAULT_CONFIGFILE_NAME = "dctap.yaml"

DEFAULT_HIDDEN_CONFIGFILE_NAME = ".dctaprc"

DEFAULT_CONFIG_YAML = """### dctap configuration file (in YAML format)

### A default shape identifier is needed to ensure the consistency
### of JSON and YAML output; the default identifier is "default".
### A different default identifier can be set here.
### Note that if identifier is set here to a string of zero length,
### the identifier will revert to "default".
# default_shape_identifier: "default"

### URIs may be shortened in a CSV by using namespace prefixes.
### Here is a selection of common prefixes:
# prefixes:
#     ":":        "http://example.org/"
#     "dc:":      "http://purl.org/dc/elements/1.1/"
#     "dcterms:": "http://purl.org/dc/terms/"
#     "dct:":     "http://purl.org/dc/terms/"
#     "foaf:":    "http://xmlns.com/foaf/0.1/"
#     "owl:":     "http://www.w3.org/2002/07/owl#"
#     "rdf:":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#     "rdfs:":    "http://www.w3.org/2000/01/rdf-schema#"
#     "schema:":  "http://schema.org/"
#     "skos:":    "http://www.w3.org/2004/02/skos/core#"
#     "skosxl:":  "http://www.w3.org/2008/05/skos-xl#"
#     "wdt:":     "http://www.wikidata.org/prop/direct/"
#     "xsd:":     "http://www.w3.org/2001/XMLSchema#"

### This module ignores elements (column headers) that are not part of the
### base DCTAP model unless they are configured here as "extra" elements.
###
### Extra elements must be declared either as "shape" elements
### or as "statement template" elements.
###
### Values for extra elements are passed through to text, JSON, and
### YAML outputs.
###
### Custom shape elements can be added here.
### Example: in some shape languages, a shape may be "closed".
# extra_shape_elements:
# - "closed"
###
### Custom statement templates can be added here.
### Example: "min" and "max" are popular alternatives to "mandatory" and
### "repeatable" for expressing the cardinality of statement templates.
# extra_statement_template_elements:
# - "min"
# - "max"

### Some statement template elements can be configured as list elements. 
### A given value of a list element is parsed as a set of multiple 
### values separated by a configurable list item separator (see below).
###
### What exactly it means for a given element to have multiple values 
### is application-dependent, so their configurability is considered to be
### an extension of the core DCTAP model. Users cannot not expect multiple 
### values to be interpreted in universally interoperable ways.
###
### Some types of element cannot be configured for multiple values:
### - Elements with numeric values: min, max
### - Elements with Boolean values: closed, start, mandatory, repeatable
### - Elements used purely for annotation: shapeLabel, propertyLabel, note
###
### The job of this module, dctap-python, is to generate output where list
### elements have been parsed as lists. What downstream applications that take
### this output as their input then do with this lists is beyond the scope of 
### the base DCTAP model.
###
### As discussed in https://dctap-python.readthedocs.io/en/latest/, 
### elements such as the following may be parsed as lists:
# list_elements:
# - "propertyID"
# - "valueNodeType"
# - "valueDataType"
###
### The value of a list element is intended to be split into substrings 
### on the basis of a given character - by default, a single blank space, 
### or alternatively by a comma (",") or pipe ("|").
### Extra whitespace is stripped from start and end of the resulting list items.
# list_item_separator: ","

### This module has three built-in value node types: "iri", "literal", and "bnode".
###
### Extra node types can be added here for use as aliases (eg "uri" for "iri") or
### as shortcuts for combinations of node types (eg, "nonliteral" for "iri OR bnode").
# extra_value_node_types:
# - "uri"
# - "nonliteral"

### Element aliases can shorten header lines.
# element_aliases:
#     "PropID": "propertyID"
#     "PropLabel": "propertyLabel"
#     "Value": "valueConstraint"
#     "ValueType": "valueConstraintType"
#     "DataType": "valueDataType"
#     "NodeType": "valueNodeType"
#     "ShapeRef": "valueShape"
#     "Mand": "mandatory"
#     "Rep": "repeatable"

### Aliases for Boolean values may make more sense in a given user community.
### As of May 2022, not yet implemented.
# boolean_aliases:
#     "Y": "true"
#     "N": "false"
"""
