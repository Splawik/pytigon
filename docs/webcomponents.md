# Creating Web Components in Pytigon

## Introduction

Pytigon enables defining custom HTML elements (Web Components) using Python, which is then
compiled to JavaScript via the **pscript** library.

The core of the system is the `DefineWebComponent` class defined in
`pytigon/static_src/pytigon_js/component.py`. This class provides a declarative API for building
components with Shadow DOM support, lazy loading of JS/CSS dependencies, reactive state binding,
and cross-component communication.

---

## Architecture

The web component system consists of three layers:

| Layer | Location | Purpose |
|-------|----------|---------|
| Helper definitions (Python→JS) | `pytigon/static_src/pytigon_js/component.py` | `DefineWebComponent`, `set_state`, `GlobalBus` |
| Loader functions (Python→JS) | `pytigon/static_src/pytigon_js/tools.py` | `load_js`, `load_many_js`, `load_css`, `jsimp_many` |
| Core element definition (JS) | `frontend/not_node_modules/pytigon-tools.js` | `define_custom_element` (creates HTMLElement subclass) |

Flow: Python code → pscript compilation → JS files → browser registration via `customElements.define()`.

---

## Basic Syntax

Component definition uses a context manager (`with`):

```python
with DefineWebComponent("tag-name", shadow, js_libs, css_libs, js_modules) as comp:
    # component definition
```

### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tag` | `str` | Custom HTML element tag name (e.g. `"ptig-calendar"`) |
| `shadow` | `bool` | Enable Shadow DOM (default `False`) |
| `js` | `list[str]` | List of JS file URLs to load before init |
| `css` | `list[str]` | List of CSS file URLs to load |
| `js_modules` | `bool` | If `True`, loads JS via `import()` instead of `load_js()` (for ES modules) |

---

## Component Options

Inside the `with` block, options are set via `comp.options["key"]`:

### `template`
HTML template injected into the component (Shadow DOM or light DOM).

```python
comp.options['template'] = '<div name="container"><slot></slot></div>'
```

Template syntax uses triple commas (`,,,`) as attribute separators:

```
div class=my-class,,,data-bind=style-width:width;style-height:height
    slot
```

The above generates: `<div class="my-class" data-bind="style-width:width;style-height:height"><slot></slot></div>`.

### `attributes`
Map of observed HTML attributes. Keys are attribute names, values are callbacks called on change
— signature: `function(component, old_value, new_value)`.

```python
def width(component, old_value, new_value):
    component.style.width = new_value

def height(component, old_value, new_value):
    component.style.height = new_value

comp.options['attributes'] = {
    "width": width,
    "height": height,
}
```

### `init`
Initialization function called after dependencies are loaded and template is injected.

```python
def init(component):
    div = component.root.querySelector('div')
    # ... initialization code
comp.options["init"] = init
```

### `constructor`
Function called before `init`, before the template is injected into Shadow DOM.
Used for preliminary state setup.

```python
def constructor(component):
    component.markers = []
    def process_slot(slot):
        component.markers.append((
            slot.getAttribute('x'),
            slot.getAttribute('y'),
            slot.getAttribute('txt')
        ))
    component['process_slot'] = process_slot
comp.options["constructor"] = constructor
```

### `disconnectedCallback`
Called when the element is removed from DOM. Used to clean up resources (timers, websockets).

```python
def disconnectedCallback(component):
    if component.timer:
        clearTimeout(component.timer)
        component.timer = None
    if component.websocket:
        component.websocket.close()
        component.websocket = None
comp.options["disconnectedCallback"] = disconnectedCallback
```

### `event_handler`
Object with event handlers from `GlobalBus`. Keys are event names.

```python
def on_save(component, data, src, callback):
    ajax_post(component.getAttribute('href'), data, callback)
    return None

comp.options['event_handler'] = {"on_save": on_save}
```

### `state_actions`
Map of functions called when specific state keys change. Signature:
`function(component, old_value, new_value)`.

### `global_state_actions`
Like `state_actions`, but for external state broadcast by `GlobalBus`.

---

## State Binding System (`set_state`)

The `data-bind` mechanism enables declarative binding of DOM elements to component state.

### `data-bind` Attribute Syntax

```
data-bind="[selector:]modifier[key];..."
```

Multiple bindings are separated by semicolons (`;`).

### Element Selector (part before `:`)

| Selector | Effect |
|----------|--------|
| (none) | Sets `innerHTML` |
| `style-*` | Sets `node.style.*` (e.g. `style-width` → `node.style.width`) |
| `attr-*` | Sets HTML attribute (e.g. `attr-src` → `node.setAttribute('src', val)`) |
| `class-*` | Toggles CSS class based on boolean value |
| other name | Sets `node[name]` (e.g. `onclick`, `href`) |

### Value Modifiers

| Char | Action |
|------|--------|
| (none) | Passes value unchanged |
| `!` | Boolean negation (`not value`) |
| `?` | Cast to bool |
| `*` | Cast to string |
| `+` | Cast to float (positive) |
| `-` | Cast to float (negated) |
| `%` | Cast to float (divided by 100) |

### Examples

```html
<!-- Set div width from state key "width" -->
<div data-bind="style-width:width"></div>

<!-- Set image src -->
<img data-bind="attr-src:src;attr-type:type" />

<!-- Display time in a span element -->
<span data-bind="time"></span>

<!-- Toggle CSS class -->
<div data-bind="class-active:is_active"></div>

<!-- Compound bindings -->
<div data-bind="style-width:width;style-height:height"></div>
```

### Calling `set_state`

In component code:

```python
state = {
    "width": "100%",
    "height": "400px",
    "title": "Hello, world!",
}
component.set_state(state)
```

---

## Loading Dependencies

### JavaScript

JS file URLs passed as the third parameter to `DefineWebComponent`:

```python
js_tab = [BASE_PATH + '/fullcalendar/main.min.js', '|', BASE_PATH + '/fullcalendar/locales-all.min.js']
with DefineWebComponent(TAG, False, js_tab, css_tab) as comp:
    ...
```

The `'|'` character acts as a stage separator — files before `'|'` load first, then files
after `'|'`. The mechanism guarantees load order.

### ES Modules (js_modules=True)

When `js_modules=True`, JS files are loaded as ES modules via `import()`. Loaded modules
are available in `component.modules` — a list in load order:

```python
with DefineWebComponent(TAG, True, [BASE_PATH + '/leaflet.js'], [BASE_PATH + '/leaflet.css'], True) as comp:
    def init(component):
        leaflet = component.modules[0]   # Imported module
        L = leaflet.L
        # ...
```

### CSS

CSS file URLs passed as the fourth parameter:

```python
css_libs = [BASE_PATH + '/fullcalendar/main.min.css']
```

For Shadow DOM, CSS is injected via `@import` in `<style>`. For light DOM — via dynamic `<link>` creation.

---

## Shadow DOM vs Light DOM

| Feature | Shadow DOM (`shadow=True`) | Light DOM (`shadow=False`) |
|---------|----------------------------|----------------------------|
| Style isolation | Yes | No |
| Element access | `component.root` = shadowRoot | `component.root` = element |
| `<slot>` | Works natively | Not supported |
| CSS dependencies | `@import` in `<style>` | `<style>` in `<head>` |
| Use when | Encapsulated widget | Integration with page CSS |

---

## Cross-Component Communication (`GlobalBus`)

`GlobalBus` is a global event bus available as `window.GLOBAL_BUS`.

### Registering a Component

Components with `global_state_actions` are automatically registered. Manual registration is also possible:

```python
window.GLOBAL_BUS.register(component)
```

### Broadcasting State

```python
GLOBAL_BUS.set_state({"theme": "dark", "lang": "en"})
```

The receiver must have `global_state_actions` defined for matching keys.

### Sending Events

```python
GLOBAL_BUS.send_event("refresh_table", None, component, None)
```

The receiver defines `event_handler` with a matching event name.

### Sending via `data-bind` (via ptig-form)

The `ptig-form` component enables sending events to `GLOBAL_BUS` through server response:

```python
# In JSON response from the server:
{
    "send_event": {
        "refresh": {"table_id": 5}
    },
    "set_state": {
        "current_record": 42
    }
}
```

---

## Component Lifecycle

```
constructor(component)       # State preparation, before template
    ↓
Shadow DOM creation (if shadow=True)
Template injection
    ↓
JS/CSS dependency loading
    ↓
init(component)              # Initialization — dependencies and DOM ready
    ↓
attributes_init()            # Initial attribute handling
    ↓
connectedCallback()          # Element in DOM
    ↓
disconnectedCallback()       # Removal from DOM — cleanup
```

---

## Storing Components in the Database

Components are stored in the project file `_schcomponents.ptigprj` as `SChStatic` objects with
type `"R"` (pscript, compiled Python→JS). Fields:

```json
{
    "model": "SChStatic",
    "attributes": {
        "type": "R",
        "name": "ptig-my-component",
        "content": "TAG = 'ptig-my-component'\n\nwith DefineWebComponent(TAG, ...) as comp:\n    ..."
    }
}
```

After compilation, the resulting JavaScript goes to:
`pytigon/prj/_schcomponents/static/_schcomponents/components/`.

---

## Example: Simple SVG Component

```python
TAG = 'ptig-svg'

TEMPLATE = """
div name=svgdiv,,,data-bind=style-width:width;style-height:height
    slot
"""

with DefineWebComponent(TAG, True) as comp:
    comp.options["attributes"] = {"width": None, "height": None}
    comp.options['template'] = TEMPLATE

    def init(component):
        div = component.root.querySelector('div')
        state = {}

        state["onclick"] = window.handle_click

        def _onmouseover(event):
            console.log("onmouseover")
        state["onmouseover"] = _onmouseover

        def _onmouseout(event):
            console.log("onmouseout")
        state["onmouseout"] = _onmouseout

        def _onmousedown(event):
            console.log("onmousedown")
        state["onmousedown"] = _onmousedown

        def _onmouseup(event):
            console.log("onmouseup")
        state["onmouseup"] = _onmouseup

        component.set_state(state)
    comp.options["init"] = init
```

## Example: Timer Component (Clock)

```python
TAG = 'ptig-time'

TEMPLATE = """
    slot
"""

with DefineWebComponent(TAG, True) as comp:
    comp.options['template'] = TEMPLATE

    def init(component):
        def _on_time():
            nonlocal component
            d = Date()
            t = d.toISOString().replace('T', ' ')
            component.set_state({
                "time": t[11:19],
                "date": t[:10],
                "datetime": t[:19],
                "time_short": t[11:16],
                "datetimeshort": t[:16],
            })
        component.timer = setInterval(_on_time, 250)
        _on_time()
    comp.options["init"] = init

    def disconnectedCallback(component):
        if component.timer:
            clearTimeout(component.timer)
            component.timer = None
    comp.options["disconnectedCallback"] = disconnectedCallback
```

Usage in HTML:

```html
<ptig-time>
    <span data-bind="time"></span>
    <span data-bind="date"></span>
</ptig-time>
```

## Example: Component with External Dependencies (Leaflet)

```python
TAG = "ptig-leaflet"

TEMPLATE = """
    div class=leafletframe,,,data-bind=style-width:width;style-height:height
        div class=leafletdiv,,,style=width:100%;height:100%
    slot
"""

BASE_PATH = window.BASE_PATH + 'static/_schcomponents/leaflet'

with DefineWebComponent(TAG, True,
    [BASE_PATH + '/leaflet.js'],
    [BASE_PATH + '/leaflet.css'],
    True        # js_modules=True — use import()
) as comp:

    comp.options['attributes'] = {"width": None, "height": None}
    comp.options['template'] = TEMPLATE

    def constructor(component):
        component.markers = []
        def process_slot(slot):
            component.markers.append((
                slot.getAttribute('x'),
                slot.getAttribute('y'),
                slot.getAttribute('txt'),
                slot.getAttribute('href'),
                slot.getAttribute('target')
            ))
        component['process_slot'] = process_slot
    comp.options["constructor"] = constructor

    def init(component):
        leaflet = component.modules[0]    # Imported JS module
        div = component.root.querySelector('div.leafletdiv')

        # HTML attribute handling
        x = float(component.getAttribute('x')) if component.hasAttribute('x') else 0
        y = float(component.getAttribute('y')) if component.hasAttribute('y') else 0
        z = float(component.getAttribute('z')) if component.hasAttribute('z') else 13

        if component.getAttribute('height'):
            component.set_state({'height': component.getAttribute('height')})

        def create():
            mapobj = leaflet.L.map(div).setView([x, y], z)
            leaflet.L.tileLayer(
                'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
                {'attribution': '&copy; OpenStreetMap contributors'}
            ).addTo(mapobj)

            for pos in component.markers:
                marker = leaflet.L.marker([pos[0], pos[1]])
                marker.addTo(mapobj)
                marker.bindPopup(pos[2])
                marker.openPopup()
                if pos[3]:
                    marker.on('click', window.create_event_handler(pos[3], pos[4]))

            component.mapobj = mapobj
            window.dispatchEvent(Event("resize"))

        setTimeout(create, 1000)
    comp.options["init"] = init
```

Usage in HTML:

```html
<ptig-leaflet x="52.2297" y="21.0122" z="13" height="500px" width="100%">
    <ptig-marker x="52.2297" y="21.0122" txt="Warsaw" href="/city/1"></ptig-marker>
</ptig-leaflet>
```

## Example: Form Component with AJAX

```python
TAG = 'ptig-form'

with DefineWebComponent(TAG, False) as comp:

    def init(component):
        def _onchange(self, new_value):
            nonlocal component

            def on_complete(data):
                def on_data(key):
                    if '__' in key:
                        x = key.split('__')
                        obj = component.root.querySelector(x[0])
                        if x[1] == 'value':
                            obj.value = data[key]
                        else:
                            obj[x[1]](data[key])
                    elif key == "refresh_ajax_frame":
                        refresh_ajax_frame(component, data[key])
                    elif key == "set_state":
                        GLOBAL_BUS.set_state(data[key])
                    elif key == "send_event":
                        for key2, value2 in data[key].items():
                            GLOBAL_BUS.send_event(key2, value2)
                    else:
                        obj = component.root.querySelector(key)
                        obj.innerHTML = data[key]

                Object.keys(data).forEach(on_data)

            # Collect all field values
            if self.hasAttribute("multiple"):
                value = get_select_values(self)
            else:
                value = self.value

            data = {'name': self.getAttribute('name'), 'new_value': value}
            for key in component.fields:
                if component.fields[key].hasAttribute("multiple"):
                    data[key] = get_select_values(component.fields[key])
                else:
                    data[key] = component.fields[key].value

            ajax_json(component.getAttribute('src'), data, on_complete)

        # Register change handler on all inputs
        component.fields = {}
        for selector in ["input", "select", "textarea"]:
            for inp in component.root.querySelectorAll(selector):
                inp.addEventListener("change", _onchange)
                name = inp.getAttribute("name")
                component.fields[name] = inp

    comp.options["init"] = init
```

## Example: Component with GlobalBus Event Handling

```python
TAG = 'ptig-save-handler'

with DefineWebComponent(TAG, False) as comp:
    comp.options['attributes'] = {"namespace": None, "href": None}

    def init(component):
        return None

    def on_save(component, data, src, callback):
        if src.getAttribute("namespace") == component.getAttribute("namespace"):
            def _complete():
                callback()
            ajax_post(component.getAttribute('href'), data, _complete)
        return None

    comp.options["init"] = init
    comp.options["event_handler"] = {"on_save": on_save}
```

Usage in HTML:

```html
<ptig-save-handler namespace="documents" href="/api/save/"></ptig-save-handler>
<ptig-action-btn label="Save" event-name="on_save" namespace="documents"></ptig-action-btn>
```

---

## Best Practices

1. **Tag naming**: use the `ptig-` prefix for application components, `sys-` for system components.

2. **Cleanup**: always implement `disconnectedCallback` when creating timers, websockets, or
   listening for global events.

3. **Shadow DOM**: use `shadow=True` when the component has its own CSS isolated from the rest
   of the page. Use `shadow=False` when the component must inherit styles from the page.

4. **Attributes vs state**: HTML attributes (`component.getAttribute(...)`) are for initial
   configuration passed from Django templates. State (`component.set_state(...)`) is for dynamic
   changes during the component's lifetime.

5. **JS dependencies**: for classic libraries (via `window.*`) use `load_many_js`. For ES modules
   use `js_modules=True`.

6. **`BASE_PATH`**: always use `window.BASE_PATH` as a prefix for static resource paths.

7. **Multiple components in one file**: possible — just use another
   `with DefineWebComponent(...) as comp:` block in the same file.

---

## API Summary

### DefineWebComponent

```python
class DefineWebComponent:
    def __init__(self, tag, shadow=False, js=None, css=None, js_modules=False): ...
    def fun(self, name): ...          # Decorator to register callbacks
    def __enter__(self): ...          # Returns self
    def __exit__(self, ...): ...      # Calls make_component()
    def make_component(self): ...     # Registers customElements.define()
```

### Available `comp.options` Fields

| Field | Type | Description |
|-------|------|-------------|
| `template` | `str` | HTML template |
| `attributes` | `dict` | Attribute→function map |
| `init` | `function(component)` | Initialization |
| `constructor` | `function(component)` | Constructor |
| `disconnectedCallback` | `function(component)` | Cleanup |
| `connectedCallback` | `function(component)` | After adding to DOM |
| `attributeChangedCallback` | `function(name, old, new)` | Attribute change |
| `event_handler` | `dict` | GlobalBus event handlers |
| `state_actions` | `dict` | Actions on state change |
| `global_state_actions` | `dict` | Actions on global state change |
| `set_state` | `function(state)` | State binding function (defaults to `window.set_state`) |

### Available `component` Fields

| Field | Description |
|-------|-------------|
| `root` | Shadow root (shadow=True) or the element itself (shadow=False) |
| `state` | Object holding current state |
| `options` | Component options |
| `modules` | Loaded ES modules (when `js_modules=True`) |
