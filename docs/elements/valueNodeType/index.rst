.. _elem_valueNodeType:

valueNodeType
^^^^^^^^^^^^^

The DCTAP model was designed for compatibility with 
the RDF model. In the RDF model, there are three types 
of node: an :term:`IRI` (or URI), a BNode, and a Literal.

Users not interested in compatibility with RDF can 
safely ignore this element.

**dctap** issues a warning if an unsupported value is 
provided (here: "Concept").

.. csv-table:: 
   :file: valueNodeType.csv
   :header-rows: 1

Interpreted, with a warning, as::

    DCTAP instance
	Shape
	    shapeID                  default
	    Statement Template
		propertyID           dcterms:title
		valueNodeType        literal
	    Statement Template
		propertyID           dcterms:creator
		valueNodeType        uri
	    Statement Template
		propertyID           dcterms:subject
		valueNodeType        concept

    WARNING [default/valueNodeType] 'concept' is not a valid node type.
