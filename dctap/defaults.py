"""Default settings."""

DEFAULT_CONFIGFILE_NAME = "dctap.yml"

DEFAULT_CONFIG_YAML = """### dctap configuration file (in YAML format)

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

### There must be a shape identifier in order to ensure consistency
### of JSON and YAML output. A different default identifier can be
### set here, but the module will not permit the identifier to be a
### string of zero length (and will revert to "default").
default_shape_identifier: "default"

### Separator for items in a picklist (default: single blank space).
### Can be configured with other common separators - eg, comma or pipe (or-bar).
### Extra whitespace is routinely stripped from start and end of picklist items.
picklist_item_separator: " "

### User-customized statement constraints can be added here.
### For example, min/max is a popular alternative to mandatory/repeatable.
extra_statement_constraint_elements:
- min
- max

### Element aliases can shorten header lines.
element_aliases:
    "PropID": "propertyID"
    "PropLabel": "propertyLabel"
    "Value": "valueConstraint"
    "ValueType": "valueConstraintType"
    "DataType": "valueDataType"
    "NodeType": "valueNodeType"
    "ShapeRef": "valueShape"
    "Mand": "mandatory"
    "Rep": "repeatable"

### Some statement constraint elements can be configured as picklists.
### These can take multiple values - eg: "this that" ("this" or "that").
### Values are separated by configurable picklist item separator (see below).
### Types of element that cannot be configured for multiple values:
### - Elements with numeric values: min, max
### - Elements with Boolean values: closed, start, mandatory, repeatable
### - Elements used purely for annotation: shapeLabel, propertyLabel, note
# picklist_elements:
# - propertyID
# - valueNodeType
# - valueDataType
# - valueShape

### This module ignores elements (column headers) that are not part of the
### base DCTAP model unless they are configured here as "extra" elements.
###
### Extra elements must be designated either as "shape" elements (eg, "closed
### or "start") or as "statement constraint" elements (eg, "min" and "max").
### As extra elements are not supported by this module, their values are
### simply passed through to the text, JSON, and YAML outputs.
# extra_shape_elements:
# - closed
# - start

### This module has three built-in value node types: "iri", "literal", and "bnode".
### Extra node types can be added here, for example as aliases, such as "uri" for "iri",
### or as combinations of node types, such as "shacl:BlankNodeOrLiteral".
# extra_value_node_types:
# - uri

"""
