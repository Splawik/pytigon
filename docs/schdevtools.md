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
  - [SChProject — The Root](#schproject-the-root)
  - [SChApp — Application Module](#schapp-application-module)
  - [SChTable — Database Table / Model](#schtable-database-table-model)
  - [SChField — Model Field](#schfield-model-field)
  - [SChView — View / URL Endpoint](#schview-view-url-endpoint)
  - [SChAppMenu — Navigation Menu](#schappmenu-navigation-menu)
  - [SChForm — Form Definition](#schform-form-definition)
  - [SChFormField — Form Field](#schformfield-form-field)
  - [SChTemplate — Template](#schtemplate-template)
  - [SChStatic — Static Asset](#schstatic-static-asset)
  - [SChFile — Custom File](#schfile-custom-file)
  - [SChTask — Background Task](#schtask-background-task)
  - [SChChannelConsumer — WebSocket Consumer](#schchannelconsumer-websocket-consumer)
  - [SChLocale, SChTranslate — i18n / l10n](#schlocale-schtranslate-i18n-l10n)
  - [SChChoice / SChChoiceItem — Choice Lists](#schchoice-schchoiceitem-choice-lists)
- [Field Types Reference](#field-types-reference)
- [Gui Types](#gui-types)
- [View Return Types](#view-return-types)
- [File Types](#file-types)
- [Static Asset Types](#static-asset-types)
- [Form Field Types](#form-field-types)
- [Template Tags & Custom Components](#template-tags-custom-components)
- [Advanced: Embedded Python/JS Code](#advanced-embedded-pythonjs-code)
- [Building & Installing](#building-installing)

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

> **Note:** The attribute tables below reflect the `schbuilder` schema at the
> time of writing. The schema evolves between releases — when in doubt,
> inspect `schdevtools/schbuilder/models.py` in your `pytigon_standard_prj`
> checkout for the authoritative field list.

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
| `author_name` | CharField(255) | Author name |
| `author_email` | CharField(256) | Author email |
| `author_www` | CharField(256) | Author website |
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
| `view_type` | CharField(1) | View action type (see below) |
| `param` | CharField(255) | Parameter expression passed to the view (e.g. `"pk"`, `"id"`, or a Python expression) |
| `url` | CharField(255) | Target model or URL path (e.g. `"SChProject"` or `"app.Model"`) |
| `view_code` | TextField | Custom Python view code (editable=False — set via the builder UI) |
| `url_params` | CharField(255) | Extra URL parameters |
| `ret_type` | CharField(1) | Return type (see [View Return Types](#view-return-types)); default `"U"` |
| `asynchronous` | BooleanField | Run as an async view (ASGI) |
| `extra_code` | TextField | Auxiliary code (helpers, imports) compiled alongside the view |
| `doc` | TextField | Documentation |

**View type (`view_type`):**

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
| `url` | CharField(255) | URL or view name |
| `url_type` | CharField(1) | Link target: `-`=default, `desktop`, `panel`, `header`, `footer`, `script`, `pscript`, `browser`, `browser_panel`, `browser_header`, `browser_footer` |
| `perms` | CharField(255) | Permission required to see the item |
| `icon` | CharField(256) | Icon path |
| `icon_size` | CharField(1) | `0`=small, `1`=medium, `2`=large |
| `icon_code` | TextField | Inline SVG icon |

---

### SChForm — Form Definition

Defines a Django form class.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Form class name |
| `module` | CharField(255) | Module label / grouping |
| `process_code` | TextField | Code injected into the form's `__init__` / processing flow |
| `end_class_code` | TextField | Code appended at the end of the form class body |
| `end_code` | TextField | Code emitted after the class definition (helpers, registration) |
| `asynchronous` | BooleanField | Generate an async form handler (ASGI) |
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
| `required` | BooleanField | Required flag |
| `label` | CharField(255) | Label text |
| `initial` | CharField(255) | Initial value |
| `widget` | CharField(128) | Widget class (e.g. `TextInput`, `Select`, `CheckboxInput`) |
| `help_text` | CharField(255) | Help text |
| `error_messages` | TextField | Custom error messages (JSON or Python dict) |
| `param` | CharField(255) | Extra field parameters |

---

### SChTemplate — Template

Defines a Django template file.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | File name (e.g. `"list.html"`) |
| `direct_to_template` | BooleanField | Expose as a direct-to-template URL (no view) |
| `url` | CharField(255) | URL pattern when `direct_to_template` is set |
| `url_parm` | CharField(255) | URL parameter for the direct-to-template route |
| `template_code` | TextField | Template source code (iHTML or HTML) |
| `static_files` | CharField(255) | Static file dependencies to bundle |
| `tags_mount` | CharField(255) | Template tag library mount point |
| `asynchronous` | BooleanField | Generate an async template view |

---

### SChStatic — Static Asset

Defines a static file bundled with the application. The `type` field
determines how the asset is processed at build time (see
[File Types](#file-types)).

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `type` | CharField(1) | Asset type code (see [File Types](#file-types)) |
| `name` | CharField(255) | File name |
| `content` | TextField | File content |
| `doc` | TextField | Documentation |

---

### SChFile — Custom File

An arbitrary file to include in the generated application (e.g. a README,
a license, a config file). Same shape as `SChStatic` but stored under
non-static paths.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `type` | CharField(1) | File type code (see [File Types](#file-types)) |
| `name` | CharField(255) | File path/name |
| `content` | TextField | File content |
| `doc` | TextField | Documentation |

---

### SChTask — Background Task

Defines a background task. The `code` field holds the full task body
(function definition + optional `init_schedule` registration); pytigon
dispatches it via `django_q.async_task` or the `SChScheduler` depending on
runtime configuration.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Task name |
| `code` | TextField | Task source code (function + schedule registration) |
| `doc` | TextField | Documentation |
| `perms` | CharField(255) | Permission required to manage the task |
| `publish` | BooleanField | Publish the task to the task list UI |
| `publish_group` | CharField(255) | Grouping label for published tasks |

---

### SChChannelConsumer — WebSocket Consumer

Defines a Django Channels consumer for WebSocket communication.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Consumer name |
| `consumer_type` | CharField(64) | Consumer class: `WebsocketConsumer`, `AsyncWebsocketConsumer`, `JsonWebsocketConsumer`, `AsyncJsonWebsocketConsumer`, `AsyncHttpConsumer`, `AsyncConsumer`, `SyncConsumer` |
| `url` | CharField(255) | WebSocket URL route |
| `consumer_code` | TextField | Custom consumer code |
| `doc` | TextField | Documentation |

---

### SChLocale, SChTranslate — i18n / l10n

**SChLocale** represents a locale (language) for the application.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChApp | Owning app |
| `name` | CharField(255) | Language name (also used as the locale code, e.g. `"pl"`, `"en"`) |

**Children:** `SChTranslate` nodes.

**SChTranslate** represents a single translation string.

| Attribute | Type | Description |
|-----------|------|-------------|
| `parent` | PtigHiddenForeignKey→SChLocale | Owning locale |
| `description` | CharField(255) | Source string (msgid) |
| `translation` | CharField(255) | Translated string (msgstr) |
| `status` | CharField(1) | Translation status flag |

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

The `SChField.type` attribute accepts either a standard Django field class
name or a Pytigon-extended type. Extended types are resolved by the builder
into concrete field classes from `pytigon_lib.schdjangoext.fields`.

### Standard Django Fields

`AutoField`, `BooleanField`, `CharField`, `CommaSeparatedIntegerField`,
`DateField`, `DateTimeField`, `DecimalField`, `EmailField`, `FileField`,
`FilePathField`, `FloatField`, `ImageField`, `IntegerField`,
`GenericIPAddressField`, `NullBooleanField`, `PositiveIntegerField`,
`PositiveSmallIntegerField`, `SlugField`, `SmallIntegerField`, `TextField`,
`TimeField`, `URLField`, `XMLField`, `ForeignKey`, `OneToOneField`,
`ManyToManyField`

### Pytigon Extended Fields

The `Ptig*` names below are aliases exported by
`pytigon_lib.schdjangoext.fields` (e.g. `PtigForeignKey = ForeignKey`).
The non-`Ptig` names are recognised by the builder and mapped to the
appropriate field class or generated code.

| Field | Description |
|-------|-------------|
| `PtigForeignKey` (= `ForeignKey`) | ForeignKey with Pytigon UI integration (search, add, popup form) |
| `PtigManyToManyField` (= `ManyToManyField`) | ManyToManyField with Pytigon UI |
| `PtigHiddenForeignKey` (= `HiddenForeignKey`) | ForeignKey hidden from forms/UI (internal parent links) |
| `PtigForeignKeyWithIcon` (= `ForeignKeyWithIcon`) | ForeignKey with icon support in the UI |
| `PtigManyToManyFieldWithIcon` (= `ManyToManyFieldWithIcon`) | M2M field with icon support |
| `PtigTreeForeignKey` (= `TreeForeignKey`) | ForeignKey for tree/hierarchy structures |
| `UserField` | Custom user-reference field (builder expands to a CharField + helper) |
| `GForeignKey` | GenericForeignKey (builder-generated) |
| `GManyToManyField` | Generic M2M (builder-generated) |
| `GHiddenForeignKey` | Hidden GenericForeignKey (builder-generated) |

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
| `P` | Python compiled to JavaScript (pscript), linked in desktop.html |
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
| `P` | Python→JS via pscript (included in desktop.html) |
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
Python-in-HTML, pscript for JS, SASS for CSS).

---

## Building & Installing

### Project Build

The builder generates a complete Django application from the `.ptigprj` file:

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

1. Parses the `.ptigprj` JSON tree
2. Creates Django app structure under the project directory
3. Compiles Python→JS (pscript), SASS→CSS
4. Compiles Django templates (Pytigon's indentation-based template engine)
5. Generates `.po` translation files

---

## Summary

The `.ptigprj` file is a complete declarative description of a Pytigon
application. It contains:

- **Schema** (tables + fields = Django models)
- **Business logic** (embedded Python code in `table_code`, `view_code`, etc.)
- **UI definition** (menus, templates, static assets, GUI types)
- **API surface** (views with their URLs, return types, filters)
- **Packaging** (install.ini, README, LICENSE, icons)
- **i18n** (locales and translations)

The `schbuilder` app itself is defined this way — the `.prj` file is both
the schema *and* the instance data for the builder tool.
