Minimal DCTAP instance
^^^^^^^^^^^^^^^^^^^^^^

The most minimal application profile simply provides a list of properties used. A property must be one that has been defined previously in a vocabulary, preferably with an IRI to identify it; more about "preferably" below.

A default shape identifier is assigned if not provided in the CSV; more about shapes below. In a very basic application, the shape identifier can simply be ignored.

.. csv-table:: 
   :file: ../tests/propertyID_only.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
	Shape
	    shapeID: :default
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/title
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/publisher
	    Statement Constraint
		propertyID: https://schema.org/creator
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/date
