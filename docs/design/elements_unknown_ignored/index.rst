.. _design_elements_unknown_ignored:

Non-DCTAP elements are ignored unless configured.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Columns in a CSV that are not part of the DCTAP model are not automatically passed through to text, YAML, or JSON output because unrecognized elements, in principle, bear an undefined relationship to :term:`Shape`\s and :term:`Statement Constraint`\s. 

.. csv-table::
   :file: unknownElement.csv
   :header-rows: 1

Interpreted (with warnings enabled) as::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          dcterms:creator

    WARNING [csv/header] Non-DCTAP element 'Status' not configured as extra element.

Users wishing to use columns in their CSV that are not part of the DCTAP model, for example to specify that a shape is "closed" or to specify "severity" of validation errors, can generate a configuration file (see section :ref:`cli_init`) and list their extra column headers in the configuration file under the sections "extra_shape_elements" or "extra_statement_constraint_elements". This will ensure that the extra columns will be passed through to the text, JSON, and YAML outputs.

For example, if the configuration file includes::
    
    extra_statement_constraint_elements:
    - Status

The text output, intended as an aid in debugging, includes the extra element but marks it as "extra" with brackets::

    DCTAP instance
        Shape
            shapeID:                 default
            Statement Constraint
                propertyID:          dcterms:creator
                [Status]:            ignotus
        
The JSON (or YAML) output includes the extra element "as is"::

    {
        "shapes": [
            {
                "shapeID": "default",
                "statement_constraints": [
                    {
                        "propertyID": "dcterms:creator",
                        "Status": "ignotus"
                    }
                ]
            }
        ]
    }
