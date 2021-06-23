.. _elem_valueConstraintType_pattern:

Pattern
^^^^^^^

A value constraint type of Pattern means that the corresponding value constraint it to be interpreted as a (Python) regular expression. If value constraints are empty or malformed as regular expressions they will be passed through, untouched, to text, JSON, and YAML output, but the anomalies will be flagged with warnings.

.. csv-table:: 
   :file: pattern.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :ex1
            Statement Constraint
                propertyID:          :status
                valueConstraint:     approved_*
                valueConstraintType: pattern
        Shape
            shapeID:                 :ex2
            Statement Constraint
                propertyID:          :status
                valueConstraintType: pattern
        Shape
            shapeID:                 :ex3
            Statement Constraint
                propertyID:          :status
                valueConstraint:     approved_(*
                valueConstraintType: pattern
        Shape
            shapeID:                 :ex4
            Statement Constraint
                propertyID:          :status
                valueConstraint:     /approved_*/
                valueConstraintType: pattern
        Shape
            shapeID:                 :ex5
            Statement Constraint
                propertyID:          :status
                valueConstraint:     ^2020 August
                valueConstraintType: pattern

    WARNING [:ex2/valueConstraint] Value constraint type is 'pattern', but value constraint is empty.
    WARNING [:ex3/valueConstraint] Value constraint type is 'pattern', but 'approved_(*' is not a valid regular expression.
