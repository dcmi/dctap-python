.. _elements:

DCTAP Elements
--------------

In the DCTAP Model, a Shape groups a set of Statement Templates, each of which describes one type of Statement in Instance Data about a specified Entity. Each of these two components (Shapes and Statement Templates) has its own (extensible) set of DCTAP Elements:

Statement Template elements
...........................

.. toctree::
   :maxdepth: 3

   propertyID/index.rst
   mandrepeat/index.rst
   valueNodeType/index.rst
   valueDataType/index.rst
   valueConstraintType/index.rst
   valueShape/index.rst
   note/index.rst

Shape elements
..............

There are two Shape elements. If the **shapeID** element is not used in a given DCTAP instance, it will be assigned a default value (which can be customized in the config file - see :ref:`default_shape_name`).

.. toctree::

   shapeID/index.rst

