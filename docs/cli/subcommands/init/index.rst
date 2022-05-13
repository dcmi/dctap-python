.. _cli_subcommands_init:

Initialize an optional config file
..................................

The command **dctap read** works out of the box, with no options, but its behavior can be customized by editing an optional configuration file. As explained in the section :ref:`config`.

Per-directory config files
::::::::::::::::::::::::::

The subcommand **dctap init** writes a starter configuration file, by default "dctap.yaml", in the working directory. If called with **--hidden**, the starter settings will be written to a **.dctaprc**. Thereafter, whenever **dctap read** is run, the program will look in the working directory first for **dctap.yaml**, then for **.dctaprc** and, if neither is found, will use built-in defaults.

.. code-block:: bash

    $ cd /home/tombaker/myproject/data/
    data$ dctap init                   # Write default dctap.yaml
    data$ dctap init --hidden          # Write alternative .dctaprc
    data$ dctap read x.csv             # Use 1) dctap.yaml or 2) .dctaprc

Global config files
:::::::::::::::::::

Once generated, config files may be moved to arbitrary locations or even renamed. As described in the section :ref:`cli_subcommands_read`, config files at arbitrary locations may be referenced by their absolute or relative pathnames with the option **--config [path-to-configfile]**. In this way, one central config file can be referenced from anywhere on the file system or multiple config files can be created with alternative settings.

.. code-block:: bash

    data$ mv dctap.yaml ..
    data$ dctap read --config ../dctap.yaml example.csv

    data$ mv dctap.yaml /home/tbaker/myproject/dctap_global.yaml
    data$ dctap read --config /home/tombaker/myproject/dctap_global.yaml example.csv
