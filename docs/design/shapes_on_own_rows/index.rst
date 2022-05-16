.. _shapes_on_own_rows:

Shapes may be declared on separate rows.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shapes, if declared on a row separately from statement templates, will apply to all subsequent statement templates - until a new **shapeID** is encountered. For example, given the following configuration file settings:

    extra_shape_elements:
    - "closed"
    - "start"

The CSV:

.. csv-table::
   :file: shapes_on_own_rows.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  book
            [closed]                 True
            [start]                  True
            Statement Template
                propertyID           dc:creator
                valueNodeType        uri
            Statement Template
                propertyID           dc:subject
                valueNodeType        literal
        Shape
            shapeID                  author
            Statement Template
                propertyID           foaf:name
                valueNodeType        literal

