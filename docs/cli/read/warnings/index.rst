.. _cli_subcommands_read_warnings:

View warnings generated
:::::::::::::::::::::::

As an aid for debugging, **dctap read --warnings** generates warnings for any obvious inconsistencies or errors found in the TAP.

Specific consistency checks are explained in the descriptions of individual :term:`DCTAP elements <DCTAP Element>`; see section :ref:`elements`. 

**dctap read --warnings example2.csv** sends warnings in plain text to stderr:

.. code-block:: bash

    DCTAP instance
        Shape
            shapeID                  :a
            Statement Template  
                propertyID           dcterms:date
                valueNodeType        noodles

    WARNING [:a/valueNodeType] 'noodles' is not a valid node type.

**dctap read --warnings --json example2.csv** includes warnings in the JSON dictionary:

.. code-block:: json

    {
      "shapes": [
        {
          "shapeID": "default",
          "statement_templates": [
            {
              "propertyID": "dcterms:date",
              "valueNodeType": "noodles"
            }
          ]
        }
      ],
      "namespaces": {
        "dcterms:": "http://purl.org/dc/terms/"
      },
      "warnings": {
        "default": {
          "valueNodeType": [
            "'noodles' is not a valid node type."
          ]
        }
      }
    }

**dctap read --warnings --yaml example2.csv** includes warnings in the YAML output:

.. code-block:: yaml

    shapes:
      - shapeID: default
        statement_templates:
          - propertyID: dcterms:date
            valueNodeType: noodles
    namespaces:
      'dcterms:': http://purl.org/dc/terms/
    warnings:
      default:
        valueNodeType:
          - "'noodles' is not a valid node type."
