.. _elem_valueConstraintType_picklist:

Picklist
^^^^^^^^

Value constraints of type "Picklist" are split into lists of literals (strings) by using the :ref:`picklist_item_separator`, by default whitespace. Lists are rendered in the text display as quoted strings, separated by commas and enclosed in square brackets, and in the JSON and YAML outputs as list objects.

In the following example:
- In the absence of valueConstraintType "picklist", "red blue green" is a string value.
- With valueConstraintType "picklist", "red blue green" is parsed on whitespace into a list.
- With valueConstraintType "picklist", "yellow" is parsed on whitespace into a list with a single item.

.. csv-table:: 
   :file: picklist.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :color
                valueConstraint      red blue green
            Statement Template
                propertyID           :color
                valueConstraint      ['red', 'blue', 'green']
                valueConstraintType  picklist
            Statement Template
                propertyID           :color
                valueConstraint      ['yellow']
                valueConstraintType  picklist

If **dctap** is configured to use a comma as the :ref:`picklist_item_separator`, the CSV

.. csv-table:: 
   :file: picklist_with_commas.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :color
                valueConstraint      ['reddish brown', 'greenish yellow', 'bluish green']
                valueConstraintType  picklist
