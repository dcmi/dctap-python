.. _design_elements_not_repeatable:

DCTAP elements are not repeatable.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements cannot be repeated, i.e., used as a header for more than one column in a CSV. This module ignores all but the last column with a given header.

.. csv-table:: 
   :file: element_repeated.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dc:creator
                note                 Typically, the person listed on the cover page.
