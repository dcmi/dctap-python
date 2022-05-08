.. _picklist_valuenodetype:

valueNodeType as a picklist element
...................................

According to the `DCTAP Primer <https://www.dublincore.org/groups/application_profiles_ig/dctap_primer/>`__, the minimal set of values for **valueNodeType** is "IRI", "bnode", and "literal". In practice, it is often necessary to say that the value is not a literal, but an "IRI or bnode". It is of course possible to handle this by declaring **valueNoteType** to be a picklist element as described in the section :ref:`picklist_elements` above. 

It can however be convenient to coin extra node types to cover the most common use cases. ShEx covers this case with the value `"nonliteral" <http://shex.io/shex-semantics/#nodeKind>`__, while SHACL provides three additional pairwise combinations, `"sh:BlankNodeOrIRI", "sh:BlankNodeOrLiteral", and "sh:IRIOrLiteral" <https://www.w3.org/TR/shacl/#syntax-rule-nodeKind-in>`__. One may also want to use "URI" instead of "IRI".

Any or all of these options can be activated by editing the configuration file accordingly::

    extra_value_node_types:
    - uri
    - nonliteral
    - IRIOrLiteral
