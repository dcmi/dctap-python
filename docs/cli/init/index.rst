.. _cli_init:

dctap init
^^^^^^^^^^

The ``init`` subcommand writes the built-in configuration defaults to a file, by default ``.dctaprc`` in the working directory. These settings can be hand-edited, for example to add namespace prefix mappings. Thereafter, whenever ``dctap generate...`` is run in that directory, its settings will be used instead of the built-in defaults.

``dctap init`` (no options)
...........................

.. code-block:: bash

    $ dctap init
    Built-in settings written to .dctaprc - edit as needed.

``dctap init --configfile``
...........................

The option ``--configfile`` designates an alternative pathname for the configuration file.

.. code-block:: bash

    $ dctap init --configfile /home/tbaker/dctap.yaml
    Built-in settings written to /home/tbaker/dctap.yaml - edit as needed.

