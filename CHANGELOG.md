# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2025-10-07

### Added
- "Create & Add Another" button now maintains ISD-AS value and auto-increments interface ID when creating multiple SCION Link Assignments
- ISD-ASes section header on Organization detail page is now a clickable link that filters the ISD-AS list by that organization

### Fixed
- Fixed appliance field not auto-selecting existing value when editing a SCION Link Assignment
- Fixed peer field unique constraint to only validate non-empty values, allowing multiple links with empty peer field for the same ISD-AS (migration 0018)

## [1.3.0] - 2025-10-01

### Added
- `comments` field (free-form internal notes) added to Organization, ISD-AS, and SCION Link Assignment models (migration 0011)
- Added Peer column (ISD-AS#IFID) to SCION Link Assignments table within ISD-AS detail view
- Linkified "SCION Link Assignments" section header on ISD-AS detail page to filtered list view
- `local_underlay` and `peer_underlay` optional fields with validation (IPv4 / IPv6, bracketed form `[addr]:port`) (migration 0015)
- Mandatory `status` field (Reserved / Active / Planned) for SCION Link Assignments with existing rows defaulted to Active (migration 0016)
- UI color-coded badges for Status (Active / Reserved / Planned) and Relationship (CORE / CHILD / PARENT)

### Changed
- Renamed `zendesk_ticket` field to generic `ticket` (migration 0012) removing numeric-only constraint
- Expanded `ticket` field capacity and interpret arbitrary input heuristically as URL (migration 0013); values render as clickable hyperlinks when they appear to be (or are normalized into) URLs
- Made `peer_name` and `peer` fields optional for SCION Link Assignments (migration 0014)

### Fixed
- Serializer exposure for new `comments` fields
- Exposed `status`, `local_underlay`, `peer_underlay`, `comments` fields on SCION Link Assignment form
- Renamed form label to "Ticket" (was "External Reference / URL")
- Restored plugin changelog pages by providing the `model` kwarg to `ObjectChangeLogView` routes and aligning their base templates with the corresponding detail pages.

### Removed
- Removed `customer_id` field from SCION Link Assignments (migration 0017)

## [1.2.0] - 2025-09-09
### Added
- Added `peer` field to SCIONLinkAssignment model with unique constraint per ISD-AS
- Added peer field validation with descriptive help text showing format: `{isd}-{as}#{interface_number}` (e.g., `1-ff00:0:110#1` or `1-1#1`)
- Auto-deletion of ISD-ASes when parent organization is deleted (changed foreign key from PROTECT to CASCADE)

### Changed
- **BREAKING:** Renamed `customer_name` field to `peer_name` in SCIONLinkAssignment model
- **BREAKING:** Renamed `cores` field to `appliances` in ISD-AS model
- **BREAKING:** Removed `appliance_type` field from ISD-AS model - appliances are now generic without type distinction
- Updated all UI labels from "Customer Name" to "Peer Name" and "Core" to "Appliance"
- Updated API serializers, admin interface, search functionality, and templates to use new field names
- Improved database migration with proper schema cleanup for removed Organization peer field

### Fixed
- Fixed database schema inconsistencies where Organization table had unwanted peer column
- Fixed AttributeError when accessing customer_name field by updating all code references to peer_name
- Fixed migration issues with unique constraints on empty values

## [1.1.2] - 2025-09-05

### Fixed
- Fixed missing filter buttons on all list pages (Organizations, ISD-AS, SCION Links)
- Fixed NoReverseMatch errors when organization field is null/empty
- Fixed corrupted detail templates causing Django template syntax errors
- Fixed ListView template references to use proper NetBox list templates
- Added null value protection for organization field references in templates
- Made Interface ID column clickable in SCION Link Assignment table

### Changed
- Improved table rendering with graceful handling of null organization fields
- Enhanced navigation between ISD-AS and SCION Link Assignment detail pages
- Updated package naming to be PEP 625 compliant (netbox_scion instead of netbox-scion)

## [1.1.1] - 2025-09-05

### Changed
- Updated installation documentation and deployment instructions

## [1.1.0] - 2025-09-05

### Added
- Appliance Type field for ISD-AS with CORE and EDGE options
- Advanced filtering interface for all list pages with search, dropdown filters, and tag support
- Dedicated Appliances management section in ISD-AS detail pages

### Changed
- Renamed "Core Nodes" to "Appliances" throughout the UI for consistency

### Fixed
- Filter sidebar now displays correctly on all list pages with proper NetBox integration
- Appliance dropdown now properly loads when ISD-AS is selected

## [1.0.0] - 2025-09-03

### Added
- Complete NetBox SCION plugin with Organizations, ISD-ASes, and SCION Link Assignments
- Dynamic appliance dropdown based on ISD-AS selection
- Relationship types (PARENT/CHILD/CORE) for link classification
- Full REST API with CRUD operations, filtering, and pagination
- Export functionality (CSV/Excel)
- Audit logging and change tracking
- PyPI package distribution for easy installation

### Fixed
- Improved form validation and error messages
- Enhanced dropdown functionality and user experience

## [0.1.0] - 2025-08-31

### Added
- Initial plugin release with core functionality
- Zendesk ticket integration with clickable links
- Basic database models and API structure

---

[Unreleased]: https://github.com/aciupac/netbox-scion/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/aciupac/netbox-scion/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/aciupac/netbox-scion/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/aciupac/netbox-scion/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/aciupac/netbox-scion/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/aciupac/netbox-scion/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/aciupac/netbox-scion/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/aciupac/netbox-scion/releases/tag/v0.1.0
