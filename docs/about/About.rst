About dctap
-----------

Dctap is a command-line utility for reading, interpreting, and verifying CSV files formatted according to the DC Application Profile (DCTAP) model. The utility interprets and normalizes the contents of a CSV file and prints the results to standard output as an aid for debugging. 

This project has been undertaken in parallel to, and in support of, a working group of the Dublin Core Metadata Initiative which is creating the DCTAP model (@@@add links).

The code in this project tries to anticipate messy or incomplete CSV inputs and to fill gaps and normalize inconsistencies. For example, the code allows users to enter URIs either as full URIs (with or without enclosing angle brackets) or as abbreviated URIs written with namespace prefixes (e.g., 'dcterms:creator'), or to enter the datatypes of literal values without using an extra column to specify that the value is a Literal (since this can be inferred).

As of August 2020, work both in this project and in the context of the DCMI working group has focused on defining the DCTAP model and its elements (concretely: the fixed set of CSV column headers). As the nature and definition of these elements is still somewhat in flux, the descriptions provided in this documentation should be considered provisional.

It is also our hope that modules and Python classes on which this command-line utility can be adapted for use in other environments. This documentation explains how CSV files are interpreted and normalized. For an up-to-the-minute look at how the modules and classes work, the reader is invited to inspect (and execute) the pytest unit tests, which have been formulated for ease of comprehension.

Potential directions for the further development of this project include:

- Resolution of prefixed URIs to full URIs on the basis of a table of namespace prefixes.

- The ability to tweak built-in defaults in local configuration files.

- The ability to read namespace prefixes from sources on the Web or from local configuration files.

- The ability to round-trip from a messy, first-draft CSV expression of a DCTAP, via a normalized expression in Python, then (potentially) back to a normalized expression in CSV.

- The ability to write the Python expression of a DCTAP to an Excel spreadsheet, potentially with tabs for namespace prefixes and controlled sets of values (such as the four main value types URI, Literal, Nonliteral, and BNode) linked to specific columns of the main sheet for use as dropdown menus.

