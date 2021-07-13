.. _design_elements_unknown_ignored:

Non-DCTAP elements are ignored unless configured.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Columns in a CSV that are not part of the DCTAP model are not automatically passed through to text, YAML, or JSON output because unrecognized elements, in principle, bear an undefined relationship to :term:`Shape`\s and :term:`Statement Constraint`\s. 

.. csv-table::
   :file: unknownElement.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          dcterms:creator

Users wishing to use columns in their CSV that are not part of the DCTAP model, for example to specify that a shape is "closed" or to specify "severity" of validation errors, can generate a configuration file (see section :ref:`cli_init`) and list their extra column headers in the configuration file under the sections "extra_shape_elements" or "extra_statement_constraint_elements". This will of course not actually extend the DCTAP model itself, but it will ensure that the extra columns will be passed through to the text, JSON, and YAML outputs.

Users wishing to extend the DCTAP model for re-use by others can do so either by publishing a description of the extra elements or by creating an application in support of the extension. One way to do so would be to import **dctap** into their own Python and extending its functions and classes as needed. The developers of **dctap** would like to facilitate the sharing of such extensions, or even to incorporate popular elements into a future extension of the base model. Extensions can be proposed by opening an issue on the main `DCTAP repository <https://github.com/dcmi/dctap/issues>`_.
