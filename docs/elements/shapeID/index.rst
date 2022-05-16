.. _elem_shapeID:

shapeID / shapeLabel
^^^^^^^^^^^^^^^^^^^^

In the DCTAP model, all :term:`Statement Template`\s are seen as grouped into :term:`Shape`\s, where a Shape is about a :term:`Description` in :term:`Instance Data` --- a set of statements about just one :term:`Entity` in the real world.

A shape identifier is typically a plain :term:`Literal` or an :term:`IRI`.

If no **shapeID** is provided in the CSV or in a configuration file (see :ref:`config`), a default shape identifier will be assigned ("default"). A different default shape identifier may be configured, as described in the section :ref:`config`. For example:

.. csv-table::
   :file: shapeID.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dcterms:creator
            Statement Template
                propertyID           dcterms:date

Users with metadata about a single :term:`Entity`, or whose downstream applications do not make use of shapes, can safely ignore this default identifier.

A **shapeID**, once declared, will apply to any immediately subsequent rows where the **shapeID** is left blank. However, a shape ID may be declared explicitly for any or for every row. When shape IDs are explicitly declared, they can be presented in any arbitrary sequence without compromising their proper grouping as shapes. Declaring shape IDs explicitly makes it possible to combine statement templates from multiple sources without regard for their sequential order.

.. csv-table::
   :file: shapeID_repeated.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  :book
            Statement Template
                propertyID           dcterms:creator
            Statement Template
                propertyID           dcterms:date
            Statement Template
                propertyID           dcterms:language
        Shape
            shapeID                  :author
            Statement Template
                propertyID           foaf:name

If a shape identifier is not provided for the first rows processed but is provided for rows processed thereafter, only the shape identifier for the first statement templates will be the default.

.. csv-table::
   :file: shapeID_default_then_named.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dcterms:creator
            Statement Template
                propertyID           dcterms:date
        Shape
            shapeID                  :author
            Statement Template
                propertyID           foaf:name

Shapes can also have labels for use in displays and documentation.

.. csv-table:: 
   :file: shapeLabel.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  :book
            shapeLabel               Book
            Statement Template
                propertyID           dcterms:creator

Note that a shape label does not function as a shape identifier. If no value is provided for **shapeID** it will be assigned a (configurable) default. Only the assignment of a new **shapeID** will trigger the creation of a new shape. In the example below, the second **shapeLabel** ("Libro") is simply ignored.

.. csv-table:: 
   :file: shapeLabel_no_shapeID.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            shapeLabel               Book
            Statement Template
                propertyID           dcterms:creator
            Statement Template
                propertyID           dcterms:creator
