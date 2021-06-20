.. _elem_valueConstraintType_picklist:

Picklists of literals
^^^^^^^^^^^^^^^^^^^^^

Value constraints of type `Picklist` are parsed on 
whitespace into lists of literals.

Note that a literal with no whitespace is parsed into a 
list with just one literal.

.. csv-table:: 
   :file: picklist.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :color
                valueConstraint:     ['red', 'blue', 'green']
                valueConstraintType: picklist
            Statement Constraint
                propertyID:          :hue
                valueConstraint:     ['yellow']
                valueConstraintType: picklist
