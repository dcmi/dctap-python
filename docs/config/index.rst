.. _config:

Configuration
-------------

`dctap` has built-in defaults for configuration settings that are customizable by users. For example:

.. code-block:: yaml

    # dctap configuration file (in YAML format)
    default_shape_name: ":default"
    
    value_node_types:
    - iri
    - literal
    - bnode
    
    prefixes:
        ":":        "http://example.org/"
        "dc:":      "http://purl.org/dc/elements/1.1/"
        "dcterms:": "http://purl.org/dc/terms/"
        "dct:":     "http://purl.org/dc/terms/"
        "foaf:":    "http://xmlns.com/foaf/0.1/"
        "owl:":     "http://www.w3.org/2002/07/owl#"
        "rdf:":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        "rdfs:":    "http://www.w3.org/2000/01/rdf-schema#"
        "schema:":  "http://schema.org/"
        "skos:":    "http://www.w3.org/2004/02/skos/core#"
        "skosxl:":  "http://www.w3.org/2008/05/skos-xl#"
        "wdt:":     "http://www.wikidata.org/prop/direct/"
        "xsd:":     "http://www.w3.org/2001/XMLSchema#"

The latest settings can be found in [config.py](https://github.com/dcmi/dctap-python/blob/main/dctap/config.py) in the variable ``DEFAULT_CONFIG_YAML``. 

As explained in the section :ref:`cli_init`, the default settings can be written to a file and customized there.
