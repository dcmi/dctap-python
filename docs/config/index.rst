.. _config:

Configuration
-------------

**dctap** has built-in defaults for configuration settings that are customizable by users by generating and editing configuration file as explained in the section :ref:`cli_subcommands_init`. The latest built-in settings can be found in the YAML string variable **DEFAULT_CONFIG_YAML** in the source code file `defaults.py <https://github.com/dcmi/dctap-python/blob/main/dctap/defaults.py>`_. Here is an example configuration file::

    default_shape_identifier: "default"

    prefixes:
        ":":        "http://example.org/"
        "dcterms:": "http://purl.org/dc/terms/"
        "foaf:":    "http://xmlns.com/foaf/0.1/"

    extra_shape_elements:
    - "closed"

    extra_statement_template_elements:
    - "min"
    - "max"

    list_elements:
    - "propertyID"
    - "valueNodeType"
    - "valueDataType"

    list_item_separator: ","

    extra_value_node_types:
    - "uri"
    - "nonliteral"

    extra_element_aliases:
        "DataType": "valueDataType"

    boolean_aliases:
        "Y": "true"
        "N": "false"

.. toctree::

   default_shape_name/index.rst
   prefix_mappings/index.rst
   extra_elements/index.rst
   list_elements/index.rst
   list_item_separator/index.rst
   list_elements/valueNodeType/index.rst
   element_aliases/index.rst
