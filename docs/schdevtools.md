# schdevtools — Pytigon Developer Tools Guide

**schdevtools** is Pytigon's built-in IDE and application builder. It lets you
visually define Django models, views, URLs, menus, templates, static assets,
forms, tasks, WebSocket consumers, translations, and more — then generates a
working Pytigon application from a single `.prj` project file.

Everything is driven by a JSON-based project description format. This guide
decodes that format so you can understand, edit, and create project files by
hand or extend the builder itself.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project File Structure](#project-file-structure)
- [Core Models Reference](#core-models-reference)
  - [SChProject — The Root](#schproject--the-root)
  - [SChApp — Application Module](#schapp--application-module)
  - [SChTable — Database Table / Model](#schtable--database-table--model)
  - [SChField — Model Field](#schfield--model-field)
  - [SChView — View / URL Endpoint](#schview--view--url-endpoint)
  - [SChAppMenu — Navigation Menu](#schappmenu--navigation-menu)
  - [SChForm — Form Definition](#schform--form-definition)
  - [SChFormField — Form Field](#schformfield--form-field)
  - [SChTemplate — Template](#schtemplate--template)
  - [SChStatic — Static Asset](#schstatic--static-asset)
  - [SChFile — Custom File](#schfile--custom-file)
  - [SChTask — Background Task](#schtask--background-task)
  - [SChChannelConsumer — WebSocket Consumer](#schchannelconsumer--websocket-consumer)
  - [SChLocale, SChTranslate — i18n / l10n](#schlocale-schtranslate--i18n--l10n)
  - [SChChoice / SChChoiceItem — Choice Lists](#schchoice--schchoiceitem--choice-lists)
- [Field Types Reference](#field-types-reference)
- [Gui Types](#gui-types)
- [View Return Types](#view-return-types)
- [File Types](#file-types)
- [Static Asset Types](#static-asset-types)
- [Form Field Types](#form-field-types)
- [Template Tags & Custom Components](#template-tags--custom-components)
- [Advanced: Embedded Python/JS Code](#advanced-embedded-pythonjs-code)
- [Building & Installing](#building--installing)

---

## Quick Start

```bash
# Run schdevtools (Pytigon IDE)
ptig schdevtools
```

This launches a desktop or web-based IDE. Inside it you can:

1. **Open** an existing `.prj` project file
2. **Edit** models, views, menus, forms, templates visually
3. **Generate** a Django application from the project
4. **Build** an installable package with `install.ini`

The project file format is a tree of JSON nodes. Each node has:

| Key | Purpose |
|-----|---------|
| `model` | The model type name (e.g. `"SChProject"`, `"SChTable"`) |
| `attributes` | Key-value properties of this node |
| `children` | Array of child nodes |

---

## Project File Structure

```
SChProject                          ← Root: one project = one Django "app"
├── SChApp (schbuilder)             ← The builder application itself
│   ├── SChChoice                   ← Reusable choice lists
│   │   └── SChChoiceItem
│   ├── SChTable (SChProject)       ← Table definition for projects
│   │   └── SChField × N           ← Fields of the table
│   ├── SChTable (SChApp)
│   │   └── SChField × N
│   ├── SChTable (SChAppMenu)
│   │   └── SChField × N
│   ├── SChTable (SChTable)
│   │   └── SChField × N
│   ├── SChTable (SChField)
│   │   └── SChField × N
│   ├── SChTable (SChView)
│   │   └── SChField × N
│   ├── SChTable (SChForm)
│   │   └── SChField × N
│   ├── SChTable (SChFormField)
│   │   └── SChField × N
│   ├── SChTable (SChTemplate)
│   │   └── SChField × N
│   ├── SChTable (SChStatic)
│   │   └── SChField × N
│   ├── SChTable (SChFile)
│   │   └── SChField × N
│   ├── SChTable (SChTask)
│   │   └── SChField × N
│   ├── SChTable (SChChannelConsumer)
│   │   └── SChField × N
│   ├── SChTable (SChLocale)
│   │   └── SChField × N
│   ├── SChTable (SChTranslate)
│   │   └── SChField × N
│   ├── SChView × N                ← URL/view definitions
│   ├── SChAppMenu × N             ← Menu items
│   └── SChTemplate × N            ← Templates
└── (more SChApp nodes for additional modules)
```

The `schbuilder` app is special — it defines the meta-schema for Pytigon
projects, i.e. the tables, fields, and views that the builder itself uses.

---

## Core Models Reference

### SChProject — The Root

A single project is one Django application. The root node represents the
entire project.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | CharField(64) | Machine name (letters, digits, underscores) |
| `title` | CharField(255) | Human-readable title |
| `version` | CharField(16) | Version string, default `"latest"` |
| `main_view` | BooleanField | Show the project in the main view / app launcher |
| `ext_apps` | CharField(4096) | Newline-separated list of external app dependencies (e.g. `_schwiki.schwiki`) |
| `plugins` | CharField(4096) | Semicolon-separated plugin paths (e.g. `standard/shell;standard/hexview`) |
| `gui_type` | CharField(32) | GUI mode: `standard`, `modern`, `tree`, `tray`, `dialog`, `one_form` |
| `gui_elements` | CharField(1024) | Toolbar config: `toolbar(file(open,exit),clipboard)` etc. |
| `login_required` | BooleanField | Require authentication |
| `public` | BooleanField | Mark as publicly accessible |
| `main` | BooleanField | Mark as the main/default project |
| `start_page` | CharField(255) | Default start page URL |
| `doc` | TextField | Documentation / notes |
| `desktop_gui_type` | CharField(32) | HTML GUI for desktop browsers (choices: `HtmlGui_CHOICES`) |
| `smartfon_gui_type` | CharField(32) | HTML GUI for smartphones |
| `tablet_gui_type` | CharField(32) | HTML GUI for tablets |
| `additional_settings` | TextField | Raw Python code appended to Django settings |
| `custom_tags` | TextField | Newline-separated paths to custom JS component files |
| `readme_file` | TextField | README.md content |
| `license_file` | TextField | LICENSE file content |
| `install_file` | TextField | install.ini content (build/packaging config) |
| `encoded_zip` | TextField | Base64-encoded ZIP of the project's source files |
| `icon` | CharField(256) | Icon path |
| `icon_size` | CharField(1) | `0`=small, `1`=medium, `2`=large |
| `git_repository` | CharField(255) | Git remote URL |
| `autor_name` | CharField(255) | Author name |
| `autor_email` | CharField(256) | Author email |
| `autor_www` | CharField(256) | Author website |
| `components_initial_state` | CharField(1024) | JSON initial state for frontend components |
| `template_desktop` | TextField | Django template for desktop layout |
| `template_smartfon` | TextField | Django template for smartphone layout |
| `template_tablet` | TextField | Django template for tablet layout |
| `template_schweb` | TextField | Django template for native wxWidgets client |
| `template_theme` | TextField | Base theme template |
| `user_app_template` | TextField | Patches / overrides |
| `app_main` | TextField | Main application entry point |
| `icon_code` | TextField | Inline SVG icon code |

**Children:** Array of `SChApp` nodes.

---

### SChApp — Application Module

A sub-module within the project. Each SChApp generates a Django app module
with its own models, views, URLs, and templates.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigForeignKey→SChProject | Owning project |
| `name` | CharField(64) | Module name (Python identifier) |
| `title` | CharField(255) | Human-readable title |
| `module_name` | CharField(64) | Grouping label for the sidebar |
| `module_title` | CharField(255) | Grouping label title |
| `perms` | BooleanField | Enable per-object permissions |
| `index` | CharField(255) | Path to an index page |
| `model_code` | TextField | Python code for `models.py` (custom model logic) |
| `view_code` | TextField | Python code for `views.py` (custom view logic) |
| `urls_code` | TextField | Python code for `urls.py` (URL routing) |
| `tasks_code` | TextField | Python code for `tasks.py` (background tasks) |
| `consumer_code` | TextField | Python code for `consumers.py` (WebSocket) |
| `doc` | TextField | Documentation |
| `user_param` | TextField | User-defined parameter string (e.g. `icon:fa_building`) |
| `icon` | CharField(256) | Icon path |
| `icon_size` | CharField(1) | Icon size |
| `icon_code` | TextField | Inline SVG icon |

**Children:** `SChChoice`, `SChTable`, `SChView`, `SChAppMenu`, `SChTemplate`,
`SChStatic`, `SChFile`, `SChTask`, `SChChannelConsumer`, `SChLocale`,
`SChForm` nodes.

---

### SChTable — Database Table / Model

Defines a Django model (database table). Each SChTable generates a Django
model class.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `base_table` | CharField(255) | Base table: `""` = `models.Model`, `"JSONModel"`, or `"app.ModelName"` |
| `name` | CharField(255) | Model class name |
| `verbose_name` | CharField(255) | Singular display name |
| `verbose_name_plural` | CharField(255) | Plural display name |
| `metaclass_code` | TextField | Code injected into the model's `Meta` inner class |
| `table_code` | TextField | Python code for custom model methods & properties |
| `ordering` | CharField(255) | Default ordering, e.g. `"['name']"` or `"['-created']"` |
| `doc` | TextField | Documentation |
| `generic` | BooleanField | Use generic foreign keys |
| `url_params` | CharField(255) | URL parameters for detail views |
| `proxy_model` | CharField(255) | Name of the proxied model (for proxy models) |

**Children:** Array of `SChField` nodes.

> **`table_code` is the key differentiator.** This is where you define
> model-level methods, properties, Meta options, custom managers, and
> anything else that goes inside the model class body beyond field
> declarations.

---

### SChField — Model Field

Defines a single field (column) on a model table.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChTable | Owning table |
| `name` | CharField(255) | Field name (Python identifier) |
| `description` | CharField(255) | `verbose_name` for the field |
| `type` | CharField(64) | Django field class (see [Field Types](#field-types-reference)) |
| `null` | BooleanField | Allow NULL in database |
| `blank` | BooleanField | Allow blank in forms |
| `editable` | BooleanField | Show in forms |
| `unique` | BooleanField | Unique constraint |
| `db_index` | BooleanField | Create database index |
| `default` | CharField(255) | Default value (Python expression) |
| `help_text` | CharField(255) | Help text for forms |
| `choices` | CharField(255) | Reference to a `SChChoice` by name (e.g. `"Gui_CHOICES"`) |
| `rel_to` | CharField(255) | Target model for relational fields (e.g. `"SChProject"` or `"auth.User"`) |
| `param` | CharField(255) | Extra field parameters (e.g. `"max_length=64"`, `"upload_to='uploads/'"`) |
| `url_params` | CharField(255) | Additional URL parameters for related lookups |

---

### SChView — View / URL Endpoint

Defines a Django view and its URL routing. This is how you expose data to
the frontend.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | View name (used as URL name) |
| `title` | CharField(255) | Display title |
| `type` | CharField(1) | **Required.** View action type (see below) |
| `table` | CharField(255) | Target model (e.g. `"SChProject"` or `"app.Model"`) |
| `view_type` | CharField(1) | Return type (see [View Return Types](#view-return-types)) |
| `template` | CharField(255) | Template path (if view_type=`T`) |
| `base_filter` | TextField | JSON filter applied to the queryset |
| `default_sort` | CharField(255) | Default sort field |
| `search_fields` | CharField(255) | Comma-separated fields searchable in the UI |
| `link` | CharField(255) | Custom URL path |
| `where` | CharField(255) | Server-side WHERE clause |
| `action` | CharField(255) | Custom action name |
| `gen_function` | CharField(255) | Generator function name |
| `rows_on_page` | IntegerField | Pagination: rows per page |
| `valid_form` | TextField | Django form class to validate submissions |
| `code` | TextField | Custom Python view code |
| `doc` | TextField | Documentation |
| `url_params` | CharField(255) | Extra URL parameters |
| `embedded` | BooleanField | Embed as sub-view in another page |

**View type (`type`):**

| Code | Meaning |
|------|---------|
| `t` | Table action — list/create/update/delete on a table |
| `r` | Row action — action on a single row |
| `u` | View — custom view/page |

**View return type (`view_type`):**

| Code | Meaning |
|------|---------|
| `T` | Django Template |
| `O` | ODF spreadsheet (default .ods) |
| `P` | PDF document |
| `J` | JSON response |
| `X` | XML response |
| `U` | User-defined |
| `S` | OOXML spreadsheet (.xlsx) |
| `t` | Plain text |
| `H` | HTML→DOCX template (.hdoc) |

---

### SChAppMenu — Navigation Menu

Defines a menu item in the application's navigation.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Display label |
| `link` | CharField(255) | URL or view name |
| `link_type` | CharField(1) | `-`=default, `desktop`, `panel`, `header`, `footer`, `script`, `pscript`, `browser`, `browser_panel`, `browser_header`, `browser_footer` |
| `view` | CharField(1) | `t`=table action, `r`=row action, `u`=view |
| `align` | CharField(255) | Alignment hint |
| `position` | CharField(255) | Position in menu |
| `icon` | CharField(256) | Icon path |
| `submenu` | CharField(255) | JSON submenu definition |
| `user_param` | TextField | User parameter string |
| `html_before` | TextField | Raw HTML inserted before the menu item |
| `html_after` | TextField | Raw HTML inserted after the menu item |
| `fragment` | CharField(255) | URL fragment for the menu item |

---

### SChForm — Form Definition

Defines a Django form class.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Form class name |
| `title` | CharField(255) | Display title |
| `table` | CharField(255) | Target model (for ModelForm) |
| `base_class` | CharField(255) | Base form class (e.g. `"ModelForm"`) |
| `layout` | TextField | Form layout definition |
| `code` | TextField | Custom form code |
| `valid` | TextField | Validation code |
| `doc` | TextField | Documentation |

**Children:** `SChFormField` nodes.

---

### SChFormField — Form Field

Defines a single field within a form.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChForm | Owning form |
| `name` | CharField(255) | Field name |
| `type` | CharField(64) | Django form field class (e.g. `CharField`, `IntegerField`, `ChoiceField`, `ModelChoiceField`) |
| `label` | CharField(255) | Label text |
| `widget` | CharField(128) | Widget class (e.g. `TextInput`, `Select`, `CheckboxInput`) |
| `param` | CharField(255) | Extra field parameters |
| `initial` | CharField(255) | Initial value |
| `required` | BooleanField | Required flag |
| `position` | IntegerField | Display order |
| `help_text` | CharField(255) | Help text |

---

### SChTemplate — Template

Defines a Django template file.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | File name (e.g. `"list.html"`) |
| `type` | CharField(1) | Template type (see below) |
| `path` | CharField(255) | Directory path relative to templates |
| `code` | TextField | Template source code |
| `doc` | TextField | Documentation |

**Template type:**

| Code | Meaning |
|------|---------|
| `f` | Template filter library |
| `t` | Template tag library |
| `c` | Custom file |
| `m` | Management command |
| `p` | Plugin code |
| `i` | Plugin template |
| `l` | Library code |
| `s` | GraphQL schema |
| `r` | REST API definition |
| `j` | Frontend view (JS) |
| `T` | Frontend template (JS) |
| `n` | Nim extension |
| `N` | Nim executable source |
| `E` | Nimpy extension |
| `C` | CSS (included in desktop.html) |
| `J` | JavaScript (included in desktop.html) |
| `P` | Python→JS via Transcrypt (included in desktop.html) |
| `R` | Web component (included in desktop.html) |
| `I` | SASS→CSS (included in desktop.html) |
| `U` | Custom file with translation support (.pyj, .webc, .sass) |
| `O` | Other application file |
| `B` | Other application file (base64 encoded) |

---

### SChStatic — Static Asset

Defines a static file bundled with the application.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | File name |
| `type` | CharField(1) | Asset type (same codes as [Template types](#schtemplate--template) but static context) |
| `path` | CharField(255) | Directory path under `static/` |
| `code` | TextField | File content |
| `doc` | TextField | Documentation |

---

### SChFile — Custom File

An arbitrary file to include in the generated application (e.g. a README,
a license, a config file).

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | File path/name |
| `code` | TextField | File content |

---

### SChTask — Background Task

Defines a background task (Django-Q or similar).

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Task name |
| `function` | CharField(255) | Python function path to call |
| `schedule` | CharField(255) | Cron or interval schedule |
| `code` | TextField | Custom task code |

---

### SChChannelConsumer — WebSocket Consumer

Defines a Django Channels consumer for WebSocket communication.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Consumer name |
| `type` | CharField(64) | Consumer class: `WebsocketConsumer`, `AsyncWebsocketConsumer`, `JsonWebsocketConsumer`, `AsyncJsonWebsocketConsumer`, `AsyncHttpConsumer`, `AsyncConsumer`, `SyncConsumer` |
| `code` | TextField | Custom consumer code |

---

### SChLocale, SChTranslate — i18n / l10n

**SChLocale** represents a locale (language) for the application.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `code` | CharField(8) | 2-letter language code (e.g. `"pl"`, `"en"`) |
| `name` | CharField(255) | Language name |

**Children:** `SChTranslate` nodes.

**SChTranslate** represents a single translation string.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChLocale | Owning locale |
| `msgid` | CharField(255) | Source string |
| `msgstr` | CharField(255) | Translated string |
| `context` | CharField(255) | Translation context (msgctxt) |

---

### SChChoice / SChChoiceItem — Choice Lists

Reusable enumerated choice lists for model fields.

**SChChoice:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Choice set name (referenced by `SChField.choices`) |
| `verbose_name` | CharField(255) | Display name |

**SChChoiceItem:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChChoice | Owning choice set |
| `name` | CharField(255) | Key (stored in DB) |
| `value` | CharField(255) | Verbose display label |

---

## Field Types Reference

Pytigon extends Django's field types with custom ones prefixed `Ptig`:

### Standard Django Fields

`AutoField`, `BooleanField`, `CharField`, `CommaSeparatedIntegerField`,
`DateField`, `DateTimeField`, `DecimalField`, `EmailField`, `FileField`,
`FilePathField`, `FloatField`, `ImageField`, `IntegerField`,
`GenericIPAddressField`, `NullBooleanField`, `PositiveIntegerField`,
`PositiveSmallIntegerField`, `SlugField`, `SmallIntegerField`, `TextField`,
`TimeField`, `URLField`, `XMLField`, `ForeignKey`, `OneToOneField`,
`ManyToManyField`

### Pytigon Extended Fields

| Field | Description |
|-------|-------------|
| `PtigForeignKey` | ForeignKey with Pytigon UI integration |
| `PtigManyToManyField` | ManyToManyField with Pytigon UI |
| `PtigHiddenForeignKey` | ForeignKey hidden from forms/UI (internal parent links) |
| `PtigForeignKeyWithIcon` | ForeignKey with icon support in the UI |
| `PtigManyToManyFieldWithIcon` | M2M field with icon support |
| `PtigTreeForeignKey` | ForeignKey for tree/hierarchy structures |
| `UserField` | Custom user reference field |
| `HiddenForeignKey` | Standard hidden FK |
| `GForeignKey` | GenericForeignKey |
| `GManyToManyField` | Generic M2M |
| `GHiddenForeignKey` | Hidden GenericForeignKey |

---

## Gui Types

### Desktop GUI (`gui_type`)

| Value | Behavior |
|-------|----------|
| `standard` | Table + detail panels |
| `modern` | Modern layout with cards & sidebar |
| `tree` | Tree-based navigation |
| `tray` | System tray app |
| `dialog` | Dialog-based UI |
| `one_form` | Single form, no navigation |

### HTML GUI per device

The `desktop_gui_type`, `smartfon_gui_type`, and `tablet_gui_type` fields
use these values:

| Value | Description |
|-------|-------------|
| `auto` | Auto-detect best fit |
| `desktop_standard` | Desktop: standard table layout |
| `desktop_modern` | Desktop: modern card layout |
| `tablet_standard` | Tablet: standard layout |
| `tablet_modern` | Tablet: modern layout |
| `smartfon_standard` | Smartphone: standard layout |
| `smartfon_modern` | Smartphone: modern layout |

### GUI Elements (`gui_elements`)

| Value | Toolbar |
|-------|---------|
| `toolbar(file(open,exit),clipboard)` | File menu + clipboard |
| `toolbar(file(open,save,save_as,exit),clipboard)` | File menu with save + clipboard |
| `toolbar(browse)` | Browse-only toolbar |

---

## View Return Types

| Code | Format | File Extension |
|------|--------|----------------|
| `T` | Django Template | .html |
| `O` | ODF Spreadsheet | .ods |
| `P` | PDF Document | .pdf |
| `J` | JSON | .json |
| `X` | XML | .xml |
| `U` | User-defined | (custom) |
| `S` | OOXML Spreadsheet | .xlsx |
| `t` | Plain Text | .txt |
| `H` | HTML→DOCX | .hdoc |

---

## File Types

When creating `SChTemplate`, `SChStatic`, or `SChFile` nodes, the `type`
field determines how the file is processed during the build:

| Code | Processing |
|------|------------|
| `C` | Plain CSS, linked in desktop.html |
| `J` | Plain JavaScript, linked in desktop.html |
| `P` | Python compiled to JavaScript (Transcrypt), linked in desktop.html |
| `R` | Web component, linked in desktop.html |
| `I` | SASS compiled to CSS, linked in desktop.html |
| `U` | Custom file with embedded translation support (.pyj, .webc, .sass) |
| `O` | Other file — copied as-is |
| `B` | Other file — base64 encoded in the JSON |
| `f` | Django template filter library |
| `t` | Django template tag library |
| `c` | Custom Python file |
| `m` | Django management command |
| `p` | Plugin Python code |
| `i` | Plugin template |
| `l` | Library code |
| `s` | GraphQL schema definition |
| `r` | REST API definition |
| `j` | Frontend view (client-side JS) |
| `T` | Frontend template |
| `n` | Pytigon extension in Nim |
| `N` | Nim executable source |
| `E` | Nimpy extension (Nim↔Python bridge) |

---

## Static Asset Types

Static assets use the same type codes as files, but only these are relevant
for static assets:

| Code | Meaning |
|------|---------|
| `C` | CSS (included in desktop.html) |
| `J` | JavaScript (included in desktop.html) |
| `P` | Python→JS via Transcrypt (included in desktop.html) |
| `R` | Component (included in desktop.html) |
| `I` | SASS→CSS (included in desktop.html) |
| `U` | Custom file (supports embedded translation) |
| `O` | Other project file (copied into static) |
| `B` | Other project file (base64 encoded) |

---

## Form Field Types

When defining `SChFormField` nodes, use standard Django form field class
names:

`BooleanField`, `CharField`, `IntegerField`, `FloatField`, `DecimalField`,
`DateField`, `DateTimeField`, `TimeField`, `EmailField`, `URLField`,
`ChoiceField`, `MultipleChoiceField`, `ModelChoiceField`,
`ModelMultipleChoiceField`, `FileField`, `ImageField`, `TextField`,
`RegexField`, `SlugField`, `UUIDField`, `JSONField`, `SplitDateTimeField`

Plus Pytigon extended form fields from `pytigon_lib.schdjangoext.formfields`.

---

## Template Tags & Custom Components

### Custom Tags (`custom_tags`)

List of JS component files loaded by the frontend, one per line:

```
_schcomponents/components/ptig-d3.js
_schcomponents/components/ptig-leaflet.js
_schcomponents/components/ptig-video.js
_schcomponents/components/ptig-spreadsheet.js
_schcomponents/components/ptig-pivottable.js
_schcomponents/components/ptig-plotly.js
_schcomponents/components/ptig-codeeditor.js
_schwiki/components/insert_object.js
```

### Plugins (`plugins`)

Semicolon-separated plugin paths:

```
standard/keymap;standard/tablefilter;standard/image_viewer;standard/hexview;standard/shell;standard/html_print
```

---

## Advanced: Embedded Python/JS Code

Several models support embedded Python code that gets injected into the
generated Django application:

| Field | Where it goes |
|-------|---------------|
| `model_code` | Inside `models.py` of the app (imports, helpers, field defaults) |
| `view_code` | Inside `views.py` of the app (view functions, logic) |
| `urls_code` | Inside `urls.py` of the app (URL patterns) |
| `tasks_code` | Inside `tasks.py` of the app (background task definitions) |
| `consumer_code` | Inside `consumers.py` of the app (ASGI consumers) |
| `table_code` | Inside the model class body (methods, properties) |
| `metaclass_code` | Inside the model's `Meta` class |
| `additional_settings` | Appended to Django `settings.py` |

These fields support the full Pytigon template syntax (indentation-based
Python-in-HTML, Transcrypt for JS, SASS for CSS).

---

## Building & Installing

### Project Build

The builder generates a complete Django application from the `.prj` file:

1. **Python sources:** `models.py`, `views.py`, `urls.py`, `tasks.py`,
   `consumers.py`, `forms.py`, `admin.py`
2. **Templates:** HTML templates from `SChTemplate` nodes
3. **Static files:** JS, CSS, images from `SChStatic` nodes
4. **Locale files:** `.po` translation files from `SChLocale`/`SChTranslate`
5. **Configuration:** `settings.py` overrides from `additional_settings`

### install.ini Format

The `install_file` attribute on `SChProject` contains packaging config:

```ini
GUI_COMMAND=--embededtaskqueue
PIP=pyautogui mss opencv-python
ANDROID_WEB=1
ANDROID_WEB_PORT=8000
ANDROID_WEB_HOST=0.0.0.0
ANDROID_WEB_HREF=127.0.0.1:8000
ANDROID_KIVY=1
SHORTCUT_DESKTOP=1
SHORTCUT_MENU=1
SHORTCUT_ANDROID=1
SHORTCUT_TITLE=DevTools
ICON=media/app.png
```

| Key | Purpose |
|-----|---------|
| `GUI_COMMAND` | Flags passed to the wxWidgets client |
| `PIP` | Extra pip packages to bundle |
| `ANDROID_WEB` | Enable Android WebView wrapper |
| `ANDROID_KIVY` | Enable Android Kivy wrapper |
| `SHORTCUT_*` | Create desktop/menu/Android shortcuts |
| `SHORTCUT_TITLE` | Shortcut display name |
| `ICON` | Path to application icon |

### Running the Builder

From the IDE, select **Build** to regenerate the application from the
project file. The build process:

1. Parses the `.prj` JSON tree
2. Creates Django app structure under the project directory
3. Compiles Python→JS (Transcrypt), SASS→CSS
4. Compiles Django templates (Pytigon's indentation-based template engine)
5. Generates `.po` translation files

---

## Summary

The `.prj` file is a complete declarative description of a Pytigon
application. It contains:

- **Schema** (tables + fields = Django models)
- **Business logic** (embedded Python code in `table_code`, `view_code`, etc.)
- **UI definition** (menus, templates, static assets, GUI types)
- **API surface** (views with their URLs, return types, filters)
- **Packaging** (install.ini, README, LICENSE, icons)
- **i18n** (locales and translations)

The `schbuilder` app itself is defined this way — the `.prj` file is both
the schema *and* the instance data for the builder tool.
