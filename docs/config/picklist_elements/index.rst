.. _picklist_elements:

Picklist elements
.................

Some statement constraint elements can be configured as picklist elements. Cell values of picklist elements are split into lists of multiple values on the basis of a configurable :ref:`picklist_item_separator`. As its name implies, a picklist is a set of choices, as in "'blue' or 'yellow'" (not: "'blue' 

### These can take multiple values - eg: "this that" ("this" or "that").
### Values are separated by configurable picklist item separator (see below).
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
