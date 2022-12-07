.. _model:

DCTAP Model
-----------

.. csv-table:: 
   :file: DCTAP_Model.csv
   :header-rows: 1

:term:`Instance Data`, whether in the form of metadata records, databases, or networked graphs such as Wikidata, typically makes statements about things "in the world" --- books, their authors, viruses, buildings, and the like. A single :term:`Statement` consists of a :term:`Property`-:term:`Value` pair. A set of statements about a distinct entity in the world is referred to here as as a :term:`Description`. Because a given body of Instance Data may describe multiple things in the world, it may be said to consist of multiple Descriptions.

An :term:`Application Profile` (here: DCTAP Instance) enumerates the properties and characterizes the values that are expected to be found in a given body of Instance Data. In effect, an Application Profile is a description of a description. This is, alas, inherently confusing.

In order to minimize that confusion, the DCTAP Model names the things "in Instance Data" differently from the things "in an Application Profile", as summarized in the table and glossary below.

In an Application Profile, a Statement in Instance Data is described with a :term:`Statement Template`, and a Property-Value pair is described with a :term:`Predicate Constraint` and :term:`Value Constraint`. A Description in Instance Data about a distinct entity in the world is described in an application profile with a :term:`Shape`. Where a Description in Instance Data groups a set of Statements, a Shape groups a set of Statement Templates.

The DCTAP Model consists of twelve "elements" related to Shapes and Statement Templates. Concretely, a :term:`DCTAP Element` serves as a header for a column in a tabular application profile. As described in the section :ref:`elements`, the DCTAP model has twelve elements related to the structure of Shapes, the structure of Statement Contraints, or of an annotational nature.

Because the DCTAP Model was designed for compatibility with RDF and Linked Data, property constraints, shapes, literal datatypes and some value constraints are represented in a DCTAP Instance with :term:`IRI`\s (or :term:`Compact IRI`\s).

.. toctree::
   :hidden:

   minimum_profile/index
