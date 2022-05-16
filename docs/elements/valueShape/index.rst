.. _elem_valueShape:

valueShape
^^^^^^^^^^

By specifing the :term:`Shape` to which the :term:`Description` of the resource represented by the :term:`Value` --- ie, the object of a :term:`Statement` in the :term:`Instance Data` --- is expected to conform, the **valueShape** element connects the shapes of a profile. 

A value shape identifier may be a literal, blank node, or IRI, so no checks are performed on the value of this element.

The example below says:

- A book, as described according to the ":book" shape, has a creator.
- The creator of the book must be described in accordance with the ":person" shape.
- The ":person" shape says that the description of a person must include their name.

.. csv-table:: 
   :file: shape_referenced.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID               :book
            Statement Template
                propertyID        dct:creator
                valueShape        :person
        Shape
            shapeID               :person
            Statement Template
                propertyID        foaf:name

