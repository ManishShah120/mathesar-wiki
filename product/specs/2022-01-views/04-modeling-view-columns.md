---
title: Views: Modeling View Columns
description: 
published: true
date: 2022-01-24T22:56:32.776Z
tags: 
editor: markdown
dateCreated: 2022-01-24T22:56:32.776Z
---

Here's how I think we should model view columns in our API and UI. Each heading represents an attribute of a View Column.

### Data Type
- **Definition**: This is the final data type of the content of the column after any computations etc. are applied.
- **Allowed values**: same as Table data types.
- **Required**. Data type should always be set, at the very least, we can treat unknown data types as text.

### Sources
 - **Definition**: This is the set of source columns that are used to generate the data in the current View column.
- **Allowed values**: references to other Table or View columns, including other columns in the same View.
- **Optional**: This could be empty for purely calculated columns (e.g. using the Postgres `random()` function and putting the output in a column)

Using Element's UI as an example (Matrix channel names stand in for data sources here), here's how Sources might be represented:

![Sources image](/assets/product/specs/2022-01-views/04-modeling-view-columns/Screen Shot 2022-01-20 at 4.21.05 PM.png)

### Formula
- **Definition**: This is the formula used to generate data in for this column.
- **Allowed values**: SQL function + operators
- **Optional**: Columns that are direct copies of other columns from tables or views won't have a formula.

We should allow users to either use a pre-set set of formulas or (in the future) enter a custom formula using whatever functions are installed on their Postgres database.

Using Element's UI as an example (Matrix channel names stand in for data sources here), here's how a Formula might be represented. Note that Sources are used within the Formula.

![Sources image](/assets/product/specs/2022-01-views/04-modeling-view-columns/Screen Shot 2022-01-20 at 4.23.21 PM.png)

### Link
- **Definition**: This notes whether a column is a join column. This is a column used to match the same values across multiple tables to create the View. These columns have multiple Sources but no Formula.
- **Allowed values**: True or False.
- **Required**: This must be set for all columns.

In [this example View](https://www.w3resource.com/sql/creating-views/create-view-with-join.php), the `agent_code` and `cust_code` columns are Links.