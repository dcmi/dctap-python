.. _home:

About dctap
===========

**dctap** is a Python package for parsing and normalizing spreadsheets or CSV files that follow the `DC Tabular Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_ (see `installation instructions <https://github.com/dcmi/dctap-python/>`_).

**dctap** provides a command-line tool for viewing the normalized contents of a DCTAP/CSV file in one of three interchangeable formats: a verbose indented-TXT format (for human users) and YAML or JSON (for machines). The tool checks a CSV for potential violations of the DCTAP model and emits warnings or helpful suggestions.

While an :term:`Application Profile`, including a DCTAP profile, is designed to support the evaluation and validation of :term:`Instance Data`, **dctap** itself does not support such operations. By converting the contents of a tabular profile into JSON or YAML, however, **dctap** can serve as a preprocessor for downstream applications that can perform such validation on the basis of formal specifications as `Shape Expressions Language (ShEx) <http://shexspec.github.io/primer/>`_ or `Shapes Constraint Language (SHACL) <https://www.w3.org/TR/shacl/>`_.

The consistency checks undertaken by **dctap** err on the side of tolerance, as it is anticipated that DCTAP will be used not just for finished profiles but also for early drafts and prototypes. Users of DCTAP are invited to customize the format with local extensions. Any parts of a CSV that cannot be processed by **dctap** are simply passed through, untouched, to applications downstream.

.. toctree::
   :hidden:

   model/index.rst
   elements/index
   config/index
   design/index
   glossary/index
   cli/index
