dctap-python
============

Basic validation of a DCTAP instance.

|Tests Badge|

Documentation
-------------

- [dctap-python project](https://readthedocs.org/projects/dctap-python/) on readthedocs.org
- https://dctap-python.readthedocs.io/en/latest/

|Docs Badge|

Installation
------------

To work correctly, "dctap" requires Python 3.7 or higher. Executing the command ``python3`` should show you if Python 3 is installed on your machine and in which version.

Installation from pip
^^^^^^^^^^^^^^^^^^^^^

Installing with "pip" pulls the most recently published version of the project from the `PyPI repository <https://pypi.org/project/dctap/>`_. Before installing, it is good practice to create and activate a virtual environment so that "dctap" is not installed into the global Python environment on your machine. The virtual environment is held in a directory of your choice; in the example below, a hidden directory ``.venv`` is created in ``some_directory`` (your current working directory), and the virtual environment is activated by executing ``source .venv/bin/activate``.


.. code-block:: bash
    
    some_directory$ python3 -m venv .venv
    some_directory$ source .venv/bin/activate
    some_directory$ python3 -m pip install dctap

Installation from local clone of Git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloning the "dctap-python" repository to your machine and installing it from the ``dctap-python`` directory is a good option if you want to keep up-to-date with the latest developments in the project. The following commands install "dctap" for the first time. In order to refresh the project directly from the project repository, you can at any time execute ``git pull`` (from within the repository), which will install the latest features and bug fixes in your local copy.

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    dctap-python$ python -m venv .venv
    dctap-python$ source .venv/bin/activate
    dctap-python$ python3 -m pip install flit Pygments
    dctap-python$ flit install -s

        566  pip list
          567  python3 -m pip install --upgrade pip
            568  python3 -m pip install dctap

.. |Docs Badge| image:: https://readthedocs.org/projects/dctap-python/badge/
       :alt: Documentation Status
       :scale: 100%
       :target: https://dctap-python.readthedocs.io
       
.. |Tests Badge| image:: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml/badge.svg
       :alt: Test Status
       :scale: 100%
       :target: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml
