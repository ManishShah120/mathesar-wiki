---
title: Usage of Foreign Key Constraints
description: 
published: true
date: 2021-10-22T09:07:13.619Z
tags: 
editor: markdown
dateCreated: 2021-10-19T09:20:55.088Z
---

# Context
This design spec describes the proposed solution for the problem defined in the issue [Design for using Foreign Key constraints](https://github.com/centerofci/mathesar/issues/243).

## Prototype Walkthrough
[Video](https://www.loom.com/share/146b0aa3adbb41009ce1a49caeb936ab)
[Prototype Link](https://mathesar-prototype.netlify.app/)

## Scenarios
A user has a table named 'artist' that contains records for artists in a music album collection. The user wants to link each artist to records in another table named 'track.' If successful, the user should relate all tracks associated with an artist to each record in the 'artist' table.

### The user opens the 'track' table and adds a new column to link records from the 'artist' table
- From the sidebar navigation list of tables, click on a table named 'track.'
- Click on 'Add new Column,' and a new column is added with text type by default
### The user opens the new column menu and selects the 'Link to Another Table' option
- Click on the column header to show the menu and select the 'Link to Another Table' option

**Note: This step does not cover the scenario where a user has a unique table, in which case they need to create an additional table to add a relationship.**


### The user selects a table from the list of available tables
- The user selects the table on the 'one side of the 'one-to-many' relationship.

### The user selects a column belonging to the selected table to create the link
- The primary key column is pre-selected by default
### The user sets the new column as a foreign key for a column in the 'artist' table
- If the column had values, this action would clear those unless they exactly matched contents from the linked column
### The user retrieves records from the linked table and adds them to the new column
- Autocomplete should allow users to complete this action without additional clicks
- When no results are available, we should show an option to add a new record
### The user removes the foreign key constraint from the column
- The system will assign the column the type of the column that was linked (if the linked column was a duration type, then it should be assigned as such)