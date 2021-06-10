Referenced as value shape
"""""""""""""""""""""""""

A statement may include a reference back to a shape to which the object value of a property must conform.

.. csv-table:: 
   :file: ../basics/shape_referenced.csv
   :header-rows: 1

Interpreted as::

    DCTAP
        Shape
            shapeID: :book
            start: True
            Statement
                propertyID: dct:creator
                shape_ref: @:person
        Shape
            shapeID: :person
            Statement
                propertyID: foaf:name

This means:

* A book, as described according to the `:book` shape, has a creator.
* The creator of the book must be described in accordance with the `:person` shape.
* The `:person` shape says that the description of a person must include their name.

Note that only the first shape is flagged as a 'start' shape.
