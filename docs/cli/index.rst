.. _cli:

Command-line tool
-----------------

To work correctly, "dctap" requires Python 3.6 or higher. Executing the command ``python3`` should show you if Python 3 is installed on your machine and in which version.

As explained below, the command-line utility can be installed either from the online PyPI repository, using the ``pip`` command, or from a local copy of the project on your own machine.

The utility has two subcommands:

.. toctree::

   init/index
   generate/index

Install with pip (ordinary users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing with "pip" pulls the most recently published version of the project from the `PyPI repository <https://pypi.org/project/dctap/>`_ with the following command:

.. code-block:: bash

    python3 -m pip install -U https://github.com/dcmi/dctap-python/archive/main.zip

Install with pip (developers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For developers who work alot with Python projects, it is good practice to create and activate a virtual environment so that "dctap", and its dependencies, will not be installed into the global Python environment on your machine. The virtual environment is held in a directory of your choice; in the example below, a hidden directory ``.venv`` is created in ``some_directory`` (your current working directory), and the virtual environment is activated by executing ``source .venv/bin/activate``.

.. code-block:: bash
    
    some_directory$ python3 -m venv .venv
    some_directory$ source .venv/bin/activate
    some_directory$ python3 -m pip install -U https://github.com/dcmi/dctap-python/archive/main.zip

Note that "dctap" will pip-install even without creating and activating a virtual environment, even though this is not considered good practice. If you do install it into a virtual environment, note that the virtual environment must be activated with `source .venv/bin/activate` or "dctap" will not work. The activation of a virtual environment can be automated by adding this command to a shell profile where it will be executed when starting the shell, for example by adding the lines to the file "~/.bash_profile":

.. code-block:: bash

    cd /Users/foo/somedirectory
    source .venv/bin/activate

Install from a local clone of Git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloning the "dctap-python" repository to your machine and installing it from the ``dctap-python`` directory is a good option if you want to keep up-to-date with the latest developments in the project. The following commands install "dctap" for the first time. In order to refresh the project directly from the project repository, you can at any time execute ``git pull`` (from within the repository), which will install the latest features and bug fixes in your local copy.

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    dctap-python$ python -m venv .venv
    dctap-python$ source .venv/bin/activate
    dctap-python$ python3 -m pip install flit Pygments
    dctap-python$ flit install -s

