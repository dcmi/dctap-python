.. _element_aliases:

Element Name Aliases
....................


By default, some shortened names can be used to minimize the horizontal length of CSV rows. Alternatively, users might want to create aliases for headers in other languages. Note that for aliases, case, dashes, and underscores will be ignored, but the canonical element names to which they map must exactly match those presented in the section :ref:`elements`. Aliases will be expanded to the canonical element names in text, JSON, and YAML output. For example, if the configuration file specifies.

The column headers of a CSV can be customized as follows by defining aliases::

    element_aliases:
        "mand": "mandatory"
        "rep": "repeatable"

Then the following table:

.. csv-table::
   :file: element_aliases.csv
   :header-rows: 1

Is interpreted as::

    DCTAP instance
        Shape
            shapeID                  :book
            Statement Template  
                propertyID           dc:creator
                mandatory            True
                repeatable           False

Aliases can be used for translations of CSV headers into other languages.
