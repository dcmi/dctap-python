.. _config:

Configuration
-------------

**dctap** has built-in defaults for configuration settings that are customizable by users by generating and editing configuration file as explained in the section :ref:`cli_init`. The latest built-in settings can be found in the YAML string variable **DEFAULT_CONFIG_YAML** in the source code file `defaults.py <https://github.com/dcmi/dctap-python/blob/main/dctap/defaults.py>`_.

Extra (non-DCTAP) elements
..........................

By default, **dctap** ignores elements that are not part of the DCTAP model. This is because **dctap** cannot know whether an extra column refers to a shape or to a statement constraint. As explained in the section :ref:`design_elements_unknown_ignored`, **dctap** can be configured to recognize extra elements as belonging either to a shape or to a statement constraint and thus pass them through to text, JSON, or YAML output. This can be done by generating a configuration file and adding the element names under the appropriate headings::

    extra_shape_elements:
    - closed
    - start

    extra_statement_constraint_elements:
    - min
    - max

Extra value node types
......................

Out of the box, DCTAP supports the three node types of the graph-based data model as defined in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#data-model>`_: IRI, literal, and blank node. These are represented in a :term:`DCTAP Instance` with "IRI", "Literal", and "BNode" as keywords for the element :ref:`elem_valueNodeType`. Users can extend this list of supported keywords with aliases for supported node types, such as "URI" (for "IRI") or with combinations of node types that will be understood by their own applications downstream, such as "Nonliteral"  or "BlankNodeOrIRI".

Namespace prefix mappings
.........................

As explained in the section :ref:`cli_generate`, the :term:`Compact IRI`\s can be expanded into full :term:`IRI`\s by replacing the short prefix with the full IRI of the namespace. The default configuration settings provide a starter set of prefix mappings for frequently used namespaces. This list can be customized with locally defined namespaces or with namespaces listed in services such as `prefix.cc <http://prefix.cc/'_ or `Linked Open Vocabularies <https://lov.linkeddata.es/dataset/lov/vocabs>`_.

Element name aliases
....................

If desired, the names of :term:`DCTAP Element`\s, aka CSV column headers, can be customized in a configuration file by editing the "element_aliases" section. The built-in configuration defaults include, as an example, some shortened names that can be used to minimize the horizontal length of CSV rows. Alternatively, users might want to create aliases for headers in other languages. Note that for aliases, case, dashes, and underscores will be ignored, but the canonical element names to which they map must exactly match those presented in the section :ref:`elements`. Aliases will be expanded to the canonical element names in text, JSON, and YAML output. For example, if the configuration file specifies::

    element_aliases:
    "mand": "mandatory"
    "rep": "repeatable"

Then the following table:

.. csv-table::
   :file: element_aliases.csv
   :header-rows: 1

Is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :book
            Statement Constraint
                propertyID:          dc:creator
                mandatory:           True
                repeatable:          False

Default shape name
..................

When shape identifiers are not provided in a CSV, a configurable default shape name is used (see section :ref:`elem_shapeID`).

Picklist item separator
.......................

By default, a picklist is parsed from the CSV string value by splitting substrings separated by a single space. This default separator can be changed to a different character, such as a comma or pipe (orbar).
