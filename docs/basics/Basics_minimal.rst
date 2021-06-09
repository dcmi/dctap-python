Minimal DCTAP instance
^^^^^^^^^^^^^^^^^^^^^^

The most minimal application profile simply provides a list of properties used.
In a simple application, the default shape identifier could be ignored.

.. csv-table:: 
   :file: ../tests/propertyID_only.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
	Shape
	    shapeID: :default
	    Statement Constraint
		propertyID: dct:title
	    Statement Constraint
		propertyID: dct:publisher
	    Statement Constraint
		propertyID: dct:creator
	    Statement Constraint
		propertyID: dct:date
