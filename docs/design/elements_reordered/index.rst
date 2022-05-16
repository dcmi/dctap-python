.. _design_element_reordered:

The sequence of elements is normalized.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to improve the consistency and readability of results, he order of :term:`DCTAP Element`\s will be normalized in text, JSON, and YAML outputs irrespective of their sequence in a CSV, 

.. csv-table:: 
   :file: elementOrder.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  :book
            shapeLabel               Book
            Statement Template
                propertyID           dcterms:creator
                valueShape           :author

