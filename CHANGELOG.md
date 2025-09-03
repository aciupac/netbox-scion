# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-09-03

### Added
- Production-ready NetBox SCION plugin
- Organization model for managing SCION operators
- ISDAS model for tracking ISD-AS identifiers
- SCIONLinkAssignment model with dynamic core dropdown functionality
- Relationship field (PARENT/CHILD/CORE) for link classification
- Tom Select integration for enhanced dropdown user experience
- Full REST API support for all models
- Web interface with filtering and search capabilities
- Export functionality (CSV/Excel)
- Audit logging for all models
- Database migrations with safe upgrade path
- Published on PyPI for easy installation

### Fixed
- Core dropdown now properly populates based on ISD-AS selection
- Form validation works correctly with dynamic dropdown values
- Error messages show proper field labels (e.g., "ISD-AS" instead of "Isd as")

## [0.1.0] - 2025-08-31

### Added
- Initial development release
- Zendesk ticket integration with clickable links
- PostgreSQL ArrayField support for core nodes
- Comprehensive test coverage
- API documentation
