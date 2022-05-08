.. _picklist_elements:

Picklist elements
.................

Some statement constraint elements can be configured as picklist elements. Cell values of picklist elements are split into lists of multiple values on the basis of a configurable :ref:`picklist_item_separator`. As its name implies, a picklist is a set of choices, as in ``blue`` OR ``yellow`` (not: ``blue`` AND ``yellow``). Picklists may be used or interpreted differently in applications downstream of a DCTAP instance, so the semantic implications of using picklist values with given elements may differ from those presented here.

### Types of element that cannot be configured for multiple values:
### - Elements with numeric values: min, max
### - Elements with Boolean values: closed, start, mandatory, repeatable
### - Elements used purely for annotation: shapeLabel, propertyLabel, note
# picklist_elements:
# - propertyID
# - valueNodeType
# - valueDataType
# - valueShape

.. toctree::

   propertyID/index
   valueNodeType/index
   valueDataType/index
   valueShape/index
