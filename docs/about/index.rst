.. _about:

About dctap
-----------

**dctap** is a Python package for parsing and normalizing spreadsheets or CSV files that follow the `DC Tabular Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_. It provides a command-line tool for viewing the normalized contents of a DCTAP/CSV file in a verbose indented-TXT format, in YAML, or in JSON. The tool checks a CSV for potential violations of the DCTAP model and emits helpful warnings.

Application profiles, including spreadsheets in DCTAP format, are designed to support the evaluation and validation of instance data. The **dctap** package itself does not support any such operations. Rather, by converting the contents of a CSV into JSON or YAML, **dctap** can serve as a preprocessor for downstream applications that can perform validation on the basis of specifications as `Shape Expressions Language (ShEx) <http://shexspec.github.io/primer/>`_ or `Shapes Constraint Language (SHACL) <https://www.w3.org/TR/shacl/>`_.

The built-in consistency checks err on the side of tolerance, as it is anticipated that DCTAP CSVs may be used not only for documenting finished application profiles but also for early drafts and prototypes. Users of DCTAP are invited to customize the format with local extensions. Any contents in a spreadsheet not recognized by **dctap** as part of the DCTAP model (or a local extension) are simply passed through to output untouched.
