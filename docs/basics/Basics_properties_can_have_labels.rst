Properties can have labels
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: 
   :file: ../tests/propertyID_plus_label.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
	Shape
	    shapeID: :default
	    Statement Constraint
		propertyID: dct:creator
		propertyLabel: Author
	    Statement Constraint
		propertyID: dct:title
		propertyLabel: Book title
	    Statement Constraint
		propertyID: dct:publisher
		propertyLabel: Publisher
	    Statement Constraint
		propertyID: dct:date
		propertyLabel: Publication date
