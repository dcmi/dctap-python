.. _element_aliases:

Element Aliases
...............

The width of CSVs can be reduced by creating aliases for headers. For aliases, case, whitespace, and punctuation are ignored, but the canonical element names to which they map must exactly match those presented in the section :ref:`elements`. Aliases will be expanded to the canonical element names in text, JSON, and YAML output. For example, given the following configuration file ("dctap.yaml")::

    prefixes:
        ":":        "http://example.org/"
        "dc:":      "http://purl.org/dc/elements/1.1/"

    extra_element_aliases:
        "PropID": "propertyID"

The following table:

.. csv-table::
   :file: element_aliases.csv
   :header-rows: 1

Is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           dc:creator

Aliases can also be used for translations of CSV headers into other languages.
