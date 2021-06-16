Command-line tool
-----------------

To get basic help, run the command with no arguments or with the '--help' option::

    $ dctap
    $ dctap --help

The subcommand 'generate' reads and displays the contents of a given CSV file (here: 'example.csv')::

    $ dctap inspect example.csv

The subcommend 'model' displays program built-ins for the DCTAP model::

    $ dctap model
Installation
------------

The following commands install 'dctap' in editable mode.

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    dctap-python$ python -m venv .venv
    dctap-python$ source .venv/bin/activate
    dctap-python$ python3 -m pip install flit Pygments
    dctap-python$ flit install -s

Once installed, the script can be run by first activating 
the virtual environment. Once the virtual environment is 
activated, the script will run within any working directory 
on the filesystem.

.. code-block:: bash

    $ cd dctap-python
    dctap-python$ source .venv/bin/activate
    dctap-python$ dctap
    Usage: dctap [OPTIONS] COMMAND [ARGS]...

    DC Tabular Application Profiles (DCTAP) - base module

    Options:
      --version  Show version and exit
      --help     Show help and exit

    Commands:
      inspect  Inspect CSV file contents, normalized, maybe with expanded...
      model    Show DCTAP model built-ins for ready reference

