Minimal DCTAP instance
^^^^^^^^^^^^^^^^^^^^^^

The most minimal application profile simply provides a list of properties used.

.. csv-table:: 
   :file: ../basics/propid.csv
   :header-rows: 1

Interpreted as::

    DCTAP
        Shape
            shapeID: @default
            start: True
            Statement
                propertyID: dct:creator
            Statement
                propertyID: dct:title
            Statement
                propertyID: dct:publisher
            Statement
                propertyID: dct:date
