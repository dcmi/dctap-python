.. _config:

Configuration
-------------

`dctap` has built-in defaults for configuration settings that are customizable by users by generating and editing configuration file as explained in the section :ref:`cli_init`. These editable defaults are:

- **Default shape name**. When shape identifiers are not provided in a CSV, a configurable default shape name is used (see section :ref:`elem_shapeID`).
- **Value node types**. Out of the box, DCTAP supports the three node types of the graph-based data model as defined in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#data-model>`_: IRI, literal, and blank node. These are represented in a :term:`DCTAP Instance` with ``IRI``, ``Literal``, and ``BNode`` as keywords for the element :ref:`elem_valudNodeType`. Users can extend this list of supported keywords with aliases for supported node types, such as ``URI`` (for ``IRI``) or with combinations of node types that will be understood by their own applications downstream, such as ``Nonliteral`` or ``BlankNodeOrIRI``.
- **Namespace prefix mappings**. As explained in the section :ref:`cli_generate`, the :term:`Compact IRI`\s can be expanded into full :term:`IRI`\s by replacing the short prefix with the full IRI of the namespace. The default configuration settings provide a starter set of prefix mappings for frequently used namespaces. This list can be customized with locally defined namespaces or with namespaces listed in services such as `prefix.cc <http://prefix.cc/'_ or `Linked Open Vocabularies <https://lov.linkeddata.es/dataset/lov/vocabs>`_.

.. code-block:: yaml

    # dctap configuration file (in YAML format)
    default_shape_name: ":default"
    
    value_node_types:
    - iri
    - literal
    - bnode
    
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

The latest built-in settings can be found in the the YAML string variable ``DEFAULT_CONFIG_YAML`` in the source code file `config.py <https://github.com/dcmi/dctap-python/blob/main/dctap/config.py>`_.

