.. _list_item_separator:

List Item Separator
...................

The value of a list element, a string, is parsed into a list of substrings on the basis of a list item separator, by default a single space. This default separator can be changed to a different character, such as a comma or pipe (orbar). For example, the element **propertyID** can be configured as a list element with a non-default list item separator, such as a comma::

    list_elements:
    - propertyID
    list_item_separator: ','

In this case, a **propertyID** containing a comma, such as:

.. csv-table::
   :file: propertyID_as_list_with_commas.csv
   :header-rows: 1

would be parsed as a list with two values, as in the example shown in the section :ref:`list_elements`.

Note, however, that because columns in CSVs are, by definition, separated by commas, a value with an embedded comma, as above, must be enclosed in quotes. Exporting to CSV from an Excel spreadsheet yields a result such as the following, where the multiple values in cell A2 are enclosed in quotes::

    propertyID,valueNodeType
    "dc:creator,foaf:maker",iri

