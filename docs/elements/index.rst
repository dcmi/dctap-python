.. _elements:

DCTAP Elements
--------------

There are three types of :term:`DCTAP Element`\s: 

- :term:`Statement Constraint` elements, which enumerate constraints on property-value pairs (aka :term:`Statement`\s) in :term:`Instance Data`.

- :term:`Shape` elements, which enumerate characteristics of a a set of Statement Constraints about a :term:`Description` in :term:`Instance Data` (ie, a set of :term:`Statement`\s about exactly one :term:`Entity`, or Resource, in the real world.

- the ``note`` element, which is a simple annotation that can apply either to a Shape or to a Statement Constraint, according to context.

Minimal application profile
...........................

In the DCTAP model, the simplest possible application profile consists of just one :term:`Statement Constraint` in the context of one :term:`Shape`.

A Statement Constraint has, at a minimum, one ``propertyID`` element, and the existence of a Shape can be inferred, so in practical terms, the simplest possible application profile is a list of just one property.

Note that if a shape identifier is not explicitly assigned in a CSV, a default identifier will be assigned. (This is discussed in the the section :ref:`elem_shapeID`.) In "shape-less" applications, this shape identifier can simply be ignored.

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

Statement Constraint elements
.............................

There are nine Statement Constraint elements, of which the ``propertyID`` element alone is required.

.. toctree::

   propertyID/index
   mandrepeat/index
   valueNodeType/index
   valueDataType/index
   valueConstraintType/index
   valueShape/index

Shape elements
..............

There are two Shape elements, of which only ``shapeID`` is required (but can be assigned by default).

.. toctree::

   shapeID/index

Annotation elements
...................

The remaining element, ``note``, can be used to annotate either a Shape or a Statement Constraint, depending on context. 

.. toctree::

   note/index

Inasmuch as ``propertyLabel`` and ``shapeLabel`` are simply annotations, they may be considered as part of this category but are presented above in the context of Statement Constraints and Shapes.
