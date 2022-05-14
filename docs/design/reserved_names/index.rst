.. _design_reserved_names:

Some element names are not allowed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some keywords may not be used as names of elements (i.e., of CSV column headers):

- "csv"
- "st_list"
- "sh_warnings"
- "st_warnings"
- "extras"

Note that in processing headers, the module ignores case, certain punctuation (dashes and understores), and whitespace, so none of the following variants of "st_list" may be used as element names (see :ref:`design_element_names`):

- "SC List"
- "SC-List"
- "SCLIST"
