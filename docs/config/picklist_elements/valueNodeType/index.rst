.. _picklist_valuenodetype:

Extra Value Node Types
......................

According to the `DCTAP Primer <https://www.dublincore.org/groups/application_profiles_ig/dctap_primer/>`__, DCTAP supports the three node types of the graph-based data model as defined in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#data-model>`_: IRI, literal, and blank node. These are represented in a :term:`TAP` with "IRI", "Literal", and "BNode" as keywords for the element :ref:`elem_valueNodeType`. Users can extend this list of supported keywords with aliases for supported node types, such as "URI" (for "IRI") or with combinations of node types that will be understood by applications downstream.

For example, it is often necessary to say that the value is "not a literal" or, in other words, that it is an "IRI or bnode". It is of course possible to handle this by declaring **valueNoteType** to be a picklist element as described in the section :ref:`picklist_elements` above. It can however be convenient to coin extra node types to cover the most common use cases. ShEx covers this case with the value `"nonliteral" <http://shex.io/shex-semantics/#nodeKind>`__, while SHACL provides three additional pairwise combinations, `"sh:BlankNodeOrIRI", "sh:BlankNodeOrLiteral", and "sh:IRIOrLiteral" <https://www.w3.org/TR/shacl/#syntax-rule-nodeKind-in>`__. One may also want to use "URI" instead of "IRI".

Any or all of these options can be activated by editing the configuration file accordingly::

    extra_value_node_types:
    - uri
    - nonliteral
    - IRIOrLiteral
