.. _elem_valueConstraintType:

valueConstraint / valueConstraintType
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A value constraint (**valueConstraint**) constrains the value associated with a property in specific ways according to its type (**valueConstraintType**). A value constraint type may define a specific interpretation of a value constraint or trigger specific techniques for processing the value constraint in an application downstream.


Value constraints with no value constraint types
................................................

When a value constraint is provided without a value constraint type, it is treated as a plain literal (unless **valueNodeType** is "IRI" or "BNode"). Typically, this is intended to close the set of possible values to one specific value and no others. In the following example, the value expected to be found with the property **:securityLevel** is "Confidential" (and no other).

.. csv-table:: 
   :file: valueConstraint.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          :securityLevel
                valueConstraint:     Confidential

Built-in value constraint types
...............................

The **valueConstraintType** element is intended to serve as a sort of extension point for implementers of the DCTAP model. As proof of concept, four commonly used value constraint types are supported here:

.. toctree::
   :maxdepth: 3

   Picklist/index
   Pattern/index
   IRIStem/index
   LanguageTag/index

In contrast to the :ref:`elem_valueDataType`, which mark the datatype of literals in a form carried by :term:`Instance Data`, the value constraint type is intended to be used to trigger specific algorithms for transforming the values of a CSV cells, which are by definition only ever strings, into lists, regular expressions, or other data structures of the type used in programming.

For example, providing the built-in value constraint type "Picklist" tells a processor to split a string value on its embedded whitespace into separate literals and present them as a list.

.. csv-table:: 
   :file: valueConstraint_with_type.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          :securityLevel
                valueConstraint:     ['Public', 'Confidential']
                valueConstraintType: picklist

Note that a value constraint that contains commas --- and is properly formatted with quotation marks in a CSV --- will be treated as a single value with commas:

.. csv-table:: 
   :file: valueConstraint_with_commas.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          :creator
                valueConstraint:     one, two, three

Because the value constraint type is intended to provide a context for interpreting a value constraint, the value constraint type means nothing in the absence of a value constraint. If a value is provided for **valueConstraintType** but not for **valueConstraint**, a warning will be emitted.

Custom value constraint types
.............................

The built-in value constraint types are intended only as examples. Implementers are encouraged to define their own types. Given sufficient demand, popular extensions to the set of value constraints may be incorporated into future extensions of DCTAP.
