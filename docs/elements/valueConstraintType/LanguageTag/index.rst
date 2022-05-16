.. _elem_valueConstraintType_languagetag:

LanguageTag
^^^^^^^^^^^

A :term:`Language Tag` is an abbreviated name for a natural language, such as ``fr`` for French or ``fr-CA`` for Canadian French. Language tags are used to identify the language of a :term:`Literal`. Standard sets of language tags serve as a controlled vocabulary of identifiers for languages.

A value constraint of type "languageTag" is processed as a picklist of one or more language tags. Specifying language tags in this manner means that the value associated with the property (in the example below, with ":status") is expected to be a string tagged with one of the language tags.

As with the value constraint type :ref:`elem_valueConstraintType_picklist`, a value constraint of type "LanguageTag" is split on whitespace unless another list separator has been defined (see section :ref:`config`).

A string with no whitespace is parsed into a list with just one string. As the rules for well-formed language tags are quite complex, the module makes no attempt to check whether the language tags themselves are well-formed.

.. csv-table:: 
   :file: languageTag.csv
   :header-rows: 1

This is interpreted as::

    DCTAP instance
        Shape
            shapeID                  default
            Statement Template
                propertyID           :status
                valueConstraint      ['fr']
                valueConstraintType  languagetag
            Statement Template
                propertyID           :status
                valueConstraint      ['fr', 'fr-CA']
                valueConstraintType  languagetag
