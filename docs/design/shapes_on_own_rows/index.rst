.. _shapes_on_own_rows:

Shapes may be declared on their own rows.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Shapes elements may be placed on their own rows. For example, given the following configuration file settings:

    extra_shape_elements:
    - "closed"
    - "start"

A CSV where shape elements are set on their own row:

.. csv-table::
   :file: shapes_on_own_rows.csv
   :header-rows: 1

Is interpreted as::

