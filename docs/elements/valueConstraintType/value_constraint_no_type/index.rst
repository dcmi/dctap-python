.. _elem_valueConstraint_no_valueConstraintType:

Value constraints with no value constraint types
................................................

When a value constraint is provided without a value constraint type, it is treated as a plain literal (unless **valueNodeType** is "IRI" or "BNode"). Typically, this is intended to close the set of possible values to one specific value and no others. In the following example, the value expected to be found with the property **:securityLevel** is "Confidential" (and no other).

.. csv-table:: 
   :file: valueConstraint.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :securityLevel
                valueConstraint      Confidential

