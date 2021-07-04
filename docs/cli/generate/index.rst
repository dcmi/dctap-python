.. _cli_generate:

Generate text, JSON, or YAML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The subcommand **dctap generate**:

- reads a CSV stream (usually a file)
- sends output to stdout as text (for on-screen debugging), JSON, or YAML
- if requested, sends warnings to stderr.

View CSV contents as text
.........................

When used without options, **dctap generate** outputs a lightly normalized view of the DCTAP elements in a CSV to stdout. Note that the CSV can be specified as a filename argument or sent to the command via stdin. The commands **dctap generate example** and **cat example | dctap generate -** (note the dash) get the same result:

.. code-block:: bash

    $ cat example.csv | dctap generate -
    DCTAP instance
        Shape
            shapeID:                 :a
            Statement Constraint
                propertyID:          dcterms:creator
                valueNodeType:       iri

View warnings
.............

As an aid for debugging, the `dctap generate` subcommand performs various consistency checks on the CSV input and generates warnings for any anomalies or possible errors found. Explanations of these consistency checks can be found in the descriptions of individual :term:`DCTAP Element`\s; see section :ref:`elements`. The option **--warnings** causes the results of these checks to be sent to stderr. This ensures that the warnings are kept out of the stdout streams of text, JSON, or YAML output and can thus be passed as input to other commands in a pipeline.

.. code-block:: bash

    $ dctap generate --warnings example2.csv
    DCTAP instance
        Shape
            shapeID:                 :a
            Statement Constraint
                propertyID:          dcterms:date
                valueNodeType:       noodles

    WARNING [:a/valueNodeType] 'noodles' is not a valid node type.

Expand prefixes
...............

The option **--expand-prefixes** triggers the expansion of namespace prefixes used in :term:`Compact IRI`\s to be expanded, by checking the prefix mappings defined in a configuration file --- by default "dctap.yml" in the working directory, or any other file specified with the **--configfile** option. If no configuration file is found, it will check the prefixes against a dozen or so mappings defined as built-in configuration defaults.

.. code-block:: bash

    $ dctap generate --expand-prefixes example.csv
    DCTAP instance
        Shape
            shapeID:                 http://example.org/a
            Statement Constraint
                propertyID:          http://purl.org/dc/terms/creator
                valueNodeType:       iri

Use a custom config file
........................

The option **--configfile** triggers use of a configuration file other than the default "dctap.yml". Settings such as the default shape name and namespace prefix mappings can be tweaked in this file, as discussed in the section :ref:`config`. A starter configuration file can be generated with **dctap init**, as described in the next section.

.. code-block:: bash

    $ dctap generate --configfile /home/tbaker/dctap.yml example.csv


Generate JSON or YAML output
............................

The options **--json** and **--yaml** (which cannot be used in combination) send JSON or YAML representations of the lightly normalized DCTAP elements in a CSV to stdout. These options can be used in combination with **--warnings**, which are sent to stderr.
