.. _design_elements_unknown_ignored:

Non-DCTAP elements are ignored.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Columns in a CSV that are not part of the DCTAP model are not passed through to text, YAML, or JSON output because unrecognized elements bear an undefined relationship to :term:`Shape`\s and :term:`Statement Constraint`\s. 

.. csv-table::
   :file: unknownElement.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:creator

Users wishing to extend the DCTAP model, for example with elements to specify that a shape is "closed" or to provide severity levels for validation errors, can import **dctap** into their own projects and add any elements required. The developers of **dctap** would like to facilitate the sharing of such extensions, or even to incorporate popular elements into a future extension of the base model. Additional elements can be proposed by opening an issue on the main `DCTAP repository <https://github.com/dcmi/dctap/issues>`_.
