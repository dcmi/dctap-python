.. _model:

DCTAP Model
-----------

.. csv-table:: 
   :file: DCTAP_Model.csv
   :header-rows: 1

:term:`Instance Data`, whether in the form of metadata records, databases, or networked graphs such as Wikidata, typically makes statements about things "in the world" --- books, their authors, viruses, buildings, and the like. A single :term:`Statement` consists of a :term:`Property`-:term:`Value` pair. A set of statements about a distinct entity in the world is referred to here as as a :term:`Description`. Because a given body of Instance Data may describe multiple things in the world, it may be said to consist of multiple Descriptions.

An :term:`Application Profile` (here: DCTAP Instance) enumerates the properties and characterizes the values that are expected to be found in a given body of Instance Data. In effect, an Application Profile is a description of a description. This is, alas, inherently confusing.

In order to minimize that confusion, the DCTAP Model names the things "in Instance Data" differently from the things "in an Application Profile", as summarized in the table and glossary below.

In an Application Profile, a Statement in Instance Data is described with a :term:`Statement Constraint`, and a Property-Value pair is described with a :term:`Property Constraint` and :term:`Value Constraint`. A Description in Instance Data about a distinct entity in the world is described in an application profile with a :term:`Shape`. Where a Description in Instance Data groups a set of Statements, a Shape groups a set of Statement Constraints.

The DCTAP Model consists of twelve "elements" related to Shapes and Statement Constraints. Concretely, a :term:`DCTAP Element` serves as a header for a column in a tabular application profile. As described in the section :ref:`elements`, the DCTAP model has twelve elements related to the structure of Shapes, the structure of Statement Contraints, or of an annotational nature.

Because the DCTAP Model was designed for compatibility with RDF and Linked Data, property constraints, shapes, literal datatypes and some value constraints are represented in a DCTAP Instance with :term:`IRI`\s (or :term:`Compact IRI`\s).

Minimal application profile
...........................

In the DCTAP model, the simplest possible application profile consists of just one :term:`Statement Constraint` in the context of one :term:`Shape`.

A Statement Constraint has, at a minimum, one **propertyID** element, and the existence of a Shape can be inferred, so in practical terms, the simplest possible application profile is a list of just one property.

Note that if a shape identifier is not explicitly assigned in a CSV, a default identifier will be assigned. (This is discussed in the the section :ref:`elem_shapeID`.) In "shape-less" applications, this shape identifier can simply be ignored.

.. csv-table:: 
   :file: propertyID_only.csv
   :header-rows: 1

Interpreted as::

    DCTAP instance
	Shape
	    shapeID: :default
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/title
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/publisher
	    Statement Constraint
		propertyID: https://schema.org/creator
	    Statement Constraint
		propertyID: http://purl.org/dc/terms/date

