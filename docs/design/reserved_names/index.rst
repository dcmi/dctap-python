.. _design_reserved_names:

Some element names are not allowed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some keywords may not be used as names of elements (i.e., of CSV column headers):

- "state_list"
- "shape_warns"
- "state_warns"
- "shape_extras"
- "state_extras"

Note that in processing headers, the module ignores case, certain punctuation (dashes and understores), and whitespace, so none of the following variants of "state_list" may be used as element names (see :ref:`design_element_names`):

- "SC List"
- "SC-List"
- "SCLIST"
