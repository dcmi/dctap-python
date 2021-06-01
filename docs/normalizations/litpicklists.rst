Picklists of literals
^^^^^^^^^^^^^^^^^^^^^

Constraint values of constraint type `LitPicklist` are interpreted as lists.

.. csv-table:: 
   :file: ../normalizations/litpicklists.csv
   :header-rows: 1

This is interpreted as::

    DCAP
        Shape
            shapeID: :book
            start: True
            Statement
                propertyID: :color
                constraint_value: ['red', 'green', 'yellow']
                constraint_type: LitPicklist
            Statement
                propertyID: :color
                constraint_value: ['red']
                constraint_type: LitPicklist
