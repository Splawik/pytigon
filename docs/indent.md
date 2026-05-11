# IHTML Format Documentation

## Overview

IHTML (Indent HTML) is an indentation-based template format used in the Pytigon framework. It is a whitespace-significant syntax that compiles to standard Django/Jinja2 HTML templates. The key principle: **indentation determines nesting, eliminating the need for closing tags**.

Files use the `.ihtml` extension and are converted to `.html` (Django templates) by the converter in [`pytigon_lib/schindent/indent_style.py`](../pytigon_lib/schindent/indent_style.py). The main entry point for conversion is the function [`ihtml_to_html()`](../pytigon_lib/schdjangoext/django_ihtml.py).

## Fundamental Rules

### 1. Indentation Defines Nesting

Like Python, each level of indentation (4 spaces per level) represents a deeper nesting level. When indentation decreases, the previous element is automatically closed.

```
div class=container
    p
        ...Hello World
```

Compiles to:

```html
<div class="container">
    <p>
        Hello World
    </p>
</div>
```

### 2. Line Structure

Each line has the following general structure:

```
<indentation><element> <attributes>...<text content>
```

- **Indentation**: spaces that define nesting depth
- **Element**: an HTML tag name, Django template tag, or special block marker
- **Attributes**: separated by `,,,` (triple comma)
- **Text content**: prefixed with `...` (triple dot)

## HTML Elements

### Basic Elements

Write HTML tags as the element name followed by attributes:

```
div class=container,,,id=main
    p style=color:red...Hello World
    span...Some text
```

Compiles to:

```html
<div class="container" id="main">
    <p style="color:red">Hello World</p>
    <span>Some text</span>
</div>
```

### Attributes

Attributes are separated by `,,,` (three commas). The format is:

```
tagname attr1=value1,,,attr2=value2,,,attr3
```

- `key=value` pairs produce `key="value"` in HTML
- Bare words (no `=`) produce boolean attributes: `checked,,,disabled` → `checked disabled`
- Django template expressions are passed through: `class={{my_class}},,,id={{my_id}}`

### Self-Closing (Void) Elements

The following elements are treated as self-closing: `br`, `meta`, `input`, `hr`, `img`, `link`.

```
meta charset=utf-8
br
input type=text,,,name=username
```

Compiles to:

```html
<meta charset="utf-8" />
<br />
<input type="text" name="username" />
```

### Text Content

Text after an element is specified with `...` (three dots) between the element/attributes and the content:

```
p...This is a paragraph
h1...Page Title
span class=highlight...Important text
```

Compiles to:

```html
<p>This is a paragraph</p>
<h1>Page Title</h1>
<span class="highlight">Important text</span>
```

### Element Chaining with `:::`

Use `:::` to chain multiple elements at the same indentation level:

```
tr:::td...Cell 1:::td...Cell 2
```

Compiles to:

```html
<tr>
    <td>Cell 1</td>
    <td>Cell 2</td>
</tr>
```

The first element after `:::` gets the parent's indentation level, subsequent ones get +1 level. This is particularly useful for table rows and list items.

## Django Template Tags

### Template Tags (`%`)

Lines starting with `%` (as the first non-whitespace character) are Django template tags:

```
% load exfiltry
% load static
% extends 'base.html'|translate:lang
% if user.is_authenticated
    p...Welcome, {{ user.username }}
% else
    p...Please log in
```

Compiles to:

```html
{% load exfiltry %}
{% load static %}
{% extends 'base.html'|translate:lang %}
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}</p>
{% else %}
    <p>Please log in</p>
{% endif %}
```

### Auto-Closing Tags

The `%` tag automatically closes when the next line has equal or lesser indentation.

**Tags with `:` suffix auto-close immediately** (generating both opening and closing tags):

```
% if user.is_authenticated:
    p...Welcome
```

Compiles directly to:

```html
{% if user.is_authenticated %}
    <p>Welcome</p>
{% endif %}
```

Auto-closing template tags include: `for`, `if`, `ifequal`, `ifnotequal`, `ifchanged`, `block`, `filter`, `with`, and any tag with `_ext` in its name.

Tags that do **not** auto-close (even with `:`): `else`, `elif`.

### Blocks (`%%`)

`%%` defines a Django `{% block %}` ... `{% endblock %}` pair:

```
%% content
    div class=main
        p...Page content goes here
```

Compiles to:

```html
{% block content %}
    <div class="main">
        <p>Page content goes here</p>
    </div>
{% endblock %}
```

If the next line has lesser or equal indentation (and is not empty), the block is rendered as a self-closing pair on one line:

```
%% title...{{title}}
```

Compiles to:

```html
{% block title %}{{title}}{% endblock %}
```

### Template Tag with Body (`%` + indented content)

When a `%` tag is followed by indented content (without a colon), it wraps the content:

```
% if user.is_authenticated
    p...Welcome, {{ user.username }}
```

Compiles to:

```html
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}</p>
{% endif %}
```

The end tag is automatically inserted when indentation returns to or below the original level.

### `{{ block.super }}` and `{% ... %}` Inline

Standard Django template syntax can be freely mixed in text content:

```
p...{{ variable|filter }} and {% url 'name' %} and {% static 'path' %}
```

## Special Multi-Line Block Markers

When a line contains a special marker, the subsequent indented lines form a code block that undergoes specific processing.

### `>>>` - Raw Text Block

Preserves content as-is (verbatim):

```
script
    >>>...console.log('hello');
        ...console.log('world');
    <<<
```

The `<<<` marker on a separate line terminates the block. The `...` prefix on each line within the block is stripped, and content is preserved with its original formatting.

### `{:}` - CSS / Indented Style Block

Lines below `{:}` use an indentation-based CSS-like syntax where colons replace braces:

```
style type=text/css{:}
    body:
        font-family: sans-serif
        font-size: 120%

    h1:
        font-weight: bold
        font-size: 200%
```

This compiles to standard CSS within `<style>` tags. The `{:}` block syntax uses indentation instead of `{` `}` and `:` instead of `{`.

### `===` - Python Code Block (wxPython/desktop templates)

Embedded Python code for wxPython desktop forms:

```
script language=python===>
    def init_form(self):
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_click)
        self.save_btn.Disable()
```

The `===>` marker starts a Python code block. The indentation of the first line after the marker determines the base indentation for the block.

### `script language=python` - Python Code Block

Alternative syntax for Python code blocks (equivalent to `===>`):

```
script language=python
    def init_form(self):
        ...
```

### `pscript` - Python-to-JavaScript Block

Python code that is compiled to JavaScript via pscript:

```
pscript
    def handle_click(event):
        console.log(event.target)
        return False
```

Compiles to equivalent JavaScript wrapped in `<script>` tags.

### `script language=py2javascript` - Alternative Py→JS Syntax

Alternative syntax for Python-to-JavaScript compilation:

```
script language=py2javascript
    def handle_click(event):
        return False
```

### `%component` - Component Python→JS Block

```
%component MyComponent:
    def __init__(self):
        self.counter = 0
```

Specific syntax for defining components that compile from Python to JavaScript.

### `###>` - Markdown Block

```
###>
    # Section Title

    - item 1
    - item 2

    **bold text** and *italic*
```

The content is processed as Markdown and converted to HTML. Uses Python `markdown` library with extensions: abbr, attr_list, def_list, fenced_code, footnotes, md_in_html, tables, admonition, codehilite.

### `^^^` - Passthrough Mode

If `^^^` appears anywhere in the file, the entire file is treated as raw content and passed through without any conversion. Useful for files that should not be processed.

```
^^^
This entire content will be left as-is, no conversion applied.
```

## Table Shorthand

IHTML provides a concise table syntax using square brackets:

### Data Rows: `[ ... ]`

```
[Column 1 | Column 2 | Column 3]
```

Compiles to:

```html
<tr><td>Column 1</td><td>Column 2</td><td>Column 3</td></tr>
```

### Header Rows: `[[ ... ]]`

```
[[Name | Age | City]]
```

Compiles to:

```html
<tr><th>Name</th><th>Age</th><th>City</th></tr>
```

### Multiple Rows

Each bracketed line represents one table row:

```
[[Product | Price | Stock]]
[Widget A | $10 | 50]
[Widget B | $15 | 30]
```

## Translation Support

### `_()` - Gettext Translation

Standard gettext function calls are processed for translation:

```
p..._("Hello World")
title..._(Welcome)
```

### `_` - Simple Translation Prefix

A line starting with `_` (not `_(`) triggers simple translation of the rest of the line:

```
_ Settings
_ User Profile
```

## Special Constructs

### File References (`@@@`)

If the first line of an `.ihtml` file starts with `@@@`, it references an external file:

```
@@@path/to/template.ihtml
... content that replaces @@@ in the referenced file
```

This merges the current file content into the referenced template where `@@@` appears.

### Output Processors (`@@(`)

The `@@(processor://value)` or `@@(processor-value)` syntax invokes an output processor:

```
a href=#...@@(fa://cog)
```

The example above renders a Font Awesome icon via the `fa` output processor. Available processors are configured in [`django_ihtml.py`](../pytigon_lib/schdjangoext/django_ihtml.py).

### Inline Content (`<inline:>`)

Wraps content that should have no extraneous whitespace between HTML tags:

```
<inline:>
    span...Hello
    span...World
</inline:>
```

Removes newlines and normalizes spacing between the contained elements.

### Line Continuation (`\\`)

A trailing `\\` at the end of a line joins it with the next line:

```
div class=very-long-class-name\\
    p...Content
```

## Escaping and Special Characters

### `.` at Start of Line (Literal Text)

If a line starts with `.` (dot), it is treated as raw text content rather than an element:

```
...This is raw text, not an element definition
```

### Lines Starting with Non-Alphabetic Characters

Lines that do not start with `%` or an alphabetic character (a-z, A-Z) are treated as raw text or Django template variable output.

## Default Element Configurations

The Django-aware converter in [`django_ihtml.py`](../pytigon_lib/schdjangoext/django_ihtml.py) configures:

**Self-closing elements**: `br`, `meta`, `input`

**Auto-closing template tags**: `for`, `if`, `ifequal`, `ifnotequal`, `ifchanged`, `block`, `filter`, `with`

**Non-auto-closing template tags**: `else`, `elif`

## File Conversion

### CLI Conversion

The [`ihtml2html.py`](../pytigon/prj/schscripts/ihtml2html.py) script provides command-line conversion:

```bash
# Convert .ihtml to .html
python ihtml2html.py template.ihtml -o template.html

# Convert .html to .ihtml
python ihtml2html.py template.html -o template.ihtml
```

### Programmatic Conversion

```python
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

# Convert from file
html = ihtml_to_html('path/to/template.ihtml')

# Convert from string
html = ihtml_to_html(None, input_str='div...Hello')
```

## Complete Examples

### Example 1: Simple Page Template

```
% extends 'base.html'|translate:lang
% load static

%% content
    div class=container
        h1...Welcome to Pytigon
        p class=lead...This is a simple page.
        % if user.is_authenticated
            p...Hello, {{ user.username }}!
        % else
            p...Please log in.
```

### Example 2: Table with Data

```
table class=table table-striped
    thead
        tr
            [[ID | Name | Status]]
    tbody
        % for item in object_list
            tr
                [{{ item.id }} | {{ item.name }} | {{ item.status }}]
```

### Example 3: Form with Fields

```
% load exfiltry
% load django_bootstrap5

form method=post,,,class=form-horizontal
    % csrf_token
    % bootstrap_field form.username layout='horizontal'
    % bootstrap_field form.email layout='horizontal'
    div class=form-group
        button type=submit,,,class=btn btn-primary...Submit
```

### Example 4: Template Block Override

```
% extends 'base.html'

%% title...My Custom Title

%% head_start
    {{ block.super }}
    link rel=stylesheet,,,href={% static 'custom.css' %}

%% content
    div class=custom-content
        {{ block.super }}
```

### Example 5: Python-to-JS Component

```
% component Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        self.update_display()

    def render(self):
        return f'''<div>
            <span>{self.count}</span>
            <button onclick="increment()">+</button>
        </div>'''
```

### Example 6: Markdown Content Block

```
div class=documentation
    ###>
        # API Reference

        ## Authentication

        The API uses token-based authentication.

        ```python
        def authenticate(token):
            return validate_token(token)
        ```

        | Method | Endpoint | Description |
        |--------|----------|-------------|
        | GET    | /api/v1  | Root endpoint |
        | POST   | /api/v1  | Create resource |
```

## Summary of Special Characters and Markers

| Marker | Meaning |
|--------|---------|
| `...` | Text content separator (element \...\text) |
| `,,,` | Attribute separator |
| `:::` | Same-level element chain |
| `%` | Django template tag |
| `%%` | Django block (auto-closing pair) |
| `%tag:` | Auto-closing template tag |
| `>>>` / `<<<` | Raw text block delimiters |
| `{:}` | Indented CSS block |
| `===` | Python code block (wxPython) |
| `###>` | Markdown block |
| `^^^` | Passthrough mode (no conversion) |
| `@@(` | Output processor |
| `@@@` | File reference (first line only) |
| `_()` | Translation function |
| `[ \| ]` / `[[ \| ]]` | Table row / header row shorthand |
| `<inline:>` / `</inline:>` | Whitespace removal wrapper |
| `\\` | Line continuation |

## See Also

- [`indent_style.py`](../pytigon_lib/schindent/indent_style.py) — Main conversion engine
- [`indent_tools.py`](../pytigon_lib/schindent/indent_tools.py) — Utility functions and JS conversion
- [`indent_markdown.py`](../pytigon_lib/schindent/indent_markdown.py) — Markdown rendering within ihtml
- [`html2ihtml.py`](../pytigon_lib/schindent/html2ihtml.py) — Reverse converter (HTML → IHTML)
- [`django_ihtml.py`](../pytigon_lib/schdjangoext/django_ihtml.py) — Django integration and default configuration
- [`py_to_js.py`](../pytigon_lib/schindent/py_to_js.py) — Python to JavaScript compilation
