.. _elem_valueConstraintType_minlength_maxlength:

MinLength / MaxLength
^^^^^^^^^^^^^^^^^^^^^

A value constraint of type MinLength or MaxLength defines a minimum or maximum length of a string value:

- MinLength means a string is at least X characters long.
- MaxLength means a string no longer than X characters long.

Note that because the columns for value constraint and value constraint type are not repeatable in the base DCTAP model, these value constraint types cannot be used to indicate ranges (eg, "2 to 9"). Users who need to express value ranges should consider extending DCTAP, for example as follows:

- With a single column that uses an application-specific syntax for ranges (eg, "1-6").
- With two columns: one for MinInclusive and one for MaxInclusive.

.. csv-table:: 
   :file: minmaxlength.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :identifier
                valueConstraint      3
                valueConstraintType  minlength
            Statement Template
                propertyID           :identifier
                valueConstraint      3.1
                valueConstraintType  minlength
            Statement Template
                propertyID           :identifier
                valueConstraint      -10
                valueConstraintType  maxlength
            Statement Template
                propertyID           :identifier
                valueConstraint      info@example.org
                valueConstraintType  maxlength

    WARNING [default/valueConstraint] Value constraint type is 'minlength', but '3.1' is not an integer.
    WARNING [default/valueConstraint] Value constraint type is 'maxlength', but 'info@example.org' is not an integer.

Values of type MinLength or MaxLength must be integers. Note:

- String and float values trigger warnings but are passed through, untouched, as string values.
- Negative integers do not trigger warnings, though they may not make sense.
