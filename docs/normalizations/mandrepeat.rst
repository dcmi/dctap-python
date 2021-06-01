mandatory and repeatable
^^^^^^^^^^^^^^^^^^^^^^^^

The cardinality elements `mandatory` ("mandatory") and `repeatable` ("repeatable") are both by default False. Specifying any value for either element makes that element True.

.. csv-table:: 
   :file: ../normalizations/mandrepeat.csv
   :header-rows: 1

This is interpreted as::

    DCTAP
        Shape
            shapeID: @default
            start: True
            Statement
                propertyID: dc:creator
                mandatory: False
                repeatable: True
            Statement
                propertyID: dc:date
                mandatory: True
                repeatable: False

Note that string values such as "No", "N", "n", "0", or "False" will be interpreted as True.

.. csv-table:: 
   :file: ../normalizations/mandrepeat2.csv
   :header-rows: 1

This is interpreted as::

    DCTAP
        Shape
            shapeID: @default
            start: True
            Statement
                propertyID: dc:subject
                mandatory: True
                repeatable: True
