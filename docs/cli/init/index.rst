.. _cli_init:

Initialize optional config files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The command **dctap generate** works out of the box, with no options, but its behavior can be customized by editing an optional configuration file. As explained in the section :ref:`config`.

Per-directory config files
..........................

The subcommand **dctap init** generates a starter configuration file by writing built-in defaults to a file, by default "dctap.yml" in the working directory. These settings can be hand-edited, for example to add namespace prefix mappings. Thereafter, whenever **dctap generate...** is run in that directory, its settings will be used instead of the built-in defaults.

.. code-block:: bash

    $ cd /home/tombaker/myproject/data/

    data$ dctap init
    Built-in settings written to dctap.yml - edit as needed.

    data$ dctap generate example.csv
    ...

Global config files
...................

Alternatively, a configuration file can be generated at a fixed location using the **dctap init --configfile** option, and referenced using **dctap generate --configfile**, which designates an alternative pathname for the configuration file.

.. code-block:: bash

    data$ dctap init --configfile /home/tombaker/myproject/dctap.yaml
    Built-in settings written to /home/tombaker/myproject/dctap.yaml - edit as needed.

    data$ dctap generate --configfile /home/tombaker/myproject/dctap.yaml example.csv
    ...
