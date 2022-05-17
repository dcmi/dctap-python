.. _element_aliases:

Element Name Aliases
....................

If desired, the names of :term:`DCTAP Element`\s, aka CSV column headers, can be customized in a configuration file by editing the "element_aliases" section. The built-in configuration defaults include, as an example, some shortened names that can be used to minimize the horizontal length of CSV rows. Alternatively, users might want to create aliases for headers in other languages. Note that for aliases, case, dashes, and underscores will be ignored, but the canonical element names to which they map must exactly match those presented in the section :ref:`elements`. Aliases will be expanded to the canonical element names in text, JSON, and YAML output. For example, if the configuration file specifies::

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
