.. _cli_subcommands_init:

Initialize an optional config file
..................................

The command **dctap read** works out of the box, with no options, but its behavior can be customized by editing an optional configuration file. As explained in the section :ref:`config`.

Per-directory config files
::::::::::::::::::::::::::

The subcommand **dctap init** generates a starter configuration file by writing built-in defaults to a file, by default "dctap.yml" or ".dctaprc" in the working directory. These settings can be hand-edited, for example to add namespace prefix mappings. Thereafter, whenever **dctap read ...** is run in that directory, the settings found in one of those two files will be used instead of the built-in defaults.

.. code-block:: bash

    $ cd /home/tombaker/myproject/data/
    data$ dctap init
    data$ dctap read example.csv

Global config files
:::::::::::::::::::

Once generated, config files may be moved to arbitrary locations and renamed. As described in the section :ref:`cli_subcommands_read`, config files at arbitrary locations may be referenced by their absolute or relative pathnames with the command **dctap read --configfile ...**:

.. code-block:: bash

    data$ dctap read --configfile /home/tombaker/myproject/dctap.yaml example.csv
    data$ dctap read --configfile ../dctap.yaml example.csv
