.. _elem_propertyID:

propertyID
^^^^^^^^^^

The DCTAP model was designed for compatibility with the
RDF model. In the RDF model, properties are identified
with IRIs, and this module will issues a warning if a
property identifier, based on a superficial inspection,
does not look like an IRI. 

Users not interested in compatibility with RDF, or users
who are brainstorming a draft application profile and
simply need a placeholder, can safely ignore such a
warning.

.. csv-table:: 
   :file: propertyID.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:creator
            Statement Constraint
                propertyID:          height

    WARNING Shape :default => propertyID: 'height' is not an IRI or Compact IRI.
