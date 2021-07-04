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

.. code-block:: bash

    $ git clone https://github.com/dcmi/dctap-python.git
    $ cd dctap-python
    dctap-python$ python -m venv .venv
    dctap-python$ source .venv/bin/activate
    dctap-python$ python3 -m pip install flit Pygments
    dctap-python$ flit install -s

.. |Docs Badge| image:: https://readthedocs.org/projects/dctap-python/badge/
       :alt: Documentation Status
       :scale: 100%
       :target: https://dctap-python.readthedocs.io
       
.. |Tests Badge| image:: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml/badge.svg
       :alt: Test Status
       :scale: 100%
       :target: https://github.com/dcmi/dctap-python/actions/workflows/python-tests.yaml
