# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-09-09

### Added
- Added `peer` field to SCIONLinkAssignment model with unique constraint per ISD-AS
- Added peer field validation with descriptive help text showing format: '{isd}-{as}#{interface_number}' (e.g., '1-ff00:0:110#1' or '1-1#1')
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
