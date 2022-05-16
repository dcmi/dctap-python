.. _minimum_profile:

Minimal application profile
...........................

In the DCTAP model, the simplest possible application profile consists of just one :term:`Statement Template` in the context of one :term:`Shape`.

A Statement Template has, at a minimum, one **propertyID** element, and the existence of a Shape can be inferred, so in practical terms, the simplest possible application profile is a list of just one property.

Note that if a shape identifier is not explicitly assigned in a CSV, a default identifier will be assigned. (This is discussed in the the section :ref:`elem_shapeID`.) In "shape-less" applications, this shape identifier can simply be ignored.

.. csv-table:: 
   :file: propertyID_only.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           http://purl.org/dc/terms/title
            Statement Template
                propertyID           http://purl.org/dc/terms/publisher
            Statement Template
                propertyID           https://schema.org/creator
            Statement Template
                propertyID           http://purl.org/dc/terms/date
