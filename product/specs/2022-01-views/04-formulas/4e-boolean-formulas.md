---
title: (e) Boolean Formulas
description: 
published: true
date: 2022-02-26T00:16:22.678Z
tags: 
editor: markdown
dateCreated: 2022-02-26T00:16:22.678Z
---

These formulas operate on boolean types. They are based on PostgreSQL [logical operators](https://www.postgresql.org/docs/9.1/functions-logical.html).

# And
Compares values to see if both are true. See this table for return values:

| a | b | a AND b |
|-|-|-|
| TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE |
| TRUE | NULL | NULL |
| FALSE | FALSE | FALSE |
| FALSE | NULL | FALSE |
| NULL | NULL | NULL |


- **Date Type**: Boolean
- **Variables Accepted**:
    - **Boolean 1**:
        - **Type**: Single Record Boolean-Like
        - **Description**: First boolean
    - **Boolean 2**:
        - **Type**: Single Record Boolean-Like
        - **Description**: Second boolean
- **Editable?**: No
- **PostgreSQL Mapping**: `AND` operator

# Not
Returns the opposite boolean value of the input value.

- **Date Type**: Boolean
- **Variables Accepted**:
    - **Boolean**:
        - **Type**: Single Record Boolean-Like
        - **Description**: Input boolean
- **Editable?**: No
- **PostgreSQL Mapping**: `NOT` operator

# Or
Compares values to see if either one is true. See this table for return values:

| a | b | a OR b |
|-|-|-|
| TRUE | TRUE | TRUE |
| TRUE | FALSE | TRUE |
| TRUE | NULL | TRUE |
| FALSE | FALSE | FALSE |
| FALSE | NULL | NULL |
| NULL | NULL | NULL |

- **Date Type**: Boolean
- **Variables Accepted**:
    - **Boolean 1**:
        - **Type**: Single Record Boolean-Like
        - **Description**: First boolean
    - **Boolean 2**:
        - **Type**: Single Record Boolean-Like
        - **Description**: Second boolean
- **Editable?**: No
- **PostgreSQL Mapping**: `OR` operator