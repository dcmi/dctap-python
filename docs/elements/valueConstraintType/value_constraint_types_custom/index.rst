.. _elem_valueConstraintType_custom:

Custom value constraint types
.............................

The built-in value constraint types are intended only as examples. Implementers are encouraged to define their own types. If a **valueConstraintType** other than the four built-in types is provided --- in the following example, a hypothetical type **markdown** --- **dctap** will simply pass the value through to the output, where any consuming applications will be responsible for processing the type correctly.

.. csv-table:: 
   :file: valueConstraintType_markdown.csv
   :header-rows: 1

is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :tutorial
                valueConstraint      click [here](https://sphinx-rtd-tutorial.readthedocs.io)
                valueConstraintType  markdown
