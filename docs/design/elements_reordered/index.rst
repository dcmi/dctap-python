.. _design_element_reordered:

The order of elements is normalized in output.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Regardless of how elements (columns) are ordered in a CSV, their order will be normalized in the text, JSON, and YAML outputs.

.. csv-table:: 
   :file: elementOrder.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :book
            shapeLabel:              Book
            Statement Constraint
                propertyID:          dcterms:creator
                valueShape:          :author

