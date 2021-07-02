.. _about:

About the project
-----------------

This project consists of:

- A Python module for parsing, normalizing, and converting CSV files formatted according to the `DC Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_.

- A command-line utility usable 

  - for viewing the normalized contents of a DCTAP/CSV file on screen as an aid in debugging, and 

  - for generating machine-processable output in JSON and YAML for use in application pipelines.

This documentation describes the :ref:`model` and its :term:`DCTAP Element`\s (a set of labels used as spreadsheet headers). 

The module performs a few simple consistency checks and emits warnings as an aid in debugging. (These are described in the documentation below.) These checks focus on verifying those parts of a CSV that fit the DCTAP model. Any parts of a CSV that are not covered by the DCTAP model, such as extra columns (aka "elements"), are simply passed through to the text, JSON, or YAML output. 

The module passes input through to output unchanged, possibly with added warnings, with the following exceptions:

- Element names (column headers) are normalized to lowercase without whitespace or punctuation (see section :ref:`design_elements_lowercased`).

- Normalized elements not part of the DCTAP model are ignored (see section :ref:`design_elements_unknown_ignored`).

- Boolean values are normalized to "False" and "True" (see section :ref:`elem_mandrepeat`).

- Value constraint strings are converted into other types of data structure, such as lists, according to the value constraint type provided (see section :ref:`elem_valueConstraintType`).

The built-in consistency checks err on the side of tolerance, as it is anticipated that DCTAP CSVs may be used not only to document mature, polished application profiles but also as tools for rapid prototyping. The performance of stricter checks, for example to verify whether values declared to be URIs, dates, or language tags are well-formed, is left to downstream projects that may import and build on this module.

Potential directions for further development include:

- The ability to tweak built-in defaults in local configuration files.

- The ability to expand :term:`Compact IRI` s by reading namespace prefixes from sources on the Web or from local configuration files.

- The ability to round-trip from a messy, first-draft CSV expression of a DCTAP back to a normalized expression in CSV.

- The ability to read from Excel spreadsheets directly, without first converting into plain CSV format.

- The ability to read from Excel spreadsheets with extra tabs for namespace prefixes and controlled sets of values for use in dropdown menus.

As of July 2021, our medium-term plan is:

- To move the command-line interface into a separate project.

- To leave this module as a **pip**-installable basis for utlities that implement more specific features, such as transforming a DCTAP instance into ShEx or SHACL.

