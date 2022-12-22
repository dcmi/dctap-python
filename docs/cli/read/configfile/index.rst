.. _cli_subcommands_read_configfile:

Read settings from nondefault config file
:::::::::::::::::::::::::::::::::::::::::

The option **--configfile** can point to non-default :ref:`configuration files <configuration>`.

A starter configuration file can be generated with **dctap init**, as described in the section :ref:`cli_subcommands_init`. As discussed in the section :ref:`config`, settings such as the default shape name and namespace prefix mappings can be tweaked in this file.

.. code-block:: bash

    $ dctap read --configfile /home/tbaker/dctap.yaml example.csv

