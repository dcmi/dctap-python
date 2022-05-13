.. _picklist_elements:

Picklist elements
.................

Some statement template elements can be configured as picklist elements. Cell values of picklist elements are split into lists of multiple values on the basis of a configurable :ref:`picklist_item_separator`. As its name implies, a picklist is a set of choices, as in: "blue OR yellow" (not: "blue AND yellow"). Picklists may be used or interpreted differently in applications downstream of a DCTAP instance. The semantic implications of using picklist values with given elements in particular applications is out of scope for DCTAP.

There are two cases where a picklist may be used as the value of an element:

- When a **valueConstraintType** of "picklist" says that the value of a related **valueConstraint** (in the same row) should be treated as a picklist.
- When an element is configured as a picklist element - ie, all values in a given column are to be treated as picklists.

Note that the following types of statement template element cannot sensibly be configured for use with multiple values:

- Elements with numeric values: **min**, **max**
- Elements with Boolean values: **closed**, **start**, **mandatory**, **repeatable**

Elements used purely for annotation, such as **shapeLabel**, **propertyLabel**, and **note**, could in principle be configured for use with multiple values (eg, with labels in multiple languages). Note that a picklist of properties or values (eg, `dcterms:creator` or `foaf:maker` would not map onto a corresponding picklist of annotations (eg, "Creator" or "Maker").

To take the example **propertyID**, given:

.. csv-table::
   :file: propertyID_as_picklist.csv
   :header-rows: 1

The value of **propertyID** by default interpreted as having an (illegal) space, "dc:creator foaf:maker"::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Template
                propertyID:          dc:creator foaf:maker

But if **dctap** is so configured::

    picklist_elements:
    - propertyID

The value is interpreted as a list::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Template
                propertyID:          ['dc:creator', 'foaf:maker']


In addition to **propertyID**, the following elements can sensibly be configured for use with multiple values:

.. toctree::

   valueNodeType/index
   valueDataType/index
   valueShape/index
