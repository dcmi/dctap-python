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
   ../MinInclusive_MaxInclusive/index
   ../MinLength_MaxLength/index

Recall that the element :ref:`elem_valueDataType` is used for general datatypes of literal values, such as "string" and "date". The element :ref:`elem_valueConstraintType` is used for more specific or rarely used types of value. While every imaginable value constraint type could, in principle, have its own column in a tabular application profile, the resulting tables would be overly wide and this specification would be more longer and difficult to use. Pairing value constraint types with value constraints in just two columns helps keep tabular profiles more compact and concise.
