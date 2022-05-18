.. _elem_valueConstraintType_builtins:

Built-in value constraint types
...............................

The **valueConstraintType** element is intended to serve as an extension point for implementers of the DCTAP model. As proof of concept, four commonly used value constraint types are supported by default:

.. toctree::
   :maxdepth: 3

   ../Picklist/index
   ../Pattern/index
   ../IRIStem/index
   ../LanguageTag/index

In contrast to the :ref:`elem_valueDataType`, which mark the datatype of literals in a form carried by :term:`Instance Data`, the value constraint type is intended to be used to trigger specific algorithms for transforming the values of a CSV cells, which are by definition only ever strings, into lists, regular expressions, or other data structures of the type used in programming.

Because the value constraint type is intended to provide a context for interpreting a value constraint, the value constraint type means nothing in the absence of a value constraint. If a value is provided for **valueConstraintType** but not for **valueConstraint**, a warning will be emitted.
