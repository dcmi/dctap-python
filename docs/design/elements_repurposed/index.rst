.. _elements_repurposed:

Elements belong either to shapes or to statement templates, not both.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A given element is defined either as an element of a shape or an element of a statement template. At one's own risk, one can configure a statement constraint element as an "extra shape element" (or vice versa), for example with::

    extra_shape_elements:
    - "note"

However, the results may be unexpected. The CSV:

.. csv-table::
   :file: elements_repurposed.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  book
            [note]                   Note on a Shape
            Statement Template
                propertyID           dc:creator
                note                 Note on a Statement Template
        Shape
            shapeID                  author
            [note]                   Where does this note belong?
            Statement Template
                propertyID           foaf:name
                note                 Where does this note belong?

This ambiguity could be solved simply by coining an extra element, eg **shapeNote**::

    extra_shape_elements:
    - "shapeNote"
