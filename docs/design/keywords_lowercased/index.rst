.. _design_elements_lowercased:

Keyword values are normalized to lowercase.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Keyword values are normalized to lowercase. For example, "LITERAL" and "Literal" are both normalized to "literal".

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
