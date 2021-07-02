.. _elem_valueConstraintType_picklist:

Picklist
^^^^^^^^

Value constraints of type "Picklist" are split on whitespace into lists of literals (strings).

These lists are rendered in the text display as quoted strings, separated by commas and enclosed in square brackets. They are rendered in the JSON and YAML outputs not as strings, but as list objects.

A string with no whitespace is parsed into a list with just one string.

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

Note that lists with items that themselves include spaces, or are intended to be parsed not by whitespace but by commas, may need to be handled differently. In such a case the value of the element --- spaces and commas included --- could be passed through "as is" for further processing by another program downstream.

The following example shows a list that is mangled if parsed as a Picklist. However, if no value constraint type is given, the value is left untouched as a single string (in JSON: "reddish brown, greenish yellow, bluish green").

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

A program that imports and builds on **dctap** might want to define its own value constraint type, for example, CSPicklist (for comma-separated picklist), with an appropriate parser.
