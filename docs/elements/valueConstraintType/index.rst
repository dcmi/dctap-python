.. _elem_valueConstraintType:

valueConstraint / valueConstraintType
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A value constraint (``valueConstraint``) can constrain
the value associated with a property in various ways
according to its type (``valueConstraintType``).

If a value constraint is a literal, and no type is
provided, the constraint value closes the set of possible
values to that specific literal and no others. In the
following example, the value expected to be found with
the property ``:securityLevel`` is "Confidential", and no
other literal value would match the :term:`Statement
Constraint`.

.. csv-table:: 
   :file: valueConstraint.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :securityLevel
                valueConstraint:     Confidential

Providing a constraint value of "picklist", however, 
tells the processor that the value constraint is to be 
treated in a specific way --- in this case, to parse
the value a list of literal values as delimited by 
whitespace.

.. csv-table:: 
   :file: valueConstraint.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :securityLevel
                valueConstraint:     ['Public', 'Confidential']
                valueConstraintType: picklist

Note that a value constraint that contains commas --- and is 
properly formatted with quotation marks in a CSV --- will be 
treated as a single value with commas:

.. csv-table:: 
   :file: valueConstraint_with_commas.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :creator
                valueConstraint:     one, two, three

Four value constraint types are currently supported:

.. toctree::
   :maxdepth: 1

   Picklist/index
   Pattern/index
   IRIStem/index
   LanguageTag/index
