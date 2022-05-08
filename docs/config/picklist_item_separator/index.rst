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

Note, however, that because columns in CSVs are, by definition, separated by commas, a value with an embedded comma, as above, must be enclosed in quotes. This what a CSV with two columns would look like on disk::

    propertyID,valueNodeType
    "dc:creator,foaf:maker",iri

Note, also, that a column can be either a regular column or a picklist column, not both - ie, all cells in that column will be treated either as single values or as lists. In the following table:

.. csv-table::
   :file: propertyID_as_picklist_with_commas2.csv
   :header-rows: 1

the value "dc:date" is treated as the single item in a list of values::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          ['dc:creator', 'foaf:maker']
            Statement Constraint
                propertyID:          ['dc:date']

