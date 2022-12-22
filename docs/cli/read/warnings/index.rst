.. _cli_subcommands_read_warnings:

View warnings generated
:::::::::::::::::::::::

As an aid for debugging, **dctap read** checks the CSV input for obvious inconsistencies and generates warnings for any anomalies or errors found. 

These consistency checks are explained in the descriptions of individual :term:`DCTAP elements <DCTAP Element>`; see section :ref:`elements`. 

The option **--warnings** causes the results of these checks to be sent to stderr. This ensures that warnings are kept out of the stdout streams of text, JSON, or YAML output and can thus be passed as input to other commands in a pipeline.

.. code-block:: bash

    $ dctap read --warnings example2.csv
    DCTAP instance
        Shape
            shapeID                  :a
            Statement Template  
                propertyID           dcterms:date
                valueNodeType        noodles

    WARNING [:a/valueNodeType] 'noodles' is not a valid node type.

