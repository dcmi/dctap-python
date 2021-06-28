.. _design_elements_lowercased:

Elements are normalized to lowercase.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements names (column headers) are normalized to lowercase. Dashes and underscores are removed.

.. csv-table::
   :file: headers.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :book
            Statement Constraint
                propertyID:          dcterms:date
                valueNodeType:       literal
