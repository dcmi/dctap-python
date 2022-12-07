.. _about:

About dctap
-----------

**dctap** is a Python package for parsing and normalizing CSV files formatted according to the `DC Tabular Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_. It provides a command-line tool for viewing the normalized contents of a DCTAP/CSV file in a verbose indented-TXT format, in YAML, or in JSON. The tool performs basic consistency checks and emits warnings as an aid to debugging a CSV.

for use in application pipelines.


These checks focus on verifying those parts of a CSV that fit the DCTAP model. Any parts of a CSV that are not covered by the DCTAP model, such as extra columns (aka "elements"), are simply passed through to the text, JSON, or YAML output. 

The module passes input through to output unchanged, possibly with added warnings, with the following exceptions:

- Element names (column headers) are normalized to lowercase without whitespace or punctuation (see section :ref:`design_keywords_lowercased`).

- Normalized elements not part of the DCTAP model are ignored (see section :ref:`design_elements_unknown_ignored`).

- Boolean values are normalized to the strings "false" and "true" (see section :ref:`elem_mandrepeat`).

- Value constraint strings are converted into other types of data structure, such as lists, according to the value constraint type provided (see section :ref:`elem_valueConstraintType`).

The built-in consistency checks err on the side of tolerance, as it is anticipated that DCTAP CSVs may be used not only to document mature, polished application profiles but also as tools for rapid prototyping. The performance of stricter checks, for example to verify whether values declared to be URIs, dates, or language tags are well-formed, is left to downstream projects that may import and build on this module.
