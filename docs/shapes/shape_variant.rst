Declared in a statement row
"""""""""""""""""""""""""""

Shape IDs can be specified on the same row as a statement.

The `csv2shex` parser considers the first shape encountered in a CSV file to be the 'start' shape.

.. csv-table:: 
   :file: ../basics/shape_variant.csv
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

The value of `shapeLabel` is taken from the row where a new `shapeID` is first encountered. In other words, subsequent labels will simply be ignored. The following CSV is therefore interpreted as shown above:

.. csv-table:: 
   :file: ../basics/shape_variant2.csv
   :header-rows: 1
