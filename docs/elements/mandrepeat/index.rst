.. _elem_mandrepeat:

mandatory and repeatable
^^^^^^^^^^^^^^^^^^^^^^^^

In the basic DCTAP model, the expected
cardinality of a property can be expressed
with the cardinality elements ``mandatory``
and ``repeatable``. These elements take 
Boolean values that express "true" or "false"
in one of two supported ways:

- The keywords ``true`` and ``false``
  (case-insensitive).
- The integers ``0`` and ``1``.

Any other value for either element will have 
no effect on the default of ``false`` for 
each element.

.. csv-table:: 
   :file: mandrepeat.csv
   :header-rows: 1

This is interpreted as::

.. csv-table:: 
   :file: ../normalizations/mandrepeat2.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:              :default
            Statement Constraint
                propertyID:       dc:creator
                repeatable:       X
            Statement Constraint
                propertyID:       dc:date
                mandatory:        Y
    DCTAP instance
        Shape
            shapeID:              :default
            Statement Constraint
                propertyID:       dc:subject
                mandatory:        Y
                repeatable:       N

=========== =========== ===== =====
 mandatory/repeatable     min/max
----------------------- -----------
mand        repeat      min   max
=========== =========== ===== =====
False       False       0     1
True        False       1     1
False       True        0     -1
True        True        1     -1
=========== =========== ===== =====

