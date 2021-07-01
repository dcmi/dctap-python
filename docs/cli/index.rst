.. _cli:

Command-line tool
-----------------

One can install 'dctap' in editable mode as follows:

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    dctap-python$ python -m venv .venv
    dctap-python$ source .venv/bin/activate
    dctap-python$ python3 -m pip install flit Pygments
    dctap-python$ flit install -s

Once installed, the script can be run by first activating the virtual environment. Once the virtual environment is activated, the script will run within any working directory on the filesystem.

.. code-block:: bash

    $ cd dctap-python
    dctap-python$ source .venv/bin/activate
    dctap-python$ cd ../../anywhere
    anywhere$ dctap ...

The utility has two subcommands:

.. toctree::

   init/index
   generate/index
