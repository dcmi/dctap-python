.. _extra_value_node_types:

Extra value node types
......................

Out of the box, DCTAP supports the three node types of the graph-based data model as defined in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#data-model>`_: IRI, literal, and blank node. These are represented in a :term:`DCTAP Instance` with "IRI", "Literal", and "BNode" as keywords for the element :ref:`elem_valueNodeType`. Users can extend this list of supported keywords with aliases for supported node types, such as "URI" (for "IRI") or with combinations of node types that will be understood by their own applications downstream, such as "Nonliteral"  or "BlankNodeOrIRI".

