Declared in a separate row
""""""""""""""""""""""""""

A shape can be identified and labeled on its own row. The shape will apply to all subsequent valid rows until a row with a different shape identifier is encountered. The `csv2shex` parser considers the first shape encountered in a CSV file to be the 'start' shape.

.. csv-table:: 
   :file: ../basics/shape.csv
   :header-rows: 1

Interpreted as::

    DCTAP
        Shape
            shapeID: :book
            start: True
            Statement
                propertyID: dct:creator
            Statement
                propertyID: dct:title
