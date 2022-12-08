.. _home:

About dctap
===========

**dctap** is a Python package for parsing and normalizing spreadsheets or :term:`CSV File`\s that follow the model for `DC Tabular Application Profiles (DCTAP) <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_ (see `installation instructions <https://github.com/dcmi/dctap-python/>`_).

The **dctap** package includes a command-line tool for viewing the normalized contents of a given :term:`TAP` in one of three interchangeable formats: a verbose indented-TXT format (for human users) and YAML or JSON (for machines). The tool checks a :term:`CSV File` for potential violations of the DCTAP model and emits warnings or helpful suggestions.

An :term:`Application Profile` describes models, vocabularies, and usage patterns that are expected or required to be found in :term:`Instance Data`. Developing a shared profile can help data providers capture consensus models on the "shape" of data in a given domain and improve the coherence or interoperability of data in that domain. Developing that profile in a simple spreadsheet, using DCTAP, can make it easier for people to participate in that process and use its results.

An Application Profile is also commonly used as a basis for data validation. While the **dctap** package itself does not support validation (or any other operation touching on instance data), it can however serve as a preprocessor for validation applications downstream. The normalized representation of a DCTAP CSV in JSON, for example, can be converted into validation schemas expressed in `Shape Expressions Language (ShEx) <http://shexspec.github.io/primer/>`_ or `Shapes Constraint Language (SHACL) <https://www.w3.org/TR/shacl/>`_.

**dctap** aims at catching a few of the more obvious inconsistencies in a given :term:`TAP` -- malformed regular expressions, the use of literal datatypes with nonliteral values, and the like. These checks are documented below and in extensive `unit tests <https://github.com/tombaker/tapshex/tree/main/tests>`_. The checks err on the side of tolerance, and error messages are meant as helpful hints to editors of early drafts. Users are free to customize the DCTAP model with local extensions. Any part of a given :term:`TAP` not recognized by **dctap** as a built-in or customized feature of the DCTAP model is simply ignored.

.. toctree::
   :hidden:

   model/index.rst
   elements/index.rst
   config/index.rst
   design/index.rst
   cli/index.rst
   glossary/index.rst
