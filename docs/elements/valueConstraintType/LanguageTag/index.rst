.. _elem_valueConstraintType_languagetag:

LanguageTag
^^^^^^^^^^^

Language tags --- abbreviated names for natural languages such as ``fr`` for French or ``fr-CA`` for Canadian French --- are used to mark the language of text elements in Web documents and commonly serve as a controlled vocabulary of identifiers for languages.

As with the value constraint type :ref:`elem_valueConstraintType_picklist`, a value constraint of type "LanguageTag" is split on whitespace.

A string with no whitespace is parsed into a list with just one string. As the rules for well-formed language tags are quite complex, the module makes no attempt to check whether the language tags appear to be well-formed.

.. csv-table:: 
   :file: languageTag.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID:                 :default
            Statement Constraint
                propertyID:          :status
                valueConstraint:     ['fr']
                valueConstraintType: languagetag
            Statement Constraint
                propertyID:          :status
                valueConstraint:     ['fr', 'fr-CA']
                valueConstraintType: languagetag
