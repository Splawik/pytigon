# How to Use the Pytigon Application Documentation

This guide explains how to generate, serve, and maintain API documentation
for the `pytigon` application package using **MkDocs** with the **Material
for MkDocs** theme and **mkdocstrings**.

---

## Quick Start (TL;DR)

```bash
# 1. Enter the pytigon package directory
cd pytigon

# 2. Install dependencies (one-time)
./gen_docs.sh install

# 3. Start live-reload preview server
./gen_docs.sh serve

# 4. Open http://127.0.0.1:8000 in your browser

# 5. When ready, build static HTML
./gen_docs.sh build
# Output is in: pytigon/site/
```

---

## What Is Documented

The documentation covers all Python modules in `pytigon/` **excluding** the
`prj/` subdirectory (project templates):

| Section | Modules |
|---------|---------|
| **Core** | `pytigon_run`, `pytigon_request`, `pytigon_task`, `django_min_init`, `manage`, `ptig` |
| **Commands** | `dispatcher`, `registry`, `handlers`, `errors`, `utils` |
| **Ext Lib** | `autocomplete`, `django_storage`, `naivehtmlparser`, `pygettext` |

---

## File Structure

```
pytigon/
├── mkdocs.yml                    # MkDocs configuration
├── gen_docs.sh                   # Bash script (build/serve/clean/install/deploy)
├── docs/                         # Documentation source
│   ├── index.md                  # Landing page
│   ├── HOWTO.md                  # This file
│   ├── getting-started/
│   │   ├── overview.md           # Architecture overview
│   │   └── quick-import.md       # Import cheat sheet
│   └── api/                      # API reference (auto-generated)
│       ├── pytigon.md
│       ├── pytigon_run.md
│       ├── pytigon_request.md
│       ├── pytigon_task.md
│       ├── django_min_init.md
│       ├── manage.md
│       ├── ptig.md
│       ├── commands.md
│       ├── commands_dispatcher.md
│       ├── commands_registry.md
│       ├── commands_handlers.md
│       ├── commands_errors.md
│       ├── commands_utils.md
│       └── ext_lib.md
└── site/                         # Built output (generated, git-ignored)
```

---

## `gen_docs.sh` Commands

| Command | Description |
|---------|-------------|
| `./gen_docs.sh install` | Install all Python dependencies |
| `./gen_docs.sh build` | Generate static HTML in `site/` |
| `./gen_docs.sh serve` | Start live-reload dev server on port 8000 |
| `./gen_docs.sh clean` | Remove `site/` directory |
| `./gen_docs.sh deploy` | Build and deploy to GitHub Pages |

---

## How mkdocstrings Works

Each API reference page uses the `::: module.path` syntax. For example,
[`docs/api/pytigon_run.md`](api/pytigon_run.md) contains:

```markdown
# pytigon_run – CLI Runner and Command Dispatcher

::: pytigon.pytigon_run
    options:
      show_submodules: false
      members: true
```

This tells mkdocstrings to import `pytigon.pytigon_run`, extract all
public members and their Google-style docstrings, then render them with
signatures, parameter tables, and optional source code.

---

## Adding a New Module

**Step 1:** Create the API reference file:

```bash
cat > pytigon/docs/api/new_module.md << 'EOF'
# new_module – Description

::: pytigon.new_module
    options:
      show_submodules: false
      members: true
EOF
```

**Step 2:** Add the page to [`mkdocs.yml`](../mkdocs.yml) under `nav`:

```yaml
nav:
  - Core:
      - new_module: api/new_module.md
```

**Step 3:** Rebuild:

```bash
./gen_docs.sh build
```

---

## Excluding Modules

Modules are excluded by **not listing them** in `mkdocs.yml`'s `nav` section.
The `prj/` directory is excluded this way – it has no entries in the navigation
tree and mkdocstrings will not import it.

---

## Customizing the Theme

Edit [`mkdocs.yml`](../mkdocs.yml):

- **Color**: Change `theme.palette[].primary` (e.g., `indigo`, `deep-purple`, `teal`)
- **Navigation**: Add/remove entries under `nav`
- **Features**: Toggle under `theme.features`
- **mkdocstrings options**: Adjust `show_source`, `inherited_members`, etc.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mkdocs: command not found` | Run `./gen_docs.sh install` |
| `ModuleNotFoundError` from mkdocstrings | Ensure the module's dependencies (Django, etc.) are installed |
| Import errors from `prj/` | Confirm no nav entries reference `prj/` paths |
| Build is slow | Use `mkdocs serve --dirty` for incremental rebuilds during editing |
