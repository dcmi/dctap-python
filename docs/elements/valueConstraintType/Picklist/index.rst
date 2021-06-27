.. _elem_valueConstraintType_picklist:

Picklists of literals
^^^^^^^^^^^^^^^^^^^^^

Value constraints of type Picklist are parsed on 
whitespace into lists of literals.

Note:

- A literal with no whitespace is parsed into a list with just one literal.
- More complex picklists

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

Note that picklists with items that themselves have spaces, or are intended to
be separated by commas, may need to be parsed differently, in which case the
raw values could be passed through without a value constraint type of Picklist
for further processing by another program downstream.

The following example yields a mangled list if parsed as a Picklist (here
defined), but if no value constraint type is given, the value is left
untouched as a single string (in JSON: "reddish brown, greenish yellow, bluish
green").

.. csv-table:: 
   :file: picklist_with_commas.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :color
                valueConstraint:     ['reddish', 'brown,', 'greenish', 'yellow,', 'bluish', 'green']
                valueConstraintType: picklist
            Statement Constraint
                propertyID:          :hue
                valueConstraint:     reddish brown, greenish yellow, bluish green

A program that imports and builds on ``dctap`` could define its own
value constraint type, for example, CSPicklist (for comma-separated 
picklist), with an appropriate parser.
