.. _elem_valueConstraintType_mininclusive_maxinclusive:

MinInclusive / MaxInclusive
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A value constraint of type MinInclusive or MaxInclusive is used with a numeric value constraint (integer or float) to indicate the minimum or maximum of a numeric value. "Inclusive" means that the value provided will also match:

- MinInclusive means "greater than or equal to".
- MaxInclusive means "less than or equal to".

Note that because the columns for value constraint and value constraint type are not repeatable in the base DCTAP model, these value constraint types cannot be used to indicate ranges (eg, "-9 to -2"). Users who need to express value ranges should consider extending DCTAP, for example as follows:

- With a single column that uses an application-specific syntax for ranges (eg, "1-6").
- With two columns: one for MinInclusive and one for MaxInclusive.

.. csv-table:: 
   :file: minmaxinclusive.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :temperature
                valueConstraint      9
                valueConstraintType  mininclusive
            Statement Template
                propertyID           :temperature
                valueConstraint      -9
                valueConstraintType  mininclusive
            Statement Template
                propertyID           :temperature
                valueConstraint      12.2
                valueConstraintType  maxinclusive
            Statement Template
                propertyID           :temperature
                valueConstraint      -2
                valueConstraintType  maxinclusive
            Statement Template
                propertyID           :temperature
                valueConstraint      info@example.org
                valueConstraintType  maxinclusive

    WARNING [default/valueConstraint] Value constraint type is 'mininclusive', but 'info@example.org' is not numeric.

Note: 

- When viewed with the default text display (as above), non-numeric value constraints are flagged with warnings.
- When output as JSON, numeric values are coerced to integers or floats, as appropriate. Values that are not coercable are passed through as strings::

    {
        "shapes": [
            {
                "shapeID": "default",
                "statement_templates": [
                    {
                        "propertyID": ":temperature",
                        "valueConstraint": 9,
                        "valueConstraintType": "mininclusive"
                    },
                    {
                        "propertyID": ":temperature",
                        "valueConstraint": 12.2,
                        "valueConstraintType": "maxinclusive"
                    },
                    {
                        "propertyID": ":temperature",
                        "valueConstraint": "info@example.org",
                        "valueConstraintType": "maxinclusive"
                    }
                ]
            }
        ]
    }
