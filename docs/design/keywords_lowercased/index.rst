.. _design_keywords_lowercased:

Keywords are normalized to lowercase.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Picklist values are normalized to lowercase. For example, "LITERAL", "Literal", and "lITERAL" are normalized to "literal", while "Picklist", "PICKLIST", and "pICKLIST" are normalized to "picklist".

.. csv-table::
   :file: headers.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
    Shape
        shapeID:                 default
        Statement Template 
            propertyID:          dc:subject
            valueNodeType:       literal
            valueConstraint:     ['Kish', 'Uruk', 'Nuzi']
            valueConstraintType: picklist
        Statement Template
            propertyID:          dc:subject
            valueNodeType:       literal
            valueConstraint:     ['Kish', 'Uruk', 'Nuzi']
            valueConstraintType: picklist
        Statement Template
            propertyID:          dc:subject
            valueNodeType:       literal
            valueConstraint:     ['Kish', 'Uruk', 'Nuzi']
            valueConstraintType: picklist
