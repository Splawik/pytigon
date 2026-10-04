**PYTIGON**
=======

*Discover the Power of Pytigon*

Introduction
----------

Pytigon brings together the prowess of several cutting-edge technologies: Python, Django, and wxWidgets. It forms an integrated and seamless development environment that caters to a range of application types.

**Key Advantages of Pytigon:**

- **Versatile Application Development:**
   - Harness the versatility of the Python language.
   - Leverage the capabilities of the Django web framework.
   - Utilize the wxWidgets toolkit to create desktop applications.
   - Craft modern web clients using Bootstrap and custom Web Components.

- **Cross-Platform Compatibility:**
   - Develop desktop applications for Linux, Windows, and macOS.
   - Create web-based clients for both mobile and desktop usage.

- **Robust Component Integration:**
   - Immerse yourself in Python's philosophy throughout:
      - Employ modified Django templates that align with Pythonic indentation principles (IHTML format).
      - Seamlessly integrate Python with JavaScript using the embedded pscript compiler.
      - Define custom HTML elements (Web Components) using Python syntax.

- **All-in-One Pytigon IDE:**
   
   The Pytigon IDE empowers you to not only create programs but also generate installation packages, creating translations for multilingual versions, e.t.c

Installation
-----------

Pytigon is published as several packages that build on each other. Pick the one
that matches what you want to run:

| Package | What it is | Install it when |
|---|---|---|
| `pytigon-batteries` | The runtime package set for Pytigon as a **web server** (Django, Channels, document and PDF tooling, standard projects). | You want to serve Pytigon, for example in Docker. **Start here.** |
| `pytigon-gui` | The **desktop application** (`ptigw`): a wxPython frontend with its own embedded Django server. | You want the graphical application. It installs `pytigon-batteries` for you. |
| `pytigon` | The **base framework**: the Django project, the `ptig` command and the ASGI/WSGI entry points. It is a library, not a runnable install. | You build a custom, reduced system, or embed Pytigon in your own application. |
| `pytigon-standard-prj` | The **standard projects and applications** — the blocks Pytigon is assembled from. | Never install it directly; `pytigon-batteries` and `pytigon-gui` pull it in. |
| `pytigon-lib` | The shared helper library used by everything above. | Never install it directly. |

### Web server (servers, Docker)

```
pip install pytigon-batteries
ptig --help
```

### Desktop application

```
pip install pytigon-gui
ptigw
```

On Linux, install wxPython following the guide at
[`https://wiki.wxpython.org/How to install wxPython`](https://wiki.wxpython.org/How%20to%20install%20wxPython).

On Windows, simply download and execute the installation program. It comes
bundled with a Python environment and all necessary libraries. Alternatively
run `pip install pytigon-gui`.

A Snap package is also available:

```
snap install --beta ptig
```

### Base framework only

```
pip install pytigon
```

This gives you the framework and the `ptig` command, but no project to run.
Commands that need a project will tell you to install `pytigon-batteries`
(web server) or `pytigon-gui` (desktop application).

