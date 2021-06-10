DCTAP Model
-----------

To understand the DCTAP model, one must understand how an instance of the DCTAP model (here: DCTAP Instance) relates to data (here: Instance Data) and how that data relates to the real world.

Instance Data typically describes things that are "in the world"; we call those things Entities. Application Profiles describe that data. A CSV that follows the DCTAP model, or DCTAP Instance, is an Application Profile.

The distinction between things "in the data" and things "in the profile" is summarized in the following table:

.. csv-table:: 
   :file: dctap_model.csv
   :header-rows: 1

Things "in the world":

- Entity: something described by the Instance Data

Things "in the data":

- Statement: a property-value pair that describes an Entity
  - Property: an attribute of an Entity
  - Value: a data value associated with a Property in the Instance Data

Things "in the profile":

- Shape: a pattern for data about a given Entity
  - Statement Constraint: a pattern for Statements in the data
    - Property Constraint: a pattern for Properties in the data
    - Value Constraint: a pattern for Values in the data
