Statement Constraints
---------------------

A Statement Constraint has, at a minimum, one
`propertyID` element. A DCTAP Instance consists, at a
minimum, of at least one Statement Constraint. The 
simplest possible Application Profile, therefore, is a 
list of at least one property.

Note that A default shape identifier is
assigned if not provided in the CSV; more
about shapes below. In a "Shape-less"
application, this default shape identifier
can simply be ignored.

.. csv-table:: 
   :file: ../test_csvs/propertyID_only.csv
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

.. toctree::

   Statement_constraints_properties_can_have_labels.rst
   Statement_constraints_nodetypes_datatypes.rst
