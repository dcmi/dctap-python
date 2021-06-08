Installation
------------

The following commands install 'dctap' in editable mode.

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python3 -m pip install flit Pygments
    $ flit install -s

Once installed, the script can be run by first activating 
the virtual environment:

.. code-block:: bash

    $ cd dctap-python
    $ source .venv/bin/activate
    $ dctap
    Usage: dctap [OPTIONS] COMMAND [ARGS]...

    DC Tabular Application Profiles (DCTAP) - base module

    Options:
      --version  Show version and exit
      --help     Show help and exit

    Commands:
      inspect  Inspect CSV file contents, normalized, maybe with expanded...
      model    Show DCTAP model built-ins for ready reference

