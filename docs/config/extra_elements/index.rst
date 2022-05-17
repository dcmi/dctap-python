.. _extra_elements:

Extra Elements
..............

By default, **dctap** ignores elements that are not part of the DCTAP model. As explained in the section ":ref:`design_elements_unknown_ignored`", **dctap** can be configured to recognize extra elements as belonging either to a shape or to a statement template. In the absence of such configuration, **dctap** has no basis for handling a given element as a shape constraint or a statement constraint. Columns with unrecognized headers are simply ignored and passed through, unchanged to text, JSON, or YAML output. 

.. toctree::

   extra_shape_elements/index
   extra_statement_template_elements/index
