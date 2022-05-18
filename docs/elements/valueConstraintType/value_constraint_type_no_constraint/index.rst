.. _elem_valueConstraintType_no_valueConstraint:

Value constraint types with no value constraints
................................................

Because the value constraint type is intended to provide a context for interpreting a value constraint, a value constraint type means nothing in the absence of a value constraint. If a value is provided for **valueConstraintType** but not for **valueConstraint**, a warning will be emitted.

.. csv-table:: 
   :file: valueConstraintType_with_no_valueConstraint.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :securityLevel
                valueConstraintType  picklist

    WARNING [default/valueConstraint] Value constraint type ('picklist') but no value constraint.
