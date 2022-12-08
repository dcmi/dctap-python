.. _model:

DCTAP Model
-----------

.. csv-table:: 
   :file: DCTAP_Model.csv
   :header-rows: 1

:term:`Instance Data`, whether in the form of metadata records, databases, or networked graphs such as Wikidata, typically makes statements about things "in the world" --- books, their authors, viruses, buildings, and the like. A single :term:`Statement` consists of a :term:`Property`-:term:`Value` pair. A set of statements about a distinct entity in the world is referred to here as as a :term:`Description`. Because a given body of :term:`Instance Data` may describe multiple things in the world, it may be said to consist of multiple :term:`Description`\s.

An :term:`Application Profile` (here: a :term:`TAP`) enumerates the properties and characterizes the values that are expected to be found in a given body of :term:`Instance Data`. In effect, an Application Profile is a description of a description -- a notion that is inevitably somewhat confusing. To minimize this confusion, the DCTAP Model names the things "in :term:`Instance Data`" differently from the things "in an :term:`Application Profile`" (see table above).

In an :term:`Application Profile`: 
- a :term:`Statement` in :term:`Instance Data` is described with a :term:`Statement Template`;
- a Property-Value pair is described with a :term:`Predicate Constraint` and :term:`Value Constraint`;
- a set of :term:`Statement`\s in :term:`Instance Data` about exactly one real-world :term:`Entity` (aka :term:`Description`) is described in a :term:`Shape`. Where a :term:`Description` in :term:`Instance Data` groups a set of :term:`Statement`\s, a :term:`Shape` groups a set of :term:`Statement Template`\s.

The DCTAP Model consists of :term:`Shape`\s and :term:`Statement Template`\s, each of which consists of :term:`DCTAP Element`\s (a generic term for the column headers in a :term:`CSV File`).

Because the DCTAP Model was designed for compatibility with RDF and Linked Data, property constraints, shapes, literal datatypes, and some value constraints are represented in a :term:`TAP` with :term:`IRI`\s (or :term:`Compact IRI`\s).

.. toctree::
   :hidden:

   minimum_profile/index
