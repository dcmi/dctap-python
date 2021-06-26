.. _model:

DCTAP Model and Glossary
------------------------

:term:`Instance Data`, whether in the form of
metadata records, databases, or networked
graphs such as Wikidata, typically makes
statements about things "in the world" ---
books, their authors, viruses, buildings, and
the like. A single :term:`Statement` consists
of a :term:`Property`-:term:`Value` pair. A
set of statements about a distinct entity in
the world is referred to here as as a
:term:`Description`. Because a given body of
Instance Data may describe multiple things in
the world, it may be said to consist of
multiple Descriptions.

An :term:`Application Profile` (here: DCTAP
Instance) enumerates the properties and
characterizes the values that are expected to
be found in a given body of Instance Data. In
effect, an Application Profile is a
description of a description. This is, alas,
inherently confusing.

In order to minimize that confusion, the
DCTAP Model names the things "in Instance
Data" differently from the things "in an
Application Profile", as summarized in the
table and glossary below.

In an Application Profile, a Statement in
Instance Data is described with a
:term:`Statement Constraint`, and a
Property-Value pair is described with a
:term:`Property Constraint` and
:term:`Value Constraint`. A
Description in Instance Data about a 
distinct entity in the world is described in 
an application profile with a :term:`Shape`.
Where a Description in Instance Data groups a 
set of Statements, a Shape groups a set of 
Statement Constraints.

The DCTAP Model consists of a dozen or so 
"elements" related to Shapes and Statement 
Constraints. Concretely, a :term:`DCTAP Element`
serves as a header for a column in a tabular 
application profile.

Because the DCTAP Model was designed for
compatibility with RDF and Linked Data,
property constraints, shapes, and some value
constraints are represented in a DCTAP
Instance with an :term:`IRI` (or
:term:`Compact IRI`).

.. csv-table:: 
   :file: DCTAP_Model.csv
   :header-rows: 1

.. glossary::

   Application Profile
       A description of the structures and terms, and their 
       usages, expected to be found **in Instance Data**.
   
   Compact IRI
       An IRI represented by an abbreviated syntax in which
       a label associated with a namespace (the prefix) is
       followed by a colon and by a local name which, taken
       together, can be expanded into a full IRI. For
       example, if the prefix ``dcterms:`` is associated with
       the namespace ``http://purl.org/dc/terms/``, then the
       prefixed name ``dcterms:creator`` can be expanded into
       ``http://purl.org/dc/terms/creator``.
   
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

