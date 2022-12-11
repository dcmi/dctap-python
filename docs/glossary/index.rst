.. _model_glossary:

DCTAP Glossary
--------------

.. glossary::

   Application Profile
       A description of the models, vocabularies, and usage patterns that are expected or required to be found in :term:`Instance Data`. An application profile that follows the :doc:`/model/index` is documented in a :term:`TAP`.
   
   Blank Node
       In RDF, a blank node is a unique identifier used, typically, within the local scope of a specific file or RDF store. As described in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-blank-nodes>`__, a blank node is distinct both from an :term:`IRI` and a :term:`Literal`. Blank nodes are of interest only to users or creators of RDF applications.
   
   Compact IRI
       An IRI represented by an abbreviated syntax in which a label associated with a namespace (the prefix) is followed by a colon and by a local name which, taken together, can be expanded into a full IRI. For example, if the prefix "dcterms:" is associated with the namespace "http://purl.org/dc/terms/", then the prefixed name "dcterms:creator" can be expanded into "http://purl.org/dc/terms/creator".

   CSV File
        A text file in which data values are delimited with commas or with other standard punctuation.
   
   Datatype
       As per `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-Datatypes>`__, a datatype is used to tag a :term:`Literal` as being a specific type of date or number or, by default, just a plain string. In RDF, datatypes are identified with :term:`IRI`\s.

   DCTAP Element
       One of a dozen or so labels defined in the DCTAP Model, such as `propertyID`, `valueConstraint`, and `shapeLabel`, used as column headers in a CSV.

   Description
       A set of Statements in :term:`Instance Data` used to describe just one real-world :term:`Entity`.
   
   Entity
       Something, typically in the real world, that is described by :term:`Instance Data`.
   
   Instance Data
       Records or, more recently, "graphs" that carry Descriptions, traditionally on paper but now, more typically, on the Web.
   
   IRI
       An `Internationalized Resource Identifier <https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier>`_ is a Web-based identifier that builds on and expands the `Uniform Resource Identifier <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_ (URI), and is used, for our purposes, to provide the Properties, Entities, and other components of Instance Data, with identity within the globally managed context of the Web.
   
   Language Tag
       A language tag is an abbreviated name for a natural language, such as ``fr`` for French or ``fr-CA`` for Canadian French. Language tags are used to identify the language of a :term:`Literal`. Standard sets of language tags serve as a controlled vocabulary of identifiers for languages.

   Literal
       Along with :term:`IRI` and :term:`Blank Node`, Literal is one of the three allowable node types defined in the abstract syntax of RDF. For the purposes of DCTAP, it is close enough to think of literals as strings. Literals are used for values such as strings, numbers, and dates. Interested readers can learn more about how literals relate to "lexical forms", :term:`Datatype`\s, and :term:`Language Tag`\s by consulting `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal>`__.

   Picklist
       A controlled list of valid options, one of which can be picked.

   Picklist Element
       A :term:`DCTAP Element`, the values of which must be selected from a :term:`Picklist`.

   Property
       A controlled term in :term:`Instance Data` denoting an attribute of an Entity referenced in a Statement.
   
   Predicate Constraint
       A pattern in an :term:`Application Profile` descriptive of how a given :term:`Property` is expected to be used in :term:`Instance Data`. Also commonly referred to as a Property Constraint.
   
   Shape 
       A component in an :term:`Application Profile` (aka :term:`TAP`) that holds a set of :term:`Statement Template`\s. In the now-superseded `DCMI Abstract Model <https://www.dublincore.org/specifications/dublin-core/abstract-model/>`_ of 2007, these were called Description Templates.
   
   Statement
       A property-value pair in :term:`Instance Data` used in a Description to make claims about an Entity.
   
   Statement Template 
       A component in an :term:`Application Profile` that describes a :term:`Statement` expected to be found in :term:`Instance Data`.
   
   TAP
       A "TAP" (for "tabular application profile") is a single instance of an :term:`Application Profile` that follows the :doc:`/model/index` and is typically serialized as a spreadsheet or :term:`CSV File`.
   
   URI
       See :term:`IRI`.
   
   Value
       A value in :term:`Instance Data` associated with a :term:`Property` in the context of a :term:`Statement`.
   
   Value Constraint
       A pattern in an :term:`Application Profile` descriptive of :term:`Value`\s expected in :term:`Instance Data`.
   
   Vocabulary
       A set of Properties and other terms used in :term:`Instance Data` and referred to in constraints defined in an :term:`Application Profile`. By convention, all properties referenced in a Dublin-Core-style Application Profile are defined and documented separately from the profile itself.

