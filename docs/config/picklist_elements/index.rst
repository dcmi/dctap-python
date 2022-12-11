.. _picklist_elements:

Picklist Elements
.................

Some statement template elements can be configured as picklist elements. Cell values of picklist elements are split into lists of multiple values on the basis of a configurable :ref:`picklist_item_separator`. Value lists may be used or interpreted differently in applications downstream of a DCTAP instance. The semantic implications of using list values with given elements in particular applications is out of scope for DCTAP.

There are two cases where a list may be used as the value of an element:

- In the context of a specific statement constraint, a **valueConstraint** is provided together with a **valueConstraintType** of "picklist".
- An element has been declared in the config file as a picklist element - ie, all values in that given column are to be treated as lists.

Note that the following types of statement template element cannot sensibly be configured for use with multiple values:

- Elements with numeric values: **min**, **max**
- Elements with Boolean values: **closed**, **start**, **mandatory**, **repeatable**

Elements used purely for annotation, such as **shapeLabel**, **propertyLabel**, and **note**, could in principle be configured for use with multiple values (eg, with labels in multiple languages).

On the example of **propertyID**, given:

.. csv-table::
   :file: propertyID_as_list.csv
   :header-rows: 1

In the following example, the value of **propertyID** would by default be interpreted as including an (illegal) space::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dc:creator foaf:maker

However, if **dctap** were so configured::

    picklist_elements:
    - propertyID

The value would be interpreted as a list::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           ['dc:creator', 'foaf:maker']

Note that a column can be either a regular column or a list column, but not both - ie, all cells in a given column will be treated either as single values or as lists. In the following table:

.. csv-table::
   :file: propertyID_as_list_with_commas2.csv
   :header-rows: 1

the value "dc:date" is treated as an item a list that has just one value::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template   
                propertyID           ['dc:creator', 'foaf:maker']
            Statement Template   
                propertyID           ['dc:date']


