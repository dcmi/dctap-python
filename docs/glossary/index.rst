.. _model_glossary:

Glossary
--------

.. glossary::

   Application Profile
       A description of the structures and terms, and their 
       usages, expected to be found **in Instance Data**.
       An application profile that follows the DCTAP model 
       is called a :term:`DCTAP Instance`.
   
   Compact IRI
       An IRI represented by an abbreviated syntax in which
       a label associated with a namespace (the prefix) is
       followed by a colon and by a local name which, taken
       together, can be expanded into a full IRI. For
       example, if the prefix "dcterms:" is associated with
       the namespace "http://purl.org/dc/terms/", then the
       prefixed name "dcterms:creator" can be expanded into
       "http://purl.org/dc/terms/creator".
   
   DCTAP Element
       One of a dozen or so labels defined in the DCTAP Model,
       such as `propertyID`, `valueConstraint`, and `shapeLabel`,
       used as column headers in a CSV.
   
   DCTAP Instance 
       An Application Profile that follows the DC Tabular
       Application Profiles Model, typically serialized as a
       CSV file.
   
   Description
       A set of Statements **in Instance Data** used to
       describe just one real-world :term:`Entity`.
   
   Entity
       Something, typically **in the real world**, that is
       described by Instance Data.
   
   Instance Data
       Records or, more recently, "graphs" that carry
       Descriptions, traditionally on paper but now, more
       typically, on the Web.
   
   IRI
       An `Internationalized Resource Identifier
       <https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier>`_
       is a Web-based identifier that builds on and expands 
       the
       `Uniform Resource Identifier <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_ (URI), 
       and is used, for our purposes, to provide the
       Properties, Entities, and other components of
       Instance Data, with identity within the globally 
       managed context of the Web.
   
   Property
       A controlled term **in Instance Data** denoting an
       attribute of an Entity used in a Statement.
   
   Property Constraint
       A pattern **in an Application Profile** descriptive 
       of how Properties are expected to be used in Instance 
       Data.
   
   Shape 
       A set of Statement Constraints **in an Application Profile** 
       that characterize Statements expected to be found in 
       a Description. In the now-superseded `DCMI Abstract 
       Model
       <https://www.dublincore.org/specifications/dublin-core/abstract-model/>`_ of 2007,
       these were called Description Templates.
   
   Statement
       A property-value pair **in Instance Data** used in a
       Description to make claims about an Entity.
   
   Statement Constraint 
       A pattern **in an Application Profile** descriptive
       of Statements expected to be found in Instance Data.
   
   URI
       See :term:`IRI`.
   
   Value
       A value **in Instance Data** associated with a
       Property in the context of a Statement.
   
   Value Constraint
       A pattern **in an Application Profile** descriptive of 
       Values expected in Instance Data.
   
   Vocabulary
       A set of Properties and other terms used **in
       Instance Data** and referred to in constraints
       defined in an Application Profile. By convention, all
       properties referenced in a DC Application Profile are
       defined and documented separately from the profile
       itself.

