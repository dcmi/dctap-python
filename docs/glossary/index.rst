.. _model_glossary:

Glossary
--------

.. glossary::

   Application Profile
       A description of the structures and terms, and their usages, expected to be found **in Instance Data**. An application profile that follows the DCTAP model is called a :term:`DCTAP Instance`.
   
   Blank Node
       In RDF, a blank node is a unique identifier used, typically, within the local scope of a specific file or RDF store. As described in `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-blank-nodes>`__, a blank node is distinct both from an :term:`IRI` and a :term:`Literal`. Blank nodes are of interest only to users or creators of RDF applications.
   
   Compact IRI
       An IRI represented by an abbreviated syntax in which a label associated with a namespace (the prefix) is followed by a colon and by a local name which, taken together, can be expanded into a full IRI. For example, if the prefix "dcterms:" is associated with the namespace "http://purl.org/dc/terms/", then the prefixed name "dcterms:creator" can be expanded into "http://purl.org/dc/terms/creator".
   
   Datatype
       As per `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-Datatypes>`__, a datatype is used to tag a :term:`Literal` as being a specific type of date or number or, by default, just a plain string. In RDF, datatypes are identified with :term:`IRI`\s.

   DCTAP Element
       One of a dozen or so labels defined in the DCTAP Model, such as `propertyID`, `valueConstraint`, and `shapeLabel`, used as column headers in a CSV.
   
   DCTAP Instance 
       An Application Profile that follows the DC Tabular Application Profiles Model, typically serialized as a CSV file.
   
   Description
       A set of Statements **in Instance Data** used to describe just one real-world :term:`Entity`.
   
   Entity
       Something, typically **in the real world**, that is described by Instance Data.
   
   Instance Data
       Records or, more recently, "graphs" that carry Descriptions, traditionally on paper but now, more typically, on the Web.
   
   IRI
       An `Internationalized Resource Identifier <https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier>`_ is a Web-based identifier that builds on and expands the `Uniform Resource Identifier <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_ (URI), and is used, for our purposes, to provide the Properties, Entities, and other components of Instance Data, with identity within the globally managed context of the Web.
   
   Language Tag
       A language tag is an abbreviated name for a natural language, such as ``fr`` for French or ``fr-CA`` for Canadian French. Language tags are used to identify the language of a :term:`Literal`. Standard sets of language tags serve as a controlled vocabulary of identifiers for languages.

   Literal
       Along with :term:`IRI` and :term:`Blank Node`, Literal is one of the three allowable node types defined in the abstract syntax of RDF. For the purposes of DCTAP, it is close enough to think of literals as strings. Literals are used for values such as strings, numbers, and dates. Interested readers can learn more about how literals relate to "lexical forms", :term:`Datatype`\s, and :term:`Language Tag`\s by consulting `RDF 1.1 Concepts and Abstract Syntax <https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal>`__.

   Property
       A controlled term **in Instance Data** denoting an attribute of an Entity used in a Statement.
   
   Property Constraint
       A pattern **in an Application Profile** descriptive of how Properties are expected to be used in Instance Data.
   
   Shape 
       A set of Statement Constraints **in an Application Profile** that characterize Statements expected to be found in a Description. In the now-superseded `DCMI Abstract Model <https://www.dublincore.org/specifications/dublin-core/abstract-model/>`_ of 2007, these were called Description Templates.
   
   Statement
       A property-value pair **in Instance Data** used in a Description to make claims about an Entity.
   
   Statement Constraint 
       A pattern **in an Application Profile** descriptive of Statements expected to be found in Instance Data.
   
   URI
       See :term:`IRI`.
   
   Value
       A value **in Instance Data** associated with a Property in the context of a Statement.
   
   Value Constraint
       A pattern **in an Application Profile** descriptive of Values expected in Instance Data.
   
   Vocabulary
       A set of Properties and other terms used **in Instance Data** and referred to in constraints defined in an Application Profile. By convention, all properties referenced in a DC Application Profile are defined and documented separately from the profile itself.

