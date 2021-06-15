About dctap
-----------

Dctap is:

- a Python module for parsing, normalizing, and converting CSV files formatted according to the `DC Application Profiles (DCTAP) model <https://github.com/dcmi/dctap/blob/main/TAPprimer.md>`_
- a command-line utility usable for
  - viewing the normalized contents of a DCTAP/CSV file on screen as an aid for debugging,
  - generating JSON output for use in an application pipeline.

As of June 2021, our medium-term plan is:

- to move the command-line utility off into a separate project
- to leave the module as a pip-installable basis for utlities that implement more specific features, such as transforming a DCTAP instance into ShEx.

This project has been undertaken in parallel to, and in support of, a [DCMI working group](https://www.dublincore.org/groups/application_profiles_ig/) that is creating the DCTAP model.

The code in this project tries to anticipate messy or incomplete CSV inputs and to fill gaps and normalize inconsistencies. For example, the code allows users to enter URIs either as full URIs (with or without enclosing angle brackets) or as abbreviated URIs written with namespace prefixes (e.g., 'dcterms:creator'), or to enter the datatypes of literal values without using an extra column to specify that the value is a Literal (since this can be inferred).

As of August 2020, work both in this project and in the context of the DCMI working group has focused on defining the DCTAP model and its elements (concretely: the fixed set of CSV column headers). As the nature and definition of these elements is still somewhat in flux, the descriptions provided in this documentation should be considered provisional.

It is also our hope that modules and Python classes on which this command-line utility can be adapted for use in other environments. This documentation explains how CSV files are interpreted and normalized. For an up-to-the-minute look at how the modules and classes work, the reader is invited to inspect (and execute) the pytest unit tests, which have been formulated for ease of comprehension.

Potential directions for the further development of this project include:

- Resolution of prefixed URIs to full URIs on the basis of a table of namespace prefixes.

- The ability to tweak built-in defaults in local configuration files.

- The ability to read namespace prefixes from sources on the Web or from local configuration files.

- The ability to round-trip from a messy, first-draft CSV expression of a DCTAP, via a normalized expression in Python, then (potentially) back to a normalized expression in CSV.

- The ability to write the Python expression of a DCTAP to an Excel spreadsheet, potentially with tabs for namespace prefixes and controlled sets of values (such as the four main value types URI, Literal, Nonliteral, and BNode) linked to specific columns of the main sheet for use as dropdown menus.

