.. _picklist_item_separator:

Picklist item separator
.......................

By default, a picklist is parsed from the CSV string value by splitting substrings separated by a single space. This default separator can be changed to a different character, such as a comma or pipe (orbar).

**dctap** can be configured with a non-default picklist item separator, such as a comma::

    picklist_elements:
    - propertyID

    picklist_item_separator: ','

In this case, a **propertyID** containing a comma, such as:

.. csv-table::
   :file: propertyID_as_picklist_with_commas.csv
   :header-rows: 1

would be parsed as a list with two alternative values (the "picklist"), as in the example shown in section :ref:`picklist_elements`.

Note, however, that because columns in CSVs are, by definition, separated by commas, a value with an embedded comma, as above, must be enclosed in quotes. This is how the contents of such a CSV look on disk::

    propertyID,valueNodeType
    "dc:creator,dc:date",iri
