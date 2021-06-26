.. _elem_valueConstraintType:

valueConstraint / valueConstraintType
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A value constraint (``valueConstraint``) constrains
the value associated with a property in specific ways
according to its type (``valueConstraintType``).
A value constraint type may define a specific
interpretation of a value constraint or trigger specific 
techniques for processing the value constraint in an 
application downstream.

When a value constraint is provided without a value
constraint type, it is treated as a plain literal (unless
``valueNodeType`` is "IRI" or "BNode"). Typically, this is
intended to close the set of possible values to one
specific value and no others. In the following example,
the value expected to be found with the property
``:securityLevel`` is "Confidential" (and no other).

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
the value as a list of literal values as delimited by 
whitespace.

.. csv-table:: 
   :file: valueConstraint_with_type.csv
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

Because the value constraint type is intended to provide
a context for interpreting a value constraint, the value
constraint type means nothing in the absence of a value
constraint. If a value is provided for
``valueConstraintType`` but not for ``valueConstraint``,
a warning will be emitted.

The ``valueConstraintType`` element is intended to serve
as a sort of extension point for implementers of the
DCTAP model. As proof of concept, four commonly used
value constraint types are supported here:

.. toctree::
   :maxdepth: 1

   Picklist/index
   Pattern/index
   IRIStem/index
   LanguageTag/index
