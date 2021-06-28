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

Once installed, the script can be run by first activating the virtual environment. Once the virtual environment is 
activated, the script will run within any working directory on the filesystem.

.. code-block:: bash

    $ cd dctap-python
    dctap-python$ source .venv/bin/activate
    dctap-python$ cd ../../anywhere
    anywhere$ dctap
    Usage: dctap [OPTIONS] COMMAND [ARGS]...
    
      DC Tabular Application Profiles (DCTAP) - base module
    
    Options:
      --version  Show version and exit
      --help     Show help and exit
    
    Commands:
      inspect  Output CSV contents to text, JSON, or YAML, with warnings
      model    Show DCTAP model built-ins for ready reference
    
The subcommand ``inspect`` reads and outputs the contents of a given CSV file::

    $ dctap inspect example.csv
    DCTAP instance
        Shape
            shapeID:                 :book
            Statement Constraint
                propertyID:          dcterms:creator
                valueShape:          author
        Shape
            shapeID:                 :author
            Statement Constraint
                propertyID:          foaf:name


The subcommand 'model' displays program built-ins for the DCTAP model::

    $ dctap model
