.. _empty_rows_ignored:

Empty rows are ignored.
^^^^^^^^^^^^^^^^^^^^^^^

For the purposes of **dctap**, a row is "empty" if it does not have a value either for **shapeID** or for **propertyID**.

The CSV:

.. csv-table::
   :file: empty_rows_ignored.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  book
            Statement Template
                propertyID           dc:creator
                valueNodeType        uri
            Statement Template
                propertyID           dc:date
                valueNodeType        literal
