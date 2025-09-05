# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-09-05

### Changed
- Updated installation steps

## [1.1.0] - 2025-09-05

### Added
- Appliance Type field for ISD-AS with CORE and EDGE options
- Advanced filtering interface for all list pages (Organizations, ISD-ASes, SCION Link Assignments)
- Filter forms with search, dropdown filters, and tag filtering support
- Dedicated Appliances management section in ISD-AS detail pages

### Changed
- Renamed "Core Nodes" to "Appliances" throughout the UI for consistency
- Improved user experience with dedicated appliance management section

### Fixed
- Filter sidebar now displays correctly on all list pages with proper NetBox integration
- Appliance dropdown now properly loads when ISD-AS is selected

## [1.0.0] - 2025-09-03

### Added
- Complete NetBox SCION plugin with Organizations, ISD-ASes, and SCION Link Assignments
- Dynamic CORE dropdown based on ISD-AS selection
- Relationship types (PARENT/CHILD/CORE) for link classification
- Full REST API with CRUD operations
- Export functionality (CSV/Excel)
- Audit logging and change tracking
- Available on PyPI for easy installation

### Fixed
- Improved form validation and error messages
- Better dropdown functionality and user experience

## [0.1.0] - 2025-08-31

### Added
- Initial plugin release
- Zendesk ticket integration with clickable links
- CORE database models and API structure
