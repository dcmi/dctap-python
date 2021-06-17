About ``dctap``
---------------

This project is creating:

- a Python module for parsing, normalizing, and converting CSV files formatted according to the `DC Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_.
- a command-line utility usable for viewing the normalized contents of a DCTAP/CSV file on screen as an aid for debugging, and generating machine-processable output in JSON and YAML for use in application pipelines.

This documentation describes the DCTAP :ref:`model` and its "elements" (a set of spreadsheet headers). It shows how the code undertakes simple consistency checks and emits warnings as an aid in debugging.

Potential directions for further development include:

- The ability to tweak built-in defaults in local configuration files.
- The ability to expand :term:`Compact IRI` s by reading namespace prefixes from sources on the Web or from local configuration files.
- The ability to round-trip from a messy, first-draft CSV expression of a DCTAP back to a normalized expression in CSV.
- The ability to read from Excel spreadsheet with extra tabs for namespace prefixes and controlled sets of values for use in dropdown menus.

As of June 2021, our medium-term plan is:

- to move the command-line utility off into a separate project
- to leave the module as a pip-installable basis for utlities that implement more specific features, such as transforming a DCTAP instance into ShEx or SHACL.

