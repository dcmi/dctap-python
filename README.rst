dctap-python
============

Basic validation of a DCTAP instance.

|Tests Badge| |Docs Badge| |Black Badge|

Documentation
-------------

- https://dctap-python.readthedocs.io/en/latest/


Installation
------------

To work correctly, "dctap" requires Python 3.7 or higher. Executing the command ``python3`` should show you if Python 3 is installed on your machine and in which version.

As explained below, the command-line utility can be installed either from the online PyPI repository, using the ``pip`` command, or from a local copy of the project on your own machine.

Installation from PyPI
^^^^^^^^^^^^^^^^^^^^^^

Installing with "pip" pulls the most recently published version of the project from the `PyPI repository <https://pypi.org/project/dctap/>`_ with the following command:

.. code-block:: bash

    python3 -m pip install dctap

or uninstalled with:

.. code-block:: bash

    python3 -m pip uninstall dctap

Installation from Github
^^^^^^^^^^^^^^^^^^^^^^^^

"dctap" can be installed directly from Github with:

.. code-block:: bash

    python3 -m pip install -U https://github.com/dcmi/dctap-python/archive/main.zip

Installing "dctap" this way, and periodically re-running this command to refresh, is the best way to keep up with the latest version of "dctap".

Installation with pip in virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For developers who work alot with Python projects, it is good practice to create and activate a virtual environment so that "dctap", and its dependencies, will not be installed into the global Python environment on your machine. The virtual environment is held in a directory of your choice; in the example below, a hidden directory ``.venv`` is created in ``some_directory`` (your current working directory), and the virtual environment is activated by executing ``source .venv/bin/activate``.

.. code-block:: bash
    
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ python3 -m pip install -U https://github.com/dcmi/dctap-python/archive/main.zip

Note that "dctap" will pip-install even without creating and activating a virtual environment, even though this is not considered good practice. If you do install it into a virtual environment, note that the virtual environment must be activated with `source .venv/bin/activate` or "dctap" will not work. The activation of a virtual environment can be automated by adding this command to a shell profile where it will be executed when starting the shell, for example by adding the lines to the file "~/.bash_profile":

.. code-block:: bash

    cd /Users/foo/somedirectory
    source .venv/bin/activate

Installation from a local clone of Git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloning the "dctap-python" repository to your machine and installing it from the ``dctap-python`` directory is a good option if you want to keep up-to-date with the latest developments in the project. The following commands install "dctap" for the first time. In order to refresh the project directly from the project repository, you can at any time execute ``git pull`` (from within the repository), which will install the latest features and bug fixes in your local copy.

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python3 -m pip install flit Pygments
    $ flit install -s

Quick start
-----------

Run without arguments, "dctap" shows what options and commands are available.

.. code-block:: bash

    $ dctap
    Usage: dctap [OPTIONS] COMMAND [ARGS]...

      DC Tabular Application Profiles (DCTAP) - base module

      Examples:

      $ dctap generate my_profile.csv
      $ dctap generate --json my_profile.csv
      $ dctap generate --expand-prefixes my_profile.csv
      $ dctap generate --warnings my_profile.csv
      $ dctap generate --warnings --expand-prefixes --json my_profile.csv
      $ dctap init
      Built-in settings written to dctap.yml - edit as needed.
      $ dctap init /Users/tbaker/dctap.yml
      Built-in settings written to /Users/tbaker/dctap.yml - edit as needed.
      $ dctap generate --configfile /Users/tbaker/dctap.yml

    Options:
      --version  Show version and exit
      --help     Show help and exit

    Commands:
      generate  Generate normalized text, JSON, or YAML of CSV, with warnings.
      init      Generate customizable configuration file [default: dctap.yml].

For more information, see the documentation `on readthedocs.io <https://dctap-python.readthedocs.io/en/latest/>`_.

.. |Docs Badge| image:: https://readthedocs.org/projects/dctap-python/badge/
       :alt: Documentation Status
       :scale: 100%
       :target: https://dctap-python.readthedocs.io
       
.. |Tests Badge| image:: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml/badge.svg
       :alt: Test Status
       :scale: 100%
       :target: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml

.. |Black Badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
       :alt: Code style: black
       :scale: 100%
       :target: https://github.com/dcmi/dctap-python
