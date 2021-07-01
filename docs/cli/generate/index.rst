.. _cli_generate:

dctap generate
^^^^^^^^^^^^^^

The subcommand ``dctap generate``:

- reads a CSV stream (usually a file)
- sends output to stdout as text (for on-screen debugging), JSON, or YAML
- if requested, sends warnings to stderr.

``dctap generate`` (no options)
...............................

Given a CSV table, "example.csv":

.. csv-table:: 
   :file: example.csv
   :header-rows: 1

the basic ``generate`` subcommand (without options) outputs a lightly normalized view of those parts of the CSV that follow the DCTAP model. Note that the CSV can be specified as a filename argument or sent to ``dctap generate`` via stdin. The commands ``dctap generate example`` and ``cat example | dctap generate -`` (note the dash) get the same result:

.. code-block:: bash

    $ cat example.csv | dctap generate -
    DCTAP instance
        Shape
            shapeID:                 :a
            Statement Constraint
                propertyID:          dcterms:creator
                valueNodeType:       iri

``dctap generate --warnings``
.............................

The option ``--warnings`` causes the results of various consistency checks (as detailed below) to be sent to stderr:

.. code-block:: bash

    $ dctap generate --warnings example2.csv
    DCTAP instance
        Shape
            shapeID:                 :a
            Statement Constraint
                propertyID:          dcterms:date
                valueNodeType:       noodles

    WARNING [:a/valueNodeType] 'noodles' is not a valid node type.

``dctap generate --expand-prefixes``
....................................

The option ``--expand-prefixes`` triggers the expansion of namespace prefixes used in :term:`Compact IRI`\s to be expanded, by checking the prefix mappings defined in a configuration file --- by default ``.dctaprc`` in the working directory, or any other file specified with the ``--configfile`` option. If no configuration file is found, it will check the prefixes against a dozen or so mappings defined as built-in configuration defaults.

.. code-block:: bash

    $ dctap generate --expand-prefixes example.csv
    DCTAP instance
        Shape
            shapeID:                 http://example.org/a
            Statement Constraint
                propertyID:          http://purl.org/dc/terms/creator
                valueNodeType:       iri

``dctap generate --configfile``
...............................

The option ``--configfile`` triggers use of a configuration file other than the default ``.dctaprc``. Settings such as the default shape name and namespace prefix mappings can be tweaked in this file, as discussed in the section :ref:`config`. A starter configuration file can be generated with ``dctap init``, as described in the next section.

.. code-block:: bash

    $ dctap generate --configfile /home/tbaker/dctap.yml example.csv


``dctap generate --json``/``--yaml``
....................................

The options ``--json`` and ``--yaml`` (which cannot be used at the same time) send JSON or YAML representations of (lightly normalized) DCTAP/CSV contents to stdout. Note that these options can be used in combination with ``--warnings``, which are sent to stderr.
