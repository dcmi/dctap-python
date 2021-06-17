.. _elem_shapeLabel:

shapeLabel
^^^^^^^^^^

Shapes can have labels.

.. csv-table:: 
   :file: shapeLabel.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :book
            shapeLabel:              Book
            Statement Constraint
                propertyID:          dcterms:creator

Note that a shape label does not function as a 
shape identifier. If no value is provided for ``shapeID`` 
it will be assigned a (configurable) default. Only the 
assignment of a new ``shapeID`` will trigger the creation 
of a new shape. In the example below, the second ``shapeLabel``
("Libro") is simply ignored.

.. csv-table:: 
   :file: shapeLabel_no_shapeID.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            shapeLabel:              Book
            Statement Constraint
                propertyID:          dcterms:creator
            Statement Constraint
                propertyID:          dcterms:creator

