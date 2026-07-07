# Changelog

## [0.260706] - 2026-07-06

### Added
- `py.typed` marker for downstream type-checking support

### Changed
- Middleware classes (vary, csrf, schjwt, schpost) converted to modern Django 6.0 format without `MiddlewareMixin`
- `AppManager`, `AppInfo`, `AppItemInfo` extracted from `context_processors.py` to `app_manager.py`
- Cache configuration fallback logs a warning instead of silently failing

### Fixed
- `os.system()` replaced with `subprocess.run()` in odf_view plugin templates
- `AbstractBaseUser` import in `pytigon_lib.schviews.schrules.py` fixed with `from __future__ import annotations`
- CORS on Android now requires explicit `CORS_ORIGIN_ALLOW_ALL` env var opt-in
- Added missing `_()` import in `translate.py`
- Django version guard assertion added in `initdjango.py`

## [0.260705] - 2025-10-27

- Separating standard projects from pytigon into separate project
- Removed bundled pkg_resources, replaced fs with fsspec

## [0.260628] - 2025-07-07

### Changed
- Modernized Python code style and improved exception handling
- Simplified shell script commands

### Added
- CSP support
- SafeSubprocess for secure subprocess execution
- New web components

## [0.260620] - 2025-06-24

### Added
- Xterm fit addon
- Project files migrated to .ptigprj format

### Changed
- Cleaned up unused dependencies
