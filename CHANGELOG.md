# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-09-04

### Added
- Dedicated CORE management section in ISD-AS detail pages for better visibility and control
- Add, edit, and remove CORE operations with cascade deletion of associated SCION links
- Improved CORE visibility with dedicated management interface

### Changed
- Simplified CORE field input to use comma-separated text format for better compatibility
- Reverted to basic filtering functionality
- Maintained all existing model functionality and data compatibility
- Moved CORE management from forms to dedicated section for improved user experience

### Fixed
- Enter key properly adds CORE tags instead of submitting the form
- Filter sidebar now displays correctly on all list pages
- Multiple COREs can be added without form interference
- Form validation errors that prevented SCION link creation
- Optional zendesk ticket field to allow creation without ticket reference

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
