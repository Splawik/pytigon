# pytigon — Architecture

## Overview

pytigon is the main application framework layer. It provides:
- Django server configuration (`schserw/`)
- CLI command dispatcher (`commands/`)
- Template tags and filters (`schserw/schsys/templatetags/`)
- Context processors and system views (`schserw/schsys/`)

## Entry Point

`pytigon_run.py` is the CLI entry point (installed as `ptig`). It dispatches
commands through the Chain of Responsibility pattern in `commands/dispatcher.py`.

## Module Map

```
pytigon/
├── pytigon_run.py          # CLI entry point
├── django_min_init.py      # Minimal Django bootstrap
├── commands/               # CLI command system
│   ├── dispatcher.py       # Command dispatching (Chain of Responsibility)
│   ├── handlers/           # Command handlers (runserver, manage, run, init)
│   └── utils/              # Subprocess utilities
├── schserw/                # Django server
│   ├── urls.py             # URL configuration
│   ├── settings/           # Modular settings (base, features, infra)
│   ├── schsys/             # System views, auth, templates
│   │   ├── views.py        # Core views (dialogs, login, media)
│   │   ├── context_processors.py  # Template context
│   │   └── templatetags/   # Custom template tags and filters
│   │       ├── exsyntax.py       # UI template tags (buttons, trees, forms)
│   │       ├── exsyntax_form.py  # Form-specific tags
│   │       ├── exsyntax_include.py # Inclusion tags
│   │       └── exfiltry.py       # Template filters (string, math, wiki)
│   └── schviews/           # View utilities
└── static/                 # Compiled frontend assets
```

## Settings Architecture

Settings are split into three modules with clean responsibilities:
- `base.py` — Paths, database, i18n, secret key
- `features.py` — Installed apps, middleware, feature flags, template config
- `infra.py` — Logging, storage, caching, channels, security

## Dialog Views

Dialog views (`datedialog`, `listdialog`, `treedialog`, `tabdialog` in
`schsys/views.py`) share a common class hierarchy:
- `_DialogView` — base class with size/dialog/test handling
- `_DateDialogView`, `_ListDialogView`, `_TreeDialogView`, `_TabDialogView` — specific implementations

## Template Tags

`exsyntax.py` provides UI template tags. It re-exports from:
- `exsyntax_form.py` — form rendering tags (`field`, `Form`, `form_item`)
- `exsyntax_include.py` — inclusion tags (`frame`, `subform`, `component`)

`exfiltry.py` provides ~72 template filters for string manipulation, math,
date formatting, markdown, wiki, and model introspection.
