.. _elements:

DCTAP Elements
--------------

There are three types of :term:`DCTAP Element`\s: 

- :term:`Statement Template` elements, which express constraints on property-value pairs (aka :term:`Statement`\s) in :term:`Instance Data`.

- :term:`Shape` elements, which enumerate characteristics of a a set of Statement Templates about a :term:`Description` in :term:`Instance Data` (ie, a set of :term:`Statement`\s about exactly one :term:`Entity`, or Resource, in the real world.

- the **note** element, which is a simple annotation that can apply either to a Shape or to a Statement Template, according to context.

Statement Template elements
...........................

There are nine Statement Template elements, of which the **propertyID** element alone is required.

.. toctree::
   :maxdepth: 3

   propertyID/index
   mandrepeat/index
   valueNodeType/index
   valueDataType/index
   valueConstraintType/index
   valueShape/index
   note/index

Shape elements
..............

There are two Shape elements. If the **shapeID** element is not used in a given DCTAP instance, it will be assigned a default value (which can be customized in the config file - see :ref:`default_shape_name`).

.. toctree::

   shapeID/index

