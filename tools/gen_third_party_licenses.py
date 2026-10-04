#!/usr/bin/env python3
"""Regenerate THIRD_PARTY_LICENSES.md and NOTICE for the bundled frontend.

The classpath of redistributed JavaScript is defined by
``frontend/js_requirements.txt`` (what esbuild bundles into
``pytigon/static/pytigon-lib.js``) plus ``frontend/static_files.txt`` (files
copied verbatim into ``pytigon/static``). This script reads the installed
versions and license files from ``frontend/node_modules`` and rewrites both
files in the repository root.

Run from the repository root after changing frontend dependencies:

    ptig python tools/gen_third_party_licenses.py

It has no third-party Python dependencies.
"""

import datetime
import json
import os
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parent.parent
FE = REPO / "frontend"
NM = FE / "node_modules"
OUT = REPO / "THIRD_PARTY_LICENSES.md"
NOTICE = REPO / "NOTICE"

LICENSE_NAMES = re.compile(r"^(licen[cs]e|copying|notice|unlicense)", re.I)


def req_pkg(line):
    """Return the package name for a js_requirements.txt entry, or None."""
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("./"):
        return None
    if line.startswith("@"):
        return "/".join(line.split("/")[:2])
    return line.split("/")[0]


def norm_license(lic):
    """Normalise the many shapes of a package.json license field."""
    if lic is None:
        return "Unspecified"
    if isinstance(lic, dict):
        lic = lic.get("type", "Unspecified")
    if isinstance(lic, list):
        lic = " OR ".join(
            (x.get("type", "?") if isinstance(x, dict) else str(x)) for x in lic
        )
    return str(lic).strip().strip("()") or "Unspecified"


def resolve(name):
    """Read a package's version, license and shipped license files."""
    path = pathlib.Path(os.path.realpath(NM / name))
    manifest = path / "package.json"
    if not manifest.exists():
        return None
    meta = json.loads(manifest.read_text(encoding="utf-8"))
    license_id = meta.get("license")
    if license_id is None:
        license_id = meta.get("licenses")
    files = [
        path / entry
        for entry in sorted(os.listdir(path))
        if (path / entry).is_file() and LICENSE_NAMES.match(entry)
    ]
    return {
        "name": name,
        "meta": meta,
        "license": norm_license(license_id),
        "files": files,
    }


def _read_texts(files):
    out = []
    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        except OSError:
            continue
        if text:
            out.append(text)
    return out


def collect():
    """Collect the redistributed components."""
    bundle = []
    for line in (FE / "js_requirements.txt").read_text().splitlines():
        name = req_pkg(line)
        if name and name not in bundle:
            bundle.append(name)
    # Copied to static via frontend/static_files.txt
    extra = ["pouchdb"]
    rows = []
    for name in bundle + [x for x in extra if x not in bundle]:
        resolved = resolve(name)
        if resolved:
            rows.append(resolved)
    return rows


def render(rows, today):
    """Render THIRD_PARTY_LICENSES.md."""
    out = [
        "# Third-Party Licenses\n",
        "Pytigon bundles and redistributes the third-party components listed "
        "below. Each component remains the property of its respective copyright "
        "holder and is used under the terms of its license. This file was "
        "generated from the versions vendored in `frontend/` and "
        f"`pytigon/static/` on {today}.\n",
        "Pytigon itself is licensed under **LGPL-2.1-or-later** (see `LICENSE`); "
        "the licenses below apply only to the third-party components.\n",
        "## 1. Bundled JavaScript (`pytigon/static/pytigon-lib.js`, "
        "`pytigon-lib.css`)\n",
        "| Component | Version | License |",
        "|---|---|---|",
    ]
    for row in rows:
        out.append(
            f"| {row['name']} | {row['meta'].get('version', '?')} | "
            f"{row['license']} |"
        )
    out.append("")
    out.append("## 2. License texts\n")
    for row in rows:
        out.append(
            f"### {row['name']} {row['meta'].get('version', '')} — "
            f"{row['license']}\n"
        )
        homepage = row["meta"].get("homepage")
        if homepage:
            out.append(f"Homepage: {homepage}\n")
        texts = _read_texts(row["files"])
        if texts:
            for text in texts:
                out.append(f"```\n{text}\n```\n")
        else:
            out.append(
                "_The package does not ship a license file; the identifier "
                "above is taken from its `package.json`. See the project's "
                "homepage for the full text._\n"
            )

    out.append("## 3. Redistributed static assets\n")
    out.append("| Asset | License | Notes |")
    out.append("|---|---|---|")
    out.extend(
        f"| {name} | {lic} | {note} |"
        for name, lic, note in [
            ("Bootstrap 5 (`static/bootstrap/`)", "MIT", "Same license as the bundled `bootstrap` package."),
            ("Bootswatch themes (`static/themes/`)", "MIT", "Bootstrap theme collection; no license file shipped."),
            ("Bootstrap Icons (`static/icons/bootstrap-icons/`)", "MIT", "See `static/icons/bootstrap-icons/LICENSE`."),
            ("GNOME-derived icon theme (`static/icons/16x16`, `22x22`, `32x32`)", "Public Domain", "See `static/icons/COPYING`; authors in `static/icons/AUTHORS`."),
            ("Material Design Icons (`static/icons/scalable/mdi-svg/`)", "Apache-2.0 (upstream)", "License text is NOT shipped; verify before public release."),
            ("Fork Awesome (`static/fonts/fork-awesome/`)", "MIT (CSS/LESS/SCSS), CC-BY-3.0 (other files), SIL OFL 1.1 (font)", "See `static/fonts/fork-awesome/LICENSES`."),
            ("DejaVu fonts (`static/fonts/`)", "Bitstream Vera / Arev (permissive)", "No license file shipped; see https://dejavu-fonts.github.io/License.html"),
            ("PouchDB browser distribution (`static/vanillajs_plugins/pouchdb/`)", "Apache-2.0", "Same license as the npm `pouchdb` package."),
            ("Pygments web assets (`static/vanillajs_plugins/pygments/`)", "Public Domain (UNLICENSE)", "See `static/vanillajs_plugins/pygments/UNLICENSE.txt`."),
        ]
    )
    out.append("")
    out.append("## 4. Vendored JavaScript (`frontend/not_node_modules/`)\n")
    out.append("| Component | License | Notes |")
    out.append("|---|---|---|")
    out.extend(
        f"| {name} | {lic} | {note} |"
        for name, lic, note in [
            ("csrf.js (`csrf/csrf.js`)", "BSD-3-Clause", "From Django (CSRF protection)."),
            ("jsi18n.js (`jsi18n.js`)", "BSD-3-Clause", "From Django (JavaScript i18n)."),
            ("jquery.draggable.js", "MIT", "jQuery UI draggable plugin."),
            ("bootstrap5-editable (`bootstrap5-editable/`)", "MIT", "x-editable, (c) Vitaliy Potapov."),
            ("sidebar-menu (`sidebar-menu/`)", "See project", "Third-party sidebar menu plugin."),
            ("pytigon_lib_init.js", "LGPL-2.1-or-later", "Pytigon's own code."),
            ("pytigon-tools.js", "LGPL-2.1-or-later", "Pytigon's own code."),
            ("fab (fab.css), tree (tree.css), select2-material.css", "See project", "Pytigon UI assets; verify before redistribution."),
        ]
    )
    out.append("")
    out.append("## 5. Action items before a public release\n")
    out.append(
        "- `bootstrap-ajax-typeahead` states no license and ships no license "
        "file; confirm its terms with upstream or replace it.\n"
        "- Material Design Icons: add the upstream Apache-2.0 text (not shipped).\n"
        "- Entries marked \"See project\" (sidebar-menu, fab/tree/select2-material) "
        "need an explicit license.\n"
        "- DejaVu fonts ship without a license file; include the Bitstream Vera / "
        "Arev text.\n"
    )
    return "\n".join(out) + "\n"


def render_notice():
    """Render the NOTICE file."""
    return "\n".join(
        [
            "Pytigon",
            "Copyright (C) Sławomir Chołaj and contributors",
            "",
            "This product includes software developed by third parties.",
            "",
            "Pytigon is licensed under the GNU Lesser General Public License v2.1",
            "(or, at your option, any later version). See LICENSE.",
            "",
            "Bundled JavaScript libraries (Bootstrap, jQuery, Select2, PouchDB, htmx,",
            "SweetAlert2 and others) are MIT, Apache-2.0, BSD or 0BSD licensed. Icon",
            "and font assets include Bootstrap Icons (MIT), a public-domain icon",
            "theme, Fork Awesome (MIT / CC-BY-3.0 / SIL OFL 1.1) and DejaVu fonts",
            "(Bitstream Vera / Arev).",
            "",
            "The complete list of third-party components and their license texts is",
            "in THIRD_PARTY_LICENSES.md.",
            "",
        ]
    )


def main():
    """Regenerate both files."""
    rows = collect()
    today = datetime.date.today().isoformat()
    OUT.write_text(render(rows, today), encoding="utf-8")
    NOTICE.write_text(render_notice(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"wrote {NOTICE} ({NOTICE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
