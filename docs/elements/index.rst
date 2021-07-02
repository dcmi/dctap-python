.. _elements:

DCTAP Elements
--------------

There are three types of :term:`DCTAP Element`\s: 

- :term:`Statement Constraint` elements, which enumerate constraints on property-value pairs (aka :term:`Statement`\s) in :term:`Instance Data`.

- :term:`Shape` elements, which enumerate characteristics of a a set of Statement Constraints about a :term:`Description` in :term:`Instance Data` (ie, a set of :term:`Statement`\s about exactly one :term:`Entity`, or Resource, in the real world.

- the **note** element, which is a simple annotation that can apply either to a Shape or to a Statement Constraint, according to context.

Statement Constraint elements
.............................

There are nine Statement Constraint elements, of which the **propertyID** element alone is required.

.. toctree::

   propertyID/index
   mandrepeat/index
   valueNodeType/index
   valueDataType/index
   valueConstraintType/index
   valueShape/index

Shape elements
..............

There are two Shape elements, of which only **shapeID** is required (but can be assigned by default).

.. toctree::

   shapeID/index

Annotation elements
...................

The remaining element, **note**, can be used to annotate either a Shape or a Statement Constraint, depending on context. 

.. toctree::

   note/index

Inasmuch as **propertyLabel** and **shapeLabel** are simply annotations, they may be considered as part of this category but are presented above in the context of Statement Constraints and Shapes.
