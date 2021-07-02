.. _elem_valueConstraintType_IRIStem:

IRIStem
^^^^^^^

A value of type IRIStem is an IRI that can be
matched with longer IRIs. For example, "http://lod.nal.usda.gov/nalt/"
is an IRIStem that matches "http://lod.nal.usda.gov/nalt/10129".
The following example says that values of the "dcterms:subject"
property are expected to be values of the NAL Thesaurus.

.. csv-table::
   :file: IRIStem.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:subject
                valueConstraint:     http://lod.nal.usda.gov/nalt/
                valueConstraintType: iristem

This module will superficially check whether the value constraint
looks like an IRI and, if not, emit a warning.

.. csv-table::
   :file: IRIStem_non_iri.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          dcterms:subject
                valueConstraint:     nalt
                valueConstraintType: iristem

    WARNING [:default/valueConstraint] Value constraint type is 'iristem', but 'nalt' does not look like an IRI or Compact IRI.
