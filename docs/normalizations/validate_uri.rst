URIs
^^^^

In the CSV file of a DCAP, URIs can be represented in three possible ways:

- as full URIs
- as full URIs enclosed in angle brackets
- as prefixed URIs (eg, `dc:`, `wd:Q46914185`)

The base URI of the DCAP can be depicted as a bare colon (`:`).

The Statement class performs some normalization of URI values (stripping out enclosing angle brackets) and checks whether URIs and prefixed URIs are basically well-formed. No attempt is made to cover all edge cases; the sanity checks are no substitute for careful modeling. There is also an attempt to catch inconsistencies in cases where one element depends on, or implies, another. For example:

- With a value type of `URI`, a constraint value (if provided) should be a URI or prefixed URI.
- A constraint type of `UriStem` implies that a constraint value is provided and is a URI or prefixed URI.

The following table shows various valid uses of URIs as constraint values.

.. csv-table:: 
   :file: ../normalizations/validate_uri.csv
   :header-rows: 1

This is interpreted as::

    DCAP
        Shape
            shapeID: :book
            start: True
            Statement
                propertyID: dct:subject
                constraint_value: https://id.loc.gov/subjects
                constraint_type: UriStem
            Statement
                propertyID: dct:subject
                constraint_value: https://id.loc.gov/subjects
                constraint_type: UriStem
            Statement
                propertyID: dct:subject
                constraint_value: nalt:
                constraint_type: UriStem
            Statement
                propertyID: dct:creator
                value_type: URI
                constraint_value: https://www.wikidata.org/wiki/Q46914185
            Statement
                propertyID: dct:creator
                value_type: URI
                constraint_value: wd:Q46914185

The following table illustrates a few simple inconsistencies that will be detected.

.. csv-table:: 
   :file: ../normalizations/validate_uri_bad.csv
   :header-rows: 1

Note:

- The string 'some_string' is not valid as a URI or as a prefixed URI.
- The constraint value `UriStem` implies a constraint value that is a URI or prefixed URI, but none is provided.

If URIs are enclosed URIs in angle brackets, the brackets are stripped away.

.. csv-table:: 
   :file: ../normalizations/uris.csv
   :header-rows: 1

This is interpreted as::

    DCAP
        Shape
            shapeID: :book
            start: True
            Statement
                propertyID: dct:subject
                constraint_value: https://id.loc.gov/subjects
                constraint_type: UriStem
            Statement
                propertyID: dct:creator
                value_type: URI
                constraint_value: https://www.wikidata.org/wiki/Q46914185
