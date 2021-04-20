---
title: Feature Ideas
description: Ideas for features that aren't in our roadmap yet.
published: true
date: 2021-04-20T19:49:02.448Z
tags: 
editor: markdown
dateCreated: 2021-04-20T19:47:31.098Z
---

These are potential feature ideas for Mathesar that are not on our [Roadmap](/development/roadmap) yet. Each section represents a conceptual grouping of features.
> 
> We are still finalizing the roadmap and it is expected to change significantly over the next few weeks. This notice will be removed when the roadmap is more stable.
{.is-warning}


## Additional Imports
Users should be able to import data in the following additional formats:
- SQL
- JSON
- XML
- Google Sheets import (via API)
- Excel file upload
- Excel web import (via API)
- Apple Numbers file upload
- Collabora import
- Airtable

## Location Type
- Add new type, using existing PostGIS type where possible:
	- Location
- Autodetect this type during import
- Allow user to change columns to this type
- Add additional grouping options:
	 Street Address
	 Country
	 Administrative Area Level 1 *(in the US, these are states)*
	 Administrative Area Level 2 *(in the US, these are counties)*
	 Administrative Area Level 3
	 Administrative Area Level 4
	 Administrative Area Level 5
	 Locality *(city/town)*
	 Sublocality *(subdivision of city/town)*
	 Neighborhood
	 Postal Code
	 Latitude
	 Longitude

The attributes of the location column type are based on results returned by the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview), Since they\'ve done the work of putting addresses into a global format.

## Phone Number Type
- Add new type
	- Phone Number
- Autodetect this type during import
- Allow user to change columns to this type
- Add grouping options:
	- Country Code
	- Area Code

## Additional Fields
- File field (for images, attachments, etc.)
- IP Address field
- Formula field (use of spreadsheet like formulas)
- JSON field

## Additional Views
- Map view
- Card (Gallery) view
- Kanban view
- Data modeling view (of entire schema or database)

## Forms
- Create forms that allow users to enter data into views

## Data Syncing
Users should be able to sync data both ways from:
- Google Sheets
- Airtable
- Excel (web)
- Airbyte connectors?

## Data Suggestions
Users should get suggestions about:
- Visualizations they can apply to their data
- Aggregations they can apply to their data
- Schema imporovements they can make to their data

## Versioning
Users should be able to:
- Save a snapshot of their database, schema, or table.
- Revert to a previous version of their database, schema, or table.
- Undo and redo recent actions.

## Events
Events in the system should be exposed via an API. e.g.
- New table created
- Table schema changed
- New data added

## Notifications
Users should be able to:
- Get email notifications of various events.
- Get web notifications of various events.

## Templates
Users should be able to:
- Save databases, schemas, applications as templates.
- Use a template to create a new database, schema, or application.
- Edit template attributes.
- Delete a template.
- Browse existing templates.
- Search for templates.

## Improved User Management
Users should be able to:
- Create teams of users, teams can have similar permissions to users.

## API
- API key management
- API documentation

## Freeform Data Support
- UI to handle freeform data (JSON) well
- Suggest conversion of non-tabular data to tabular data based on schema
- Automatically generate appropriate tabular data if consistency exists in imported freeform data

## SQL Exploration
- Run SQL from the web interface

## Comments
- Comment on data