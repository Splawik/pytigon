# appdata — Plugins and Build Assets

`appdata/` holds the runtime assets that ship with the `pytigon` package:
bundled plugins, install templates, and the source assets that compile to
`static/` and `templates/` at build time.

```
appdata/
├── plugins/              # Built plugins (shipped to users)
│   └── standard/         # The standard plugin set
├── plugins_src/          # Plugin sources (before build)
├── icss/                 # Indented CSS sources (compiled to .css)
└── install/
    └── install.ini       # Default packaging template
```

---

## Standard Plugins

Each plugin lives under `appdata/plugins/standard/<name>/` and is enabled
in a project's `.prj` file via the `plugins` attribute (semicolon-separated
paths, e.g. `standard/keymap;standard/tablefilter`).

| Plugin | Purpose |
|--------|---------|
| `autocomplete` | Autocomplete control with server-side dynamic choices |
| `editor` | Styled text editor (Scintilla-based on desktop) |
| `hexview` | Hex viewer for binary data |
| `html_print` | Print HTML content (printer integration) |
| `html_process` | HTML pre-processing pipeline |
| `ifind` | Interactive find / search |
| `image_viewer` | Image viewer with zoom / pan |
| `keymap` | Keyboard shortcut customisation |
| `odf_view` | ODF (OpenDocument) viewer stub |
| `schconsole` | Embedded Python console |
| `shell` | Interactive Python shell |
| `tablefilter` | Advanced table filtering UI |
| `test_tcc` | Test plugin for TCC (Tiny C Compiler) integration |
| `webview` | WebView browser (CEF / wx.html2 / WebKit backends) |

### webview backends

The `webview` plugin is the most complex — it provides a unified browser
abstraction with multiple backends selected at runtime:

| Backend | Use case |
|---------|----------|
| `cef` (Chromium Embedded Framework) | Full Chromium rendering, used on desktop when available |
| `wxwebview` (wx.html2) | Lightweight native WebView, wxPython fallback |
| Browser frame | Plain `wx.Frame` hosting an HTML panel for non-WebView environments |

CEF integration lives in `webview/cef/schcef.py` and `cefcontrol.py`. The
backends are registered in `webview/__init__.py` and selected based on
availability and the `--browser` CLI flag.

---

## Build Pipeline

`appdata/plugins_src/` and `appdata/icss/` contain source forms that are
compiled at build time:

- `plugins_src/*.pyj` → `plugins/.../*.js` (pscript, Python→JS)
- `icss/*.icss` → `static/*.css` (indented CSS, see [IHTML Format](indent.md))
- `templates_src/*.ihtml` → `templates/*.html` (iHTML templates)

The build is driven by `compiletemplates.sh` at the repo root and the
`schdevtools` builder's "Build" action.

---

## install.ini

`appdata/install/install.ini` is the default packaging template copied into
new projects. It controls shortcut creation, Android packaging, and extra
pip dependencies. See [schdevtools — install.ini Format](schdevtools.md#installini-format)
for the full key reference.
