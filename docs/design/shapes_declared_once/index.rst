.. _shapes_declared_once:

Shape elements are set just once.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Values for shape elements are set from the row where a new shape is first encountered. Shape element values asserted in subsequent rows are ignored. For example, given the following configuration file settings:

    extra_shape_elements:
    - "closed"
    - "start"

The CSV:

.. csv-table::
   :file: shapes_declared_once.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  book
            [start]                  True
            Statement Template
                propertyID           dc:creator
                valueNodeType        uri
            Statement Template
                propertyID           dc:date
                valueNodeType        literal
