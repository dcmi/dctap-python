.. _elem_valueDataType:

valueDataType
^^^^^^^^^^^^^

The DCTAP model was designed for compatability with the
RDF model. In the RDF model, literal values can be tagged
with a datatype that marks the value as a date, string,
decimal number, and the like. The most commonly used
datatypes are defined in the `W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes specification <https://www.w3.org/TR/xmlschema11-2/>`_.

Because datatypes are identified by IRI, this module
issues a warning if a non-IRI keyword is encountered.
Users not interested in compatability with RDF can safely
ignore such a warning.

.. csv-table:: 
   :file: valueDataType.csv
   :header-rows: 1

Interpreted, with a warning, as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dc:creator
                valueDataType:       xsd:string
            Statement Constraint
                propertyID:          dct:date
                valueDataType:       Date

    WARNING Shape :default => valueDataType: 'Date' is not an IRI or Compact IRI.

Datatypes are used only with literal values, so 
if a node is of type "URI", "IRI", or "BNode" and 
any datatype is provided, this will trigger a 
warning.

Note that if a URI is meant to be processed as a 
string, the node type should be "Literal".

.. csv-table:: 
   :file: valueDataType_with_valueNodeType_URI.csv
   :header-rows: 1

Interpreted, with a warning, as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:creator
                valueNodeType:       iri
                valueDataType:       xsd:string
            Statement Constraint
                propertyID:          dcterms:subject
                valueNodeType:       bnode
                valueDataType:       xsd:string

    WARNING Shape :default => valueDataType: Datatypes are for literals only, and node type provided is 'iri'.
    WARNING Shape :default => valueDataType: Datatypes are for literals only, and node type provided is 'bnode'.
