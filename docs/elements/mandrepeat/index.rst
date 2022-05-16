.. _elem_mandrepeat:

mandatory / repeatable
^^^^^^^^^^^^^^^^^^^^^^

In the DCTAP model, the expected cardinality of a property can be expressed with the elements **mandatory** and **repeatable**. These elements take Boolean values that express "true" or "false" in one of two supported ways:

- The keywords **true** and **false** (case-insensitive).
- The integers **0** and **1**.

These supported Boolean values are handled in the following ways:

- normalized as the Boolean class instances True and False in the internal Python object. 
- normalized as true and false in the JSON and YAML outputs, 
- displayed as True and False in the compact text output.

Note that empty values (ie, strings of length zero) are simply interpreted as unspecified and are not assigned an explicit Boolean value.

.. csv-table:: 
   :file: mandrepeat.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dc:creator
                mandatory            True
                repeatable           False
            Statement Template
                propertyID           dc:date
                mandatory            False

Any other value for either element --- including an empty string for when the element is present but left blank --- has no effect on the default of **None** for each element and will be passed through as a string (or empty string) to the JSON and YAML output.

An empty string value will result in an element not being displayed at all in the compact text output; in the verbose text format, the value will be displayed as the default "None".

.. csv-table:: 
   :file: mandrepeat_warn_unsupported_values.csv
   :header-rows: 1

This is displayed as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dc:creator
                repeatable           N
            Statement Template
                propertyID           dc:date
                mandatory            Y

    WARNING [default/repeatable] 'N' is not a supported Boolean value.
    WARNING [default/mandatory] 'Y' is not a supported Boolean value.

The four possible combinations of **mandatory** with **repeatable** translate into the following minimum and maximum values when cardinality is expressed as a range (where "-1" means "many").

=========== =========== ===== =====
 mandatory/repeatable     min/max
----------------------- -----------
mand        repeat      min   max
=========== =========== ===== =====
False       False       0     1
True        False       1     1
False       True        0     -1
True        True        1     -1
=========== =========== ===== =====

Users of DCTAP in areas such as biology, where more expressive cardinality is required, may want to extend the model with such ranges.
