.. _cli_subcommands_read:

View a TAP as TXT, JSON, or YAML
................................

The subcommand **dctap read**:

- reads a CSV file
  - alternatively, reads CSV file contents from stdin (eg, **cat example.csv | dctap read -**)
- sends a lightly normalized view of a TAP to stdout
  - by default, outputs TXT for on-screen debugging, without showing prefixes
  - with option **--json**, outputs JSON, with namespace prefixes
  - with option **--yaml**, outputs YAML, with namespace prefixes
- with the option **--warnings**, sends warnings to stderr

The option **--expand-prefixes** expands any :term:`Compact IRI` into a full :term:`IRI` using prefixes found in the built-in defaults or as overridden by a :ref:`configuration file <prefix_mappings>`.

The file **example.csv**:

.. csv-table::
   :file: example.csv
   :header-rows: 1

can be read as TXT, with full IRIs, with **dctap read --expand-prefixes example.csv**:

.. code-block:: bash

    DCTAP instance
        Shape
            shapeID                  http://example.org/a
            Statement Template
                propertyID           http://purl.org/dc/terms/creator
                valueNodeType        iri

Or as JSON with **dctap read --json example.csv**:

.. code-block:: json

    {
      "shapes": [
        {
          "shapeID": ":a",
          "statement_templates": [
            {
              "propertyID": "dcterms:creator",
              "valueNodeType": "iri"
            }
          ]
        }
      ],
      "namespaces": {
        "dcterms:": "http://purl.org/dc/terms/",
        ":": "http://example.org/"
      }
    }

Or as YAML, with full IRIs, with **dctap read --yaml example.csv**:

.. code-block:: yaml

    shapes:
      - shapeID: http://example.org/a
        statement_templates:
          - propertyID: http://purl.org/dc/terms/creator
            valueNodeType: iri
    namespaces:
      'dcterms:': http://purl.org/dc/terms/
      ':': http://example.org/

.. toctree::
   :hidden:

   warnings/index.rst
   configfile/index.rst

