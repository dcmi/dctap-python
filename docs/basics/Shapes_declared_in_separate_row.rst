Declared in a separate row
""""""""""""""""""""""""""

A shape can be identified and labeled on its own row. The shape will apply to all subsequent valid rows until a row with a different shape identifier is encountered. The `csv2shex` parser considers the first shape encountered in a CSV file to be the 'start' shape.

.. csv-table:: 
   :file: ../tests/shapeID_declared_in_separate_row.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID: :default
            Statement Constraint
                propertyID: dct:creator
            Statement Constraint
                propertyID: dct:title
