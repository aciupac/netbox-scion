# NetBox SCION Plugin – Technical & Architectural Prompt

This document is a compact, high‑signal technical brief for engineers (human or AI) to quickly understand, reason about, and safely extend the `netbox_scion` plugin. It emphasizes concrete structures, patterns, constraints, and known pitfalls so future changes can be implemented with minimal unintended side effects.

---
## 1. Purpose & Domain
The plugin extends NetBox to model and manage SCION network entities:
- Organizations (SCION operators)
- ISD-AS identifiers ("ISDAS") with a list of appliances (generic endpoints; previously called cores)
- SCION Link Assignments tying an ISD-AS + appliance + interface metadata + peer/customer info + optional generic external ticket/reference (URL or ID)

Provides:
- Web UI (CRUD, list filtering, tables, change logs)
- REST API (DRF via NetBox abstractions) with filtering & counts
- CSV/Excel export via NetBox built-ins

---
## 2. Technology Stack
- Python 3.8–3.11 (per `setup.py` classifiers)
- Django (version governed by NetBox; comments refer to NetBox 3.5+, README says NetBox 4.0+) – mismatch noted below
- NetBox Plugin Framework (generic class-based views, tables, filtersets, plugin config, navigation)
- Django REST Framework via `netbox.api` wrappers (NetBoxModelViewSet, NetBoxModelSerializer)
- django-filter (`NetBoxModelFilterSet`)
- django-tables2 (`NetBoxTable` subclasses)
- PostgreSQL JSONB (`models.JSONField`) for `appliances` lists
- No additional third‑party runtime dependencies beyond NetBox core

---
## 3. Repository Layout (Key Files)
```
netbox_scion/
  __init__.py        # PluginConfig + version constants
  models.py          # Organization, ISDAS, SCIONLinkAssignment
  forms.py           # Model + filter + appliance mgmt forms (dynamic choices)
  filtersets.py      # Searching & field filtering
  tables.py          # django-tables2 table definitions
  views.py           # Web CRUD & custom appliance mgmt actions
  urls.py            # UI URL routes (hyphenated segments for lists; changelog routes pass model via kwargs)
  navigation.py      # Sidebar menu & buttons
  admin.py           # Django admin registrations
  api/
    serializers.py   # DRF serializers (nested + counts)
    views.py         # ViewSets + legacy AJAX endpoint
    urls.py          # API router registrations
  migrations/        # Schema evolution (field renames, constraints)
  tests.py           # Basic model tests (contains a bug, see §15)
```
Deployment helpers under `deployment/` (Docker variants, examples).

---
## 4. Plugin Configuration (`__init__.py`)
Class: `NetBoxScionConfig(PluginConfig)`
- `name = 'netbox_scion'` (must match folder & PLUGINS entry)
- `base_url = 'scion'` → All plugin UI paths: `/plugins/scion/...`
- `urls = 'urls'`, `api_urls = 'api.urls'`
- `default_settings = { 'top_level_menu': True }` toggles menu integration
- Version: `1.3.1` (current)

---
## 5. Data Model Overview (in `models.py`)
### 5.1 Organization
Fields:
- `short_name` (unique, indexed by uniqueness)
- `full_name`
- `description` (optional)
Reverse: `isd_ases` (from ISDAS)
Ordering: `short_name`

### 5.2 ISDAS
Represents SCION ISD-AS identifier.
Fields:
- `isd_as` (unique string; regex: `^\d+-([0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+|\d+)$` supports both full hex triplet and short dash decimal form)
- `description` (optional)
- `organization` (FK CASCADE → Organization) – changed from PROTECT in v1.3.0
- `appliances` (JSON list, default `[]`) – renamed from `cores`
Helpers:
- `appliances_display` property (comma join)
Ordering: `isd_as`

### 5.3 SCIONLinkAssignment
Represents an interface assignment.
Key Fields (v1.3.0+):
- `isd_as` (FK CASCADE)
- `core` (text; UI label "Appliance" – legacy internal name)
- `interface_id` (PositiveInteger; unique within an ISD-AS)
- `relationship` (enum: PARENT / CHILD / CORE)
- `status` (enum: ACTIVE / RESERVED / PLANNED; default ACTIVE)
- `customer_id` (required at model layer; forms suggest optionality – mismatch to address)
- `peer_name` (optional)
- `peer` (optional identifier; uniqueness enforced per ISD-AS when non-blank; format guidance only)
- `local_underlay`, `peer_underlay` (optional `ip:port`; IPv4 or IPv6 with bracketed `[addr]:port` support; validated in `clean()`)
- `ticket` (generic external reference; any string accepted; heuristically linkified via `get_ticket_url()`)
- `comments` (free-form notes)
Constraints: Unique(`isd_as`, `interface_id`) & Unique(`isd_as`, `peer`).
Method: `get_ticket_url()` – best-effort URL normalization.
Ordering: (`isd_as`, `interface_id`)

### 5.4 NetBoxModel Inheritance
All three models inherit from `netbox.models.NetBoxModel` (implies standard fields `created`, `last_updated`, `custom_field_data`, tags support, change logging, etc.).

---
## 6. Validation & Integrity
- ISD-AS regex ensures two accepted forms.
- Zendesk ticket numeric enforced via RegexValidator & form `clean_zendesk_ticket`.
- `SCIONLinkAssignment.peer` uniqueness enforced but format not validated beyond help text (gap).
- Appliances stored as JSON list; no enforced uniqueness within the list – duplicates possible if not prevented externally (forms attempt to avoid duplicates on add).
- Cascade delete of Organization now cascades to ISDAS and then link assignments.

---
## 7. Forms (`forms.py`)
Patterns:
- Use `NetBoxModelForm` for CRUD.
- `ISDAForm` hides `appliances` (managed separately) – stores incoming comma-separated values -> list.
- `SCIONLinkAssignmentForm` dynamically populates `core` (Appliance) choices based on selected ISD-AS (initial or POST data) by overriding `__init__` and `full_clean`.
- Appliance management separate non-model form: `ApplianceManagementForm` provides add/edit actions.
- Filter forms subclass `NetBoxModelFilterSetForm` and expose search (`q`) + tag filters + model-specific filters.

Key Caveat:
- `customer_id` and `zendesk_ticket` optionality enforced only at form level; model still declares both as non-blank (except zendesk which is blank=True). If API creates assignment without `customer_id`, will it fail? Currently model field `customer_id` has no `blank=True`; API serializer includes it; omission will raise validation error at model level. Align if optionality intended.

---
## 8. Filtering (`filtersets.py`)
- Each model gets a `NetBoxModelFilterSet` adding a `q` CharFilter with `method='search'`.
- Search uses `icontains` across key textual fields combined via OR.
- Potential performance issue for large datasets (no full-text index use) – consider trigram or search vector indexing if scaling.

---
## 9. Tables (`tables.py`)
- Subclass `NetBoxTable` for NetBox integration (bulk actions, checkboxes).
- Custom renderers:
  - `OrganizationTable.render_isd_ases_count` counts related objects (N+1 risk if not prefetched – views use `prefetch_related`, mitigating).
  - `ISDATable.render_appliances` returns count of appliances, not list (UI intentionally numeric summary).
  - `ISDATable.render_organization` null-safe link formatting.
  - `SCIONLinkAssignmentTable.render_zendesk_ticket` converts ticket to external link.

---
## 10. Views (`views.py`)
Use NetBox generic class-based views for consistency:
- `ObjectListView` + `ObjectView` + `ObjectEditView` + `ObjectDeleteView` + `BulkDeleteView` + `ObjectChangeLogView`.
- Changelog CBVs define `base_template` matching their detail pages; the URLconf must supply the target model (see §12).
- Querysets optimized with `select_related` / `prefetch_related`.
- Custom appliance mgmt functions (add/edit/remove) manipulate list stored in JSON and propagate edits:
  - Renaming appliance updates all related `SCIONLinkAssignment.core` values (bulk update query).
  - Removing appliance deletes associated link assignments (explicit cascade at application level; ensures referential integrity to the appliance concept which is otherwise uncontrolled text field).
- AJAX endpoint: `get_isdas_appliances` returns JSON list of appliances for UI dynamic dropdown.

---
## 11. Navigation (`navigation.py`)
- Conditional top-level menu creation based on `PLUGINS_CONFIG['netbox_scion']['top_level_menu']`.
- Three primary menu items: Organizations, ISD-ASes, SCION Link Assignments each with Add button.

---
## 12. URL Structure
UI (`urls.py`):
- Base: `/plugins/scion/`
- Organizations: `/organizations/` CRUD & changelog
- ISD-ASes: `/isd-ases/` + appliance mgmt nested operations
- Link Assignments: `/link-assignments/`
- Changelog entries use NetBox's `ObjectChangeLogView`; include `kwargs={'model': Model}` in the URL pattern to avoid runtime errors.
- AJAX: `/ajax/isdas-appliances/`
API (`api/urls.py`):
- Router registers `organizations`, `isd-ases`, `link-assignments`
- Extra path `isdas-cores/` (legacy – see technical debt) for core lookup

---
## 13. API Layer
Serializers:
- Extend `NetBoxModelSerializer` (adds `created`, `last_updated`, `custom_field_data` automatically)
- Computed read-only counts via queryset annotations (`isd_ases_count`, `link_assignments_count`)
- Provide `zendesk_url` via model method mapping.
ViewSets:
- Subclass `NetBoxModelViewSet` (inherits permissions, bulk operations, export) – rely on NetBox permission system.
- Use `select_related` / `prefetch_related` + `annotate(Count(...))` for count fields.
Legacy Inconsistency:
- `ISDACoreLookupView` still references `isdas.cores` (field removed / renamed) – currently broken unless compatibility layer elsewhere (none in repo). Should be updated to `appliances` or removed.

---
## 14. Migrations Timeline Highlights
1. `0001_initial` – Base schema used `cores` and `customer_name`, FK PROTECT, mandatory Zendesk ticket.
2. `0002_add_custom_field_data` – Defensive addition of `custom_field_data` columns (raw SQL) ensuring idempotence.
3. `0003_fix_cores_field` – Converted `cores` to JSONField.
4. `0004_add_core_field` – Added `core` field to SCIONLinkAssignment (appliance reference string).
5. `0005_add_relationship_field` – Added `relationship` with staged nullability + data migration defaulting to CHILD.
6. `0006_make_zendesk_ticket_optional` – Made zendesk ticket `blank=True`.
7. `0007_add_appliance_type` – Introduced `appliance_type` enum.
8. `0008_remove_gate_appliance_type` – Removed GATE option (contracting enum).
9. `0009_version_1_2_changes` – Major rename: `cores` -> `appliances`; removed `appliance_type`; renamed `customer_name` -> `peer_name`; added `peer` + unique constraint; FK to Organization changed to CASCADE.
10. `0010_fix_database_schema` – Cleaned stray columns + enforced unique constraint for peer idempotently.

Renames rely on Django migration operations; ensure subsequent code references updated (one missed in API view). When adding new renames, prefer `RenameField` to preserve data.

---
## 15. Tests (`tests.py`) – Current State & Issues
Covers:
- Organization basic uniqueness & __str__
- ISDAS validation and appliances display
- SCIONLinkAssignment uniqueness & zendesk ticket validation and zendesk URL
Issues / Bugs:
- In `SCIONLinkAssignmentTestCase.setUp`, assignment creation uses `isd_as=isd_as` (undefined variable) instead of `self.isdas`; test would error if executed.
- Creation of `SCIONLinkAssignment` lacks required fields (`relationship`, `core`, etc. in earlier versions) – currently sets `relationship` but `core="v1"` is present; `peer` missing (now required & unique) → test likely failing post v1.3 without default value.
- No API tests (serialization, filtering) or view permission tests.
Suggested improvements:
- Fix variable reference
- Add test coverage for `peer` uniqueness, cascade deletes, appliance rename side effects.

---
## 16. Known Technical Debt / Inconsistencies
| Area | Issue | Impact | Suggested Fix |
|------|-------|--------|---------------|
| Versioning | `__init__.__version__ = 1.3.0` vs `setup.py version='1.3'` | Confusion for packaging / PyPI | Align to semantic version (1.3.0) in `setup.py` & tag |
| NetBox Version Docs | README says NetBox v4.0+; `requirements.txt` comment says 3.5+ | Install ambiguity | Confirm minimum tested version & update both |
| API Legacy View | `ISDACoreLookupView` uses `isdas.cores` | Runtime KeyError / attribute error | Rename to `appliances` or remove endpoint |
| Field Naming | Model field storing appliance is `core` but UI/labels say Appliance | Cognitive overhead | Consider migration renaming `core` → `appliance` (careful with existing constraints) |
| `customer_id` Optionality | Forms treat as optional but model requires non-blank | API inconsistencies | Add `blank=True` or enforce requirement in form |
| `peer` Format | Help text describes format but no regex validation | Data quality risk | Add RegexValidator & migration |
| Tests | Broken variable, outdated assumptions | CI failures if enabled | Fix & expand tests |
| Duplicate Appliances | No enforcement of uniqueness inside JSON list | UI duplication risk | Normalize list (set) before save |
| Security / Permissions | No custom permission granularity beyond model-level | Over-broad access in some deployments | Add object-level or action-specific permission hooks if needed |

---
## 17. Performance Considerations
Current dataset likely small; existing use of `select_related` / `prefetch_related` and `annotate` is adequate. Potential future optimizations:
- Add DB index on `SCIONLinkAssignment(interface_id, isd_as)` (implicit via unique constraint) and `(isd_as, peer)` (also via unique constraint) – already handled.
- Add index on `ISDAS.isd_as` (unique -> already indexed) and `Organization.short_name` (unique -> already indexed).
- If `q` searches become slow, implement a materialized search column or Postgres full-text index.

---
## 18. Extension Patterns (How To Safely Add Features)
### Add a New Field to Existing Model
1. Add field in `models.py` with `blank=True` / reasonable default to avoid migrations failing.
2. Create migration via `makemigrations`.
3. Update serializers (read/write), forms (include in `Meta.fields`), tables, filtersets (optional).
4. Add tests verifying create + edit + API representation.
5. Document in CHANGELOG under Added / Changed.

### Add a New Model
1. Subclass `NetBoxModel` for automatic metadata + change logging.
2. Implement `__str__`, `get_absolute_url`, optional `display` property.
3. Create serializer, filterset, table, forms, views, URLs, navigation entry.
4. Add counts to related parent model via `annotate` if needed.

### Add Validation
- Prefer model-level validator functions or `clean()` if cross-field.
- Reflect validation in API serializer tests + forms.

### Add API-Only Computed Field
- Implement model method or property.
- Add serializer `SerializerMethodField` or mapped source (`source='method_name'`).

### Add UI Action (Bulk or Custom)
- Use function-based or subclass appropriate NetBox generic view.
- Add route in `urls.py` under logical grouping.
- Protect with permissions via mixins if adding sensitive operations.

---
## 19. Coding Conventions Observed
- Consistent use of `select_related` / `prefetch_related` in list/detail views.
- RegexValidator used for structured identifiers.
- UniqueConstraints defined inside `Meta.constraints` for multi-field uniqueness.
- Naming: `ISDAS` (capitalized acronym) model, property `isd_as` attribute.
- Help texts carefully describe required formats.

---
## 20. Deployment & Packaging Notes
- PyPI distribution (`netbox-scion`), `pip install netbox-scion==1.3.0` per README.
- Docker integration leverages custom `Dockerfile-Plugins` installing plugin requirements with `uv pip`.
- Wheel build via `python setup.py bdist_wheel` (could modernize to `pyproject.toml`).
- No explicit runtime dependencies declared (empty `install_requires=[]`) – relies fully on NetBox environment.

Recommendations:
- Add explicit `Requires-Dist` constraints (e.g., `netbox>=X,<Y` for clarity).
- Migrate packaging to PEP 621 / `pyproject.toml` for future updates.

---
## 21. Security & Permissions
- No custom permission classes; inherits NetBox default permission model (object-level scoping not implemented).
- No direct user-submitted raw SQL; migrations use raw SQL but controlled and idempotent.
- User-provided JSON list (`appliances`) has no sanitation beyond whitespace trimming; ensure no code injection paths (used only as plain strings).
- Zendesk ticket rendered as anchor tag – value validated numeric; safe from simple XSS injection.

---
## 22. Logging & Auditing
NetBoxModel integration implies:
- Change logging (viewable through changelog views) for create/update/delete.
- Tagging support (forms include TagFilterField) though tagging UI not explicitly surfaced in forms (could be added).

---
## 23. Potential Future Enhancements
| Priority | Enhancement | Rationale |
|----------|-------------|-----------|
| High | Fix broken `ISDACoreLookupView` or remove | Eliminate runtime error / confusion |
| High | Add regex validation for `peer` | Data hygiene & predictable downstream parsing |
| High | Align version strings & NetBox minimum version | Reduce install support issues |
| Medium | Rename `core` → `appliance` with migration | Consistency (UI vs storage) |
| Medium | Fix / expand tests & add API tests | Confidence for refactors |
| Medium | Enforce unique appliances list & provide management UI improvements | Data normalization |
| Low | Add pyproject-based build & CI workflow | Modern packaging |
| Low | Add caching for frequent heavy queries (if scaling) | Performance |

---
## 24. Quick Reference – Critical Objects & Methods
- Models: `Organization`, `ISDAS`, `SCIONLinkAssignment`
- Serializer Count Fields: `isd_ases_count`, `link_assignments_count`
- Constraints: `unique_interface_per_isdas`, `unique_peer_per_isdas`
- Dynamic Form Behavior: `SCIONLinkAssignmentForm.__init__` + `full_clean` updates `core` choices
- Appliance CRUD Logic: `add_appliance_to_isdas`, `edit_appliance_in_isdas`, `remove_appliance_from_isdas`
- Zendesk URL: `SCIONLinkAssignment.get_zendesk_url`

---
## 25. When Modifying – Safety Checklist
Before committing changes:
1. Do new/renamed fields appear in: model, migration, serializer, forms, tables, filterset (if searchable), templates?
2. Are constraints / uniqueness rules updated accordingly?
3. Are `select_related` / `prefetch_related` still valid (field rename could break)?
4. Do API endpoints reflect new fields (GET & POST JSON)?
5. Does navigation still link to correct URL names? (Reverse names used in templates?)
6. Are tests updated (especially on rename)?
7. CHANGELOG entry added with version bump following SemVer.
8. Version constants consistent (`__init__`, packaging metadata, README examples).

---
## 26. Example: Adding Validation for `peer`
1. In `SCIONLinkAssignment`: add `RegexValidator(regex=r'^\d+-([0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+|\d+)#\d+$', message='Peer must be ISD-AS#Interface (e.g., 1-ff00:0:110#1)')` to `peer` field.
2. Create migration.
3. Update tests to include both valid & invalid cases.
4. Update API docs (`API.md`).

---
## 27. Known Missing Artifacts
- No static assets directory currently in repo (README mentions it) – safe to ignore unless adding JS helpers for dynamic appliance selection.
- Templates rely on NetBox generic templates; custom detail/edit templates located under `templates/netbox_scion/` but not deeply analyzed here; ensure naming matches view `template_name` fields.

---
## 28. Risk Areas During Refactors
- Field Renames: Must coordinate across serializers, filters, templates, tests, navigation, AJAX endpoints.
- JSONField Schema Changes: Existing data shape assumptions (list of strings). Changing to objects requires data migration + UI changes.
- Unique Constraints: Dropping/altering requires careful migration order (remove constraint, transform data, re-add).
- Optionality Shifts: Making a required field optional demands serializer & form alignment to avoid inconsistent validation paths.

---
## 29. High-Signal Summary (For Fast AI Context Priming)
NetBox plugin named `netbox_scion` providing CRUD & API for Organizations, ISD-ASes (with JSON list `appliances`), and SCION link interface assignments (with uniqueness on (isd_as, interface_id) and (isd_as, peer)). Uses NetBox generic CBVs, DRF serializers, django-filter, django-tables2. Legacy naming (`core` field) and outdated endpoint (`ISDACoreLookupView`) reflect pre-renaming state where `cores` became `appliances`. Validation robust for ISD-AS & Zendesk tickets, weaker for `peer` and appliance list uniqueness. Tests minimal and currently broken due to variable reference and new required `peer` field absence. Primary future work: align naming, add validation, fix outdated view, improve test coverage, synchronize version declarations, and optionally modernize packaging.

---
## 30. Change Log Integration Requirement
When adding functionality: update `CHANGELOG.md` section for new unreleased version (e.g., `[1.3.1] - YYYY-MM-DD`). Maintain Added / Changed / Fixed / Removed headings following Keep a Changelog format.

---
## 31. Recent Changes (v1.3.1)
### Added
- **Filterable section headers**: Made section headers clickable links in detail pages:
  - ISD-AS detail page: "SCION Link Assignments" header links to filtered list (`?isd_as={id}`)
  - Organization detail page: "ISD-ASes" header links to filtered list (`?organization={id}`)
  - Improves navigation and allows users to quickly view all related items

### Changed
- **SCION Link Assignment detail page**: Changed "Full ISD-AS Path" label to "ISD-AS" in Related Information section and made the value clickable, linking to the ISD-AS detail page for better navigation consistency.

### Fixed
- **Appliance field auto-selection on edit**: Fixed `SCIONLinkAssignmentForm.__init__` to properly set `self.initial['core']` and added `data-initial-value` attribute to the widget. Updated the JavaScript in `scionlinkassignment_edit.html` to use polling-based ready-check mechanisms throughout:
  - `waitForTomSelect()` polls for Tom Select initialization instead of 100ms/200ms fixed delays
  - Appliance value restoration polls for option availability before setting value
  - Maximum retry attempts (20 for initialization, 10 for value restoration) with 10ms intervals prevent infinite loops
  - Graceful fallback with console warnings if ready state not achieved
  - This prevents race conditions on slower systems and works reliably across different speeds
- **Peer field unique constraint**: Changed the `peer` field to allow `NULL` values and updated the unique constraint to only validate non-empty peer values (migration 0018). This allows multiple SCION Link Assignments with empty peer fields for the same ISD-AS, while still enforcing uniqueness for actual peer values. Modified both `SCIONLinkAssignment.clean()` and `SCIONLinkAssignmentForm.clean_peer()` to convert empty strings to `None` for proper constraint handling.

---
## 32. Contact Points / External Integrations
- Zendesk: Only stored as numeric ID → URL pattern `https://anapaya.zendesk.com/agent/tickets/{id}` hardcoded in `get_zendesk_url()`; if multi-tenant support required, externalize base URL to plugin settings.

---
## 32. Suggested Immediate Fixes (Actionable)
1. Update `api/views.py`: replace `cores` with `appliances`.
2. Fix tests variable name + include `peer` field in assignment creation.
3. Align version numbers everywhere to `1.3.0` (or bump to `1.3.1`).
4. Decide on `customer_id` optionality → add `blank=True` if intended.
5. Add regex validator for `peer` if format is required operationally.
6. (Done in 0011) Added `comments` TextField to Organization, ISDAS, SCIONLinkAssignment.

---
End of technical prompt.
