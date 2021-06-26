.. _elem_shapeID:

shapeID
^^^^^^^

In the DCTAP model, all :term:`Statement Constraint`\s
are seen as grouped into :term:`Shape`\s, where a Shape
is about a :term:`Description` in :term:`Instance Data`
--- a set of statements about just one :term:`Entity` in
the real world.

If no ``shapeID`` is provided, a default shape identifier
will be assigned (":default"). A different default shape
identifier may be configured, as described in the section
:ref:`config`. For example:

.. csv-table::
   :file: shapeID.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:creator
            Statement Constraint
                propertyID:          dcterms:date

Users with metadata about a single :term:`Entity`, or
whose downstream applications do not make use of shapes,
can safely ignore this default identifier.

In RDF validation languages that support shapes, shapes are
typically identified with IRIs, so a warning will be emitted
if a shape identifier, on a superficial inspection, does not
look like an IRI.

.. csv-table::
   :file: shapeID_non_iri.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 book
            Statement Constraint
                propertyID:          dcterms:creator

    WARNING [book/shapeID] 'book' is not an IRI or Compact IRI.

Note that if a shape identifier is not provided for the first
rows processed but is provided for rows processed thereafter,
only the shape identifier for the first statement constraints will
be the default.

.. csv-table::
   :file: shapeID_default_then_named.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:creator
            Statement Constraint
                propertyID:          dcterms:date
        Shape
            shapeID:                 :author
            Statement Constraint
                propertyID:          foaf:name

