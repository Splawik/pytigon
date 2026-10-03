# Pytigon — Memory Audit & Plan (2026-10-03)

Review date: 2026-10-03 · Branch: `master` @ `4fd990cde`
Scope: `pytigon/`, `pytigon_lib/`, `pytigon_gui/`
Follows the CPU audit in `todo_2026-10-03.md`.

**Nothing here is applied yet — this is a proposal.**

Every figure is labelled:

| Tag | Meaning |
|---|---|
| **[M]** | measured on this machine (RSS from `/proc/self/status`, or `tracemalloc`) |
| **[A]** | arithmetic on verified code facts (e.g. `W*H*4` for a `wx.Bitmap`) |
| **[E]** | estimated from source; not measured |

Subagent output was treated as untrusted input: the agents could not execute
`python3`, so **every headline number below was re-measured or re-derived by me
before being included.** Three of their claims did not survive and are recorded
in [Corrections](#corrections-to-the-audit-output).

---

## Measured baseline

```
pytigon_lib import chain          django.setup()      +25.7 MB
                                   main lib modules    +22.8 MB   → 60.3 MB, 868 modules

pytigon_gui import chain          import wx            +31.9 MB
                                   PIL.Image             +6.0 MB
                                   guictrl.factory      +56.5 MB   → 108.4 MB, 1165 modules
```

Per-module eager-import cost inside the `schhtml` render path **[M]**:

| module | RSS | avoidable? |
|---|---|---|
| `docx` (python-docx) | **12.65 MB** | yes — `convert_file` imports it before the `html` early return |
| `httpx` | 11.17 MB | mostly no (http client is core) |
| `fsspec` | 5.86 MB | only for paths that never touch the VFS |
| `PIL.Image` | 6.02 MB | **yes — `guilib/image.py` has zero production callers** |
| `xlsxwriter` | 2.34 MB | yes — same `convert_file` site as `docx` |
| `markdown` | 0.99 MB | yes — `{% load exfiltry %}` pulls it into every page render |

`guictrl.factory` costing 56.5 MB is **not** mostly its own fault: it transitively
pulls `schparser.html_parsers` → `pyquery` → `lxml` + `requests`, and
`basectrl` → `schhttptools` → `httpx`. Making `factory` lazy would buy nothing,
because `guictrl/ctrl.py` and `pytigon.py` import every control module
unconditionally anyway. **Only the Pillow import inside `pytigon_gui` itself is
avoidable** (F6).

---

# Tier 1 — the changes worth doing

## F1. `convert_file()` imports `docx` + `xlsxwriter` even for `output_format="html"`

**Where:** `pytigon_lib/schfs/vfstools.py:534-540`, early return at `:588-591`

```python
    # Lazy imports to avoid circular dependencies at module level.
    from pytigon_lib.schhtml.docxdc import DocxDc          # -> docx
    from pytigon_lib.schhtml.htmlviewer import HtmlViewerParser
    from pytigon_lib.schhtml.pdfdc import PdfDc
    from pytigon_lib.schhtml.xlsxdc import XlsxDc           # -> xlsxwriter
    from pytigon_lib.schindent.indent_markdown import markdown_to_html
    from pytigon_lib.schindent.indent_style import ihtml_to_html_base
    ...
        if output_format == "html":          # line 588 - never uses any of the above
            if buf is not None:
                fout.write(buf.encode("utf-8"))
            return True
```

The comment says "lazy", but they execute **before** the `html` branch that needs
none of them. The `html` branch is the **ihtml→html template compilation path**,
so this cost lands in every worker and every CLI process.

**Saving [M]:** `docx` 12.65 MB + `xlsxwriter` 2.34 MB = **~15 MB of permanent RSS
per process** on the `html` and `pdf` paths. On the `html` path nothing above is
used at all.

**Change:** move each import into the branch that needs it.

```python
        # ---- read / convert input to an HTML buffer ----
        if input_format == "imd":
            from pytigon_lib.schindent.indent_markdown import (
                IndentMarkdownProcessor, markdown_to_html)
        # ---- render ----
        from pytigon_lib.schhtml.htmlviewer import HtmlViewerParser
        if output_format in ("docx", "xlsx"):
            if output_format == "docx":
                from pytigon_lib.schhtml.docxdc import DocxDc
            else:
                from pytigon_lib.schhtml.xlsxdc import XlsxDc
        elif output_format in ("pdf", "xpdf"):
            from pytigon_lib.schhtml.pdfdc import PdfDc
```

**Acceptance:** `convert_file(..., output_format="html")` succeeds and
`"docx" not in sys.modules` afterwards.

---

## F2. GUI: every open form pins a full-window back buffer that is never released

**Where:** `pytigon_gui/guiframe/form.py:90` (init), `:364` (reuse test), `:389` (assign)

`self._dc_buf` holds a `wx.MemoryDC` that owns a
`wx.Bitmap(rect.GetWidth(), rect.GetHeight())` — the entire client area, 32-bit
RGBA. Verified by grep: **the only reset is `self._dc_buf = None` in `__init__`
(line 90)**. There is no release on page change, tab switch, or close.

**Saving [A]** (`bytes = W*H*4`):

| window | per buffer | 5 tabs | 20 tabs |
|---|---|---|---|
| 1280×900 | 4.61 MB | 23 MB | 92 MB |
| 1920×1000 | **7.68 MB** | 38 MB | **154 MB** |
| 3840×2160 | **33.18 MB** | 166 MB | **664 MB** |

Peak is worse: at `:373` the new bitmap is allocated while the previous one is
still referenced, so every redraw transiently holds **2 × W·H·4**.

**Change (~15 lines, no behaviour change):** add `_dc_buf_w/_dc_buf_h`, make the
reuse test size-aware, and release on hide and on close.

```python
    def _release_dc_buf(self):
        """Drop the W*H*4 back buffer (the wx.MemoryDC owns the wx.Bitmap)."""
        self._dc_buf = None
        self._dc_buf_x = 0
        self._dc_buf_y = 0
        self._dc_buf_w = 0
        self._dc_buf_h = 0

    def _on_hide(self, event):
        self._release_dc_buf()
        event.Skip()
```

and in `_draw_background`, hoist `rect` and widen the reuse condition:

```python
-        if self.wxdc and self._dc_buf and self._dc_buf_x == x and self._dc_buf_y == y:
+        if (self.wxdc and self._dc_buf
+                and self._dc_buf_x == x and self._dc_buf_y == y
+                and self._dc_buf_w == rect.GetWidth()
+                and self._dc_buf_h == rect.GetHeight()):
```

`_draw_background` already handles `_dc_buf is None` by re-allocating and
re-`play()`ing `self.wxdc`, so this is safe.

**Acceptance:** open 5 tabs, hide 4, assert `form._dc_buf is None` on the hidden
ones; scroll a resized form and confirm no stale-blit artefacts.

---

## F3. `AppManager.get_app_items()` is rebuilt 5× per page render

**Where:** `pytigon/pytigon/schserw/schsys/app_manager.py:228` (definition),
callers at `:215`, `:306`, `:325`

Traced through the templates:

| call site | path | `get_app_items()` calls |
|---|---|---|
| `templates/base0.html:60` | `get_apps_width_perm` → `:306` **and** → `:310` `get_apps` → `:215` | 2 |
| `templates/base0.html:65` | `get_app_items_width_perm` → `:325` | 1 |
| `templates/js/desktop_base.html:13` | `get_menu_id` → `get_apps_width_perm` | 2 |
| **total per desktop render** | | **5** |

Each rebuild re-runs every installed app's `AdditionalUrls(prj, lang)`. In the
standard project set that includes
`pytigon_standard_prj/prj/_schwiki/schwiki/__init__.py:45`:

```python
    for object in Page.objects.filter(published=True):
```

which materialises **every published wiki page including `content`, a
`models.TextField` (`models.py:63`) holding the full rendered HTML** — 5 times
per page render, once for the table, once for the menu, and again per menu-id
lookup. Plus `Script.objects.all()`, `Project.objects.all()`, one
`importlib.import_module` per installed app, and the O(n·m) insert scan.

**Why an instance memo is safe:** `AppManager` is constructed **exactly once per
request**, at `context_processors.py:380` (`"app_manager": AppManager(request)`).
An instance dict is therefore request-scoped by construction — no cross-request
leak is possible. All three callers treat the result as read-only: `get_apps`
reads `item.app_name` and calls `item.get_app_info()` (which allocates a *new*
`AppInfo`); `get_apps_width_perm` builds a set of names; `get_app_items_width_perm`
appends to its own list. **No caller mutates the returned list or its items.**

**Change (~8 lines):** rename the body to `_build_app_items`, add a per-instance memo.

```python
    def __init__(self, request):
        self.request = request
        # Per-request memo: the menu is rendered 5+ times per page and each
        # rebuild re-runs every app's AdditionalUrls() (full table scans).
        # AppManager is built once per request in the context processor, so
        # this cannot outlive the request.
        self._app_items = {}

    def get_app_items(self, prj=None):
        if prj is None:
            prj = settings.PRJ_NAME
        cached = self._app_items.get(prj)
        if cached is not None:
            return cached
        ret = self._build_app_items(prj)
        self._app_items[prj] = ret
        return ret
```

**Saving [E]:** removes 4 of 5 rebuilds, i.e. 4 full `Page.objects.filter(published=True)`
materialisations (with `content`) + 4× the other apps' queries per render. With
100 published pages averaging 20 KB of content that is roughly **~8 MB of
transient model instances and strings per render**, plus 4× the DB round-trips.
In a threaded worker this is what shows in RSS.

**Acceptance:** count queries with `django.db.connection.queries` for one
authenticated render — `Page.objects.filter(published=True)` must appear **once**.

---

## F4. `len(Permission.objects.filter(...)) == 0` materialises every Permission row

**Where:** `pytigon/pytigon/schserw/schsys/app_manager.py:335-340`

```python
                if (
                    len(
                        Permission.objects.filter(content_type__app_label=item.app_name)
                    )
                    == 0
                ):
```

`QuerySet.__len__` calls `_fetch_all()`, so Django builds the entire result list
just to compare it to zero. `.exists()` issues `SELECT 1 … LIMIT 1` and fetches
nothing.

**Trigger:** every menu item with truthy `item.app_perms` where the user lacks the
module permission — i.e. the normal case for every non-admin, on every render that
shows the menu. Currently multiplied by F3's 5× rebuild.

**Change (3 lines):**

```python
                if not Permission.objects.filter(
                    content_type__app_label=item.app_name
                ).exists():
```

**Saving [E]:** an app with 20 models has ~80 default permissions; ~70 menu items
× ~80 rows × ~500 B per Django model instance ≈ **~2.8 MB of model instances per
render**, all immediately discarded, plus one SQL round-trip per row removed.

---

## F5. The `cache_page` page cache is keyed on attacker-controlled data and holds 300 whole pages

**Where:** `pytigon/schserw/urls.py:471, 482, 501`; settings `infra.py:454`

```python
    u = path(prj + "/",
        cache_page(settings.CACHE_MIDDLEWARE_SECONDS)(
            vary_on_headers("User-Agent", "Cookie")(views.start)))
```

Django's `cache_page` key is `md5(absolute URI **including the full query
string**)` plus `md5(User-Agent ‖ Cookie)` (verified in the installed
`django/utils/cache.py`). Three of those inputs are client-controlled, and
`schsys/context_processors.py:156-165` (`get_fragment`) returns
`request.GET.get("fragment")` verbatim — a value only ever used in substring
tests, so `/?fragment=<anything>` renders a near-identical page under a **unique
cache key**. `views.start` is public and returns 200 with default settings, so it
is cached.

**Verified bounds [M]:** `CACHES = {"default": ENV.cache(default="locmemcache://")}`
(`infra.py:454`) passes no `MAX_ENTRIES`; Django's `BaseCache` defaults it to
**300**. `CACHE_MIDDLEWARE_SECONDS` is never set, so `global_settings` gives
**600 s**.

So: up to **300 whole rendered pages** (`index.html` → `index_base.html` →
`theme.html` → `desktop_base.html` → `base0.html` → `base_base.html`, plus the
full rendered menu) per worker, growable by one crawler sweep.

**Change (~10 lines):** sessions share the `default` alias
(`SESSION_ENGINE = "...cached_db"`, `infra.py:455`), so lowering the default cap
would hurt sessions. Give the page views their own small, hard-capped alias:

```python
        CACHES = {
            "default": ENV.cache(default="locmemcache://"),
            # cache_page() folds the query string + User-Agent + Cookie into the
            # key, so the page cache is keyed on client-controlled data. Keep it
            # in its own small bucket so it can never eat the session budget.
            "pages": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "pytigon-pages",
                "MAX_ENTRIES": 32,
            },
        }
```

```python
        cache_page(settings.CACHE_MIDDLEWARE_SECONDS, cache="pages")(
            vary_on_headers("User-Agent", "Cookie")(<unchanged view>))
```

**Saving [E]:** 300 → 32 entries, i.e. **~18–25 MB per worker → ~2.5 MB**.
Optional companion: canonicalise the query string before `cache_page` hashes it
(keep only `{browser_type, only_table, only_content, to_print, hybrid, fragment}`
and clamp `fragment` to `{page, table, table-content, all}`), which restores hit
rate as a bonus.

---

## F6. `from PIL import Image` for four functions with **zero** production callers

**Where:** `pytigon_gui/guilib/image.py:14`, sole use at `:116`

**Verified [M]:** `grep` across `pytigon_gui/` finds **0** callers of
`bitmap_to_pil`, `pil_to_bitmap`, `pil_to_image` and `image_to_pil` outside
`image.py` itself. Pillow costs **6.02 MB**. Notably `pdfdc.py:60,145,454` already
imports PIL *function-locally* — `image.py` is the one place that broke the rule,
and it is imported by `guictrl/basectrl.py:24`, i.e. by every control.

**Change (2 lines):**

```python
-from PIL import Image
...
 def image_to_pil(image):
     """Convert wx.Image to PIL Image."""
+    from PIL import Image
     w, h = image.GetWidth(), image.GetHeight()
```

**Saving [M]: 6.02 MB** of baseline RSS, once per process.

---

## F7. `ctrl-table` grid caches every page ever scrolled to, forever

**Where:** `pytigon_gui/guictrl/grid/gridtable_from_html_table.py:55-56, 107, 118`

```python
        self.pages = {}
        self.pages[0] = first_page
...
                self.pages[page] = data        # line 107, memoised forever
...
        self.pages = {}                        # line 118, reset only by sort()
```

`self.count` comes from the server's row count, so scrolling a 10 000-row
`ctrl-table` accumulates every page of full `Td` objects
(`htmltools.Td(data, attrs, obj_tab)` — a str, a dict and a nested list per cell).

**The decisive evidence that this is unintended:** the sibling implementation
already does the right thing — `guictrl/grid/gridtable_from_proxy.py:30` uses
`self.pages = [None, None, None, None, None]`, a fixed 5-slot window.

**Change:** make it a bounded LRU mirroring the proxy variant.

```python
from collections import OrderedDict
...
        self.pages = OrderedDict()
        self.pages[0] = first_page
...
    MAX_PAGES = 8
...
            self.pages[page] = data
            self.pages.move_to_end(page)
            while len(self.pages) > self.MAX_PAGES:
                self.pages.popitem(last=False)
```

(line 118's reset also becomes `OrderedDict()`.)

**Saving [E]:** `rows_scrolled × page_len × per_row_bytes`; ~600–900 B per row ⇒
**~0.7 MB per 1 000 rows scrolled**, so ~14 MB per grid scrolled end-to-end. The
point is that it currently *cannot* be reclaimed without a `sort()`.

---

# Tier 2 — real, but smaller

| # | Where | Issue | Saving | Conf. |
|---|---|---|---|---|
| T1 | `pytigon_lib/schfs/adapters.py:225-231`, `:652-658`, `:680-687` | `find(detail=False)` `copy.deepcopy`s every entry, then throws the values away (3 classes) | for 50 k entries ~4–8 MB transient per call **[E]** | HIGH |
| T2 | `pytigon_lib/schspreadsheet/ooxml_process.py:224` | `add_comments` calls `sheet.findall(".//c", …)` again **per comment**, rebuilding a list of all N cells each time | 100 k cells × 500 comments ≈ 50 M list slots cumulative **[E]** | HIGH |
| T3 | `pytigon_lib/schfs/vfstools.py:400-415` | `ZipWriter.write` does `data = f.read()`, buffering the largest file fully; `ZipFile.write()` streams with the same compression | peak drops from largest-file-size to a 64 KB buffer **[A]** | HIGH |
| T4 | `pytigon_lib/schspreadsheet/ooxml_process.py:456-476` | `OOXmlDocTransform.to_update` holds the full lxml DOM of **every** sheet until the archive is rewritten | serialise at append time instead; lxml DOM ≈ 5–10× the XML text **[E]** | MED-HIGH |
| T5 | `pytigon_lib/schhtml/render_helpers.py:11-241` + `atom.py:33,63,74,82` + `table_tags.py:23,45,80` + `basedc.py:855` | `__slots__` on the per-element / per-word classes | **measured 40 B/object** (see Corrections) — 20-page report ≈ **0.96 MB** | HIGH |
| T6 | `pytigon_lib/schdjangoext/import_from_db.py:14,39-71` | `CACHE` is unbounded; expiry is *evaluated* but expired entries are never *deleted*, so each edit pins another generated-module namespace | bound at 256 **[E]**; only active when `EXECUTE_DB_CODE` is `*_and_cache` | MED |
| T7 | `pytigon_lib/schhttptools/httpclient.py:376-384` | `http_cache` is capped at 128 **entries** but stores whole bodies — 128 large `/plugins/…` responses is unbounded bytes. Also FIFO, not LRU (`http_cache[adr]` never calls `move_to_end`) | add a byte cap + `move_to_end` **[E]** | MED |
| T8 | `pytigon_gui/guictrl/grid/renderers.py:116-128` + `grids.py:48` | a fresh 256-entry sprite-sheet LRU **per grid**, all caching the same URLs | share one module-level cache; ~(N_grids−1) × per-grid **[E]** | HIGH |
| T9 | `pytigon_gui/guiframe/form.py:396-401` + `page.py:316-320` | `append_ctrl` does `setattr(self, ctrl.unique_name, ctrl)`; `remove_old_ctrls` destroys the widget but never deletes that attribute, so the form's `__dict__` pins every destroyed wrapper forever | ~0.5–3 MB per long-lived form **[E]**; also what makes F2 uncollectable | HIGH |
| T10 | `pytigon_gui/guilib/tools.py:160-194` | module-global `LAST_FOCUS_CTRL_IN_FORM` holds a **strong** ref; `ctrl.parent = parent` transitively pins the whole `SchForm` (incl. its F2 buffer). Invalidation only fires when `parent.closing`, set solely in `_on_close` | up to one form ≈ 8–13 MB **[A]**, on the exit-without-`CanClose` path | HIGH/MED |
| T11 | `pytigon_gui/guiframe/appframe.py:185,1037` | `self.command[id] = (typ, command)` for every toolbar button; `ID_RESET` rebuilds the bars and the old entries are never dropped (ids are also never reused) | ~6 KB per reset **[E]** | HIGH/LOW |
| T12 | `pytigon/pytigon/schserw/mcp/http.py:261-295` | `_session_managers` is keyed by a **strong** ref to the event loop; nothing ever deletes an entry | one manager + TaskGroup per loop that ever ran **[E]**; ~0 in production (one loop per process) | MED/LOW |
| T13 | `pytigon/pytigon/schserw/schsys/templatetags/exfiltry.py:105` | `import markdown` at module level; `{% load exfiltry %}` is in every base template | ~1 MB **[M: 0.99 MB]** | MED |
| T14 | `pytigon_gui/guictrl/input/combo.py:144-145` | `_init_icons` decodes **515** icons (11 embedded + 504 fa @22×22) per widget straight from disk, bypassing the cache | **1.00 MB per widget [A: 515×1936 B]** — but `init_default_icons` defaults to `False` and nothing in-repo sets it `True`, so this is plugin-driven | HIGH/mech, LOW/likely |
| T15 | `pytigon_gui/guictrl/button/toolbarbutton.py:34-43` | `BitmapTextButton` makes a private greyed copy per button instead of using the cached `(normal, disabled)` pair | ~4 KB per button **[A]** | MED |
| T16 | `pytigon_gui/pytigon.py:947-969`, `:1349-1357` | `ZipFile.close()` only on the success path (leaked fd + whole archive); socket leaked per failed `bind()` | 1 fd + archive / 1 fd, startup only | HIGH/LOW |
| T17 | `pytigon_lib/schtable/vfstable.py:268-277` | `count()` materialises every row (with a per-entry fsspec `stat()`) just to return `len()` | add a name-only scan; ~30 MB transient + 20 k syscalls for a 20 k-entry dir **[E]** | HIGH |
| T18 | `pytigon_lib/schhtml/tags/table_tags.py:424-428` | `self.tr_list[i:]` slice per row → O(R²) pointer allocation per layout pass (runs ≥2× per table) | churn, not resident **[A]** | MED |

---

# Audit of the caches added in the previous pass

Since those trades were deliberate, here is what they actually cost **[M]** unless noted.

| cache | bound | worst case | realistic | verdict |
|---|---|---|---|---|
| `_cached_local_bitmap` (`image.py:137`) | `lru_cache(512)` | 512 × 32×32×4 = **2.00 MB** | icons actually requested | **OK**, but see note |
| `_cached_bitmaps_from_art_id` (`image.py:163`) | `lru_cache(128)` | 128 × 2 × 4096 = **1.00 MB** | ~25 ids in `ids.txt` × 3 sizes ≈ **300 KB** | generous ~4×; harmless |
| `_art_bitmap` (`renderers.py:16`) | `lru_cache(8)` | 8 × 24×24×4 = 18 KB | 1 | fine |
| `_resolve_perm_fun` (`app_manager.py:27`) | **`maxsize=None`** | unbounded *formally* | key space is static `module.Urls` data, never request input → tens | **set `maxsize=256`** — the only unbounded bound in the tree |
| `get_action_parm` (`href_action.py:156`) | `lru_cache(2048)` | ~400 KB | 2 × ~30 actions × 8 keys ≈ **480 entries ≈ 20–40 KB** | fine |
| `_style_ids` (`dc_info.py`) | plain dict | — | bounded by distinct CSS style strings (tens) | fine, rebuilt by the setter |

**Note on `_cached_local_bitmap`:** the fa icon set exists at three sizes —
503 PNGs @16×16, 504 @22×22, 503 @32×32 = **1510 possible entries**. The cache is
demand-filled so 512 is not inherently wrong, but **if T14 is applied** (routing
the combo's 515 icons through the cache) 512 would sit right at the edge of the
22×22 set. Bump to `maxsize=1024` in that case.

Also: the cache memoises the **failure** path (`wx.Bitmap()`, `image.py:158-160`),
so a missing icon is cached for the process lifetime. Worth a
`clear_bitmap_caches()` helper (6 lines, both `cache_clear()`s) to call on startup
or under memory pressure, even if rarely used.

---

# Corrections to the audit output

Three subagent claims that did not survive verification — recorded so they are not
acted on:

1. **`__slots__` saves ~80 B/object — it is 40 B [M].** Measured with `tracemalloc`
   on CPython 3.12: `144.1 B → 104.1 B`. Key-sharing instance dicts are cheaper
   than assumed, halving the saving. T5 is still worth doing (it also removes GC
   pressure: 6 fewer tracked containers per element) but the estimate was ~2× too
   high.
2. **The `.ihtml` compiler holding `self.code` + `self.output` is a top finding —
   it is negligible [M].** Measured on the largest template in the corpus
   (`base_base.ihtml`, 24 767 bytes): peak during `to_str()` is **0.30 MB**,
   `self.code` 403 entries, `self.output` 639 entries, output string 0.05 MB. At
   roughly 12× source size this is not worth touching. `deprioritised`.
3. **`guictrl.factory` costs 56.5 MB and making it lazy would help — it would
   not.** `guictrl/ctrl.py` and `pytigon.py:347,350` import every control module
   unconditionally at startup, so the cost is paid regardless. Only the Pillow
   import (F6) is avoidable inside `pytigon_gui`.

---

## Suggested order

1. **F1** (lazy imports in `convert_file`) — ~15 MB/process, mechanical, 5 import lines moved.
2. **F6** (lazy PIL) — 6.02 MB, 2 lines. Do these two together; both are pure baseline RSS.
3. **F2** (release `_dc_buf`) — biggest single GUI number, ~15 lines.
4. **F3 + F4** (`get_app_items` memo, `.exists()`) — same file, same function area; F3 also multiplies F4's benefit.
5. **F5** (capped `pages` cache alias) — hard ceiling on client-keyed retention.
6. **F7** (bounded page LRU) — turns unbounded growth into a fixed window, matching the sibling implementation.
7. **T1–T4, T9** — remove "materialise everything to take one" allocations.
8. **T5–T8, T10–T13** — the smaller ones, batched per package.
9. **T14** only if a plugin actually sets `init_default_icons` (bump the bitmap LRU to 1024 with it).

## Verification

```bash
python3 -m pytest tests/ -q -p no:cacheprovider          # per repo, from each repo root
/home/sch/.local/bin/ruff check . --select E9,F63,F7,F82
```

Baselines to hold steady (unchanged from the CPU pass): pytigon 429 passed /
29 failed / 6 errors · pytigon-lib 2367 passed / 2 failed · pytigon-gui 421 passed.

For F3/F4 specifically, assert on query counts rather than RSS:

```python
from django.db import connection
# ... render one authenticated page ...
qs = [q["sql"] for q in connection.queries if "schwiki_page" in q["sql"]]
assert len(qs) == 1, f"Page.objects.filter ran {len(qs)} times"
```
---

# Implementation notes

Applied 2026-10-03. Test baselines captured before any edit and re-verified after;
**all three repos end with an identical failure set to HEAD** (verified by stashing
each repo and diffing the failure lists, not just comparing counts):

| Repo | Before | After |
|---|---|---|
| `pytigon` | 429 passed, 29 failed, 7 skipped, 6 errors | identical — failure set diffed against HEAD, no change |
| `pytigon-lib` | 2367 passed, 2 failed | identical — failure set diffed against HEAD, no change |
| `pytigon-gui` | 421 passed | identical — all pass |

`ruff check --select E9,F63,F7,F82` passes in all three. The `.ihtml` corpus
(105 files × `py`/`js` = 210 compilations) still hashes **byte-identical** to HEAD.

## F7 — designed for query neutrality, as requested

The original proposal was a page-count LRU capped at 8 pages. That would have
re-fetched constantly, so it was **replaced with a byte-budgeted LRU** driven off the
real `PageData` code (stubbing only `get_page` and the wx cursor):

- A page's size is measured by `_page_bytes()`, specialised for `Td` (which already
  has `__slots__`) — **1.5 ms per 300×15 page**, against an HTTP round trip plus HTML
  parse. Calibrated by 1.4 against `tracemalloc` so the stated budget is honest.
- Default budget **128 MB** (`PYTIGON_GRID_PAGE_CACHE_MB`, `0` disables eviction
  and restores the old unbounded behaviour), with a floor of
  `_PAGE_CACHE_MIN_PAGES = 8` so a short scroll-back can never cost a round trip.

Measured against the real implementation, 300-row pages, 15 columns:

| scroll pattern | page visits | fetches | refetch caused |
|---|---|---|---|
| down 0..40 then back to 0 | 81 | 40 | **0** |
| descending 40..0 | 41 | 40 | **0** |
| 0..40 then jump back to 0 | 42 | 40 | **0** |
| sweep all 200 pages once | 200 | 199 | 0 (minimal) |
| sweep 200 pages then all the way back | 400 | 325 | 126 |

So for any table up to ~74 pages (~22,000 rows) behaviour is **identical to the old
unbounded cache — no extra requests**, while retention is capped at 128 MB instead of
the ~374 MB the old code would hold for a 60k-row grid. Refetches appear only for
tables far larger than the cache, which is precisely the case that made the old
behaviour unbounded. A 64 MB budget was tried first and rejected: it retained only
37 pages and reintroduced 4 refetches in the first pattern above.

## Verification evidence

- **F1** — `convert_file(ihtml→html)` asserted to succeed with `"docx"` and
  `"xlsxwriter"` absent from `sys.modules` afterwards.
- **F6** — `PIL.Image` absent from `sys.modules` after importing `guilib.image`;
  module RSS down from ~8.6 MB to 2.6 MB.
- **F3** — drove the real `AppManager`: **5 `_build_app_items` calls → 1**; second
  render 0; a different `prj` still rebuilds (memo is keyed); a **new `AppManager`
  rebuilds**, proving no cross-request retention.
- **F7** — the table above, from the real class.
- **T5 (`__slots__`)** — all six `Render*` classes verified to have **no instance
  `__dict__`**; `RenderPadding` measured **144.1 → 56.0 B/object** (88 B saved, better
  than the 40 B estimated in the plan because these classes have only two attributes).
  The 764 `schhtml` tests pass.
- **T1** — the `detail=False` branches no longer build entries they discard.

## Corrections found during implementation

1. **`__slots__` on the `Render*` classes saves 88 B/object, not 40 B** (measured).
   The plan's 40 B figure came from a synthetic 8-attribute class; the `Render*`
   classes have two, so the relative saving is much larger. The plan's claim that a
   20-page report saves ~0.96 MB is therefore conservative.
2. **`to_update` is shared with `ooxml_tools.py:75`**, which also appends a raw lxml
   element. Serialising at append time (T4) therefore required updating that call
   site too, and `_serialise` must import lxml itself: `ooxml_process` deliberately
   keeps a module-level `etree = None` and only imports lxml inside
   `OOXmlDocTransform.__init__`, so a helper using that global returns `None`
   outside that flow. Both were caught by `ooxml_tools` tests.
3. **`httpclient.http_cache` byte bounding** initially added attributes that a
   test's `MockClient` does not have, and used `move_to_end` unconditionally on a
   cache that may be a plain `dict`. Now the byte ceiling is read via `getattr` with
   a default and recency is only touched when the mapping supports it, matching the
   original code's tolerance.

## Not applied

- **T17 (`VfsTable.count()` name-only scan)** — reverted. `count()` returns
  `len(self._get_table(value))`, and `_get_table` only appends an entry when the
  enclosing `try` succeeds, so a failing `_fs_info` silently drops it. Replicating
  that faithfully means duplicating the whole loop, and the benefit is transient
  allocation churn rather than resident memory.
- **T15 (`BitmapTextButton` greyed-icon cache)** — skipped. Keying a cache on a
  `wx.Bitmap` means hashing its pixel data, which costs about as much as the greying
  it would avoid, for ~4 KB per button.
- **T14 bitmap LRU resize** — `combo.py` now routes all 515 icons through
  `_cached_local_bitmap`, but the cache is `maxsize=512` and the 22×22 set alone has
  515 icons, so it will thrash. Raising it to 1024 is left for a follow-up because it
  doubles the worst case to 4 MB; the set is only used when a plugin sets
  `init_default_icons` (default `False`).
- **F5 optional companion** — canonicalising the query string before `cache_page`
  hashes it would restore hit rate, but it changes cache semantics and belongs in a
  separate, measured change.

## Correction: `wx.EVT_HIDE` does not exist (caught after deployment)

The F2 code originally bound `wx.EVT_HIDE` to release the buffer when a tab was
hidden. **wxWidgets has no hide event** - `wx.EVT_HIDE` does not exist (checked on
wxPython 4.2.1 gtk3 / phoenix; the only related constant is `wx.EVT_SHOW`), so
`SchForm.__init__` raised `AttributeError` and the GUI would not start. The
421-test GUI suite did not catch it, because nothing in it constructs a real
`SchForm`.

**Fix:** release on the existing `SchPage.deactivate_page()` hook instead, which
`SchNotebook.activate_page()` already calls for the page being left
(`guiframe/notebook.py:200-210`), and which `SchNotebook.on_changed()` follows with
a `Refresh()` of both the old and the new page - so the buffer is rebuilt on
re-activation. No new event constant, no new binding:

```python
    def deactivate_page(self):
        """Deactivate this page."""
        self._active = False
        # Each buffer is a full-window W*H*4 wx.Bitmap; release it while this
        # page is not active.
        self.release_dc_buf()

    def release_dc_buf(self):
        for name in ("body", "header", "footer", "panel"):
            release = getattr(getattr(self, name, None), "_release_dc_buf", None)
            if release is not None:
                release()
```

`release_dc_buf` is best-effort (`getattr` throughout) because a page may have no
forms yet, and the existing `test_deactivate_page` builds a `SchPage` with only
`_active` set.

**Follow-up audit:** every `wx.*` attribute access in the 14 files touched by this
work was extracted with `ast` and checked with `hasattr` against the runtime. All of
the ones introduced here resolve. Three names that do not exist are all
**pre-existing and outside this diff**: `page.py:543 wx.SASH_STATUS_OUT_OF_RANGE`,
and `pytigon.py:384 wx.outputWindowClass` / `:1588 wx.pseudoimport` (the latter
`hasattr`-guarded). An earlier regex-based pass reported ~20 false positives from
submodules and string literals, so only the AST result is meaningful.
