.. _elements:

Statement Constraint elements
-----------------------------

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
   :file: propertyID_only.csv
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

   propertyID/index
   propertyLabel/index
   mandrepeat/index
   valueConstraintType/index
   valueDataType/index
   valueNodeType/index
   valueShape/index

Shape elements
--------------

.. toctree::

   shapeID/index
   shapeLabel/index

Annotation element
------------------

.. toctree::

   note/index
