"""
Web Component definition and state management module.

Provides:
- set_state: data-binding engine for reactive state updates in components.
- DefineWebComponent: declarative custom element builder with shadow DOM,
  JS/CSS loading, and lifecycle management.
- GlobalBus: pub/sub event bus for cross-component communication.
"""


# =============================================================================
# State binding engine
# =============================================================================


def set_state(component, state):
    """Apply reactive state updates to a component's DOM bindings.

    Processes `data-bind` attributes on elements within the component,
    applying state values using optional modifiers:

    Modifier prefixes (applied to the data_selector portion):
        !  - boolean NOT
        ?  - boolean cast (truthy → True, falsy → False)
        *  - string cast
        +  - float cast (positive)
        -  - float cast (negated)
        %  - float cast (divided by 100)

    Element selector prefixes:
        style-  - set CSS style property
        attr-   - set HTML attribute
        class-  - toggle CSS class based on value truthiness
        (none)  - set innerHTML

    Args:
        component: The component instance (must have .root, .options, .state).
        state: Dict of key-value pairs to apply.
    """
    # Valid modifier characters
    spec = ("!", "?", "*", "0", "+", "-", "%")

    if component.options.hasOwnProperty("state_actions"):
        state_actions = component.options["state_actions"]
    else:
        state_actions = []

    for key in Object.keys(state):
        value = state[key]
        if component.root != None:
            # Search both component.root and component for matching bindings
            for c in (component.root, component):
                nodes = Array.prototype.slice.call(c.querySelectorAll('[data-bind*="' + key + '"]'))
                for node in nodes:
                    xx = node.getAttribute("data-bind")
                    # Each data-bind can contain multiple ;-separated bindings
                    for x in xx.split(";"):
                        if not x.lower().endswith(key.lower()):
                            continue

                        mod_fun = None
                        if ":" in x:
                            x2 = x.split(":", 1)
                            element_selector = x2[0]
                            data_selector = x2[1]
                            # Check for modifier prefix
                            if data_selector[0] in spec:
                                mod_fun = data_selector[0]
                                data_selector = data_selector[1:]
                            if not element_selector:
                                element_selector = data_selector
                        else:
                            element_selector = ""
                            data_selector = x
                            if data_selector[0] in spec:
                                mod_fun = data_selector[0]
                                data_selector = data_selector[1:]

                        value2 = value
                        if mod_fun:
                            if mod_fun == "!":
                                value2 = not value
                            elif mod_fun == "?":
                                if value:
                                    value2 = True
                                else:
                                    value2 = False
                            elif mod_fun == "*":
                                value2 = str(value)
                            elif mod_fun == "+":
                                value2 = float(value)
                            elif mod_fun == "-":
                                value2 = -1 * float(value)
                            elif mod_fun == "%":
                                value2 = float(value) / 100

                        # Apply the value to the target element property
                        if element_selector:
                            if element_selector.startswith("style-"):
                                node.style[element_selector[6:]] = value2
                            elif element_selector.startswith("attr-"):
                                node.setAttribute(element_selector[5:], value2)
                            elif element_selector.startswith("class-"):
                                cls = element_selector[6:]
                                if value2:
                                    node.classList.add(cls)
                                else:
                                    node.classList.remove(cls)
                            else:
                                node[element_selector] = value2
                        else:
                            node.innerHTML = value2

        # Invoke registered state action callbacks
        if key in state_actions:
            if key in component.state:
                state_actions[key](component, component.state[key], value)
            else:
                state_actions[key](component, None, value)

        component.state[key] = value


# =============================================================================
# Web Component definition
# =============================================================================


class DefineWebComponent:
    """Declarative builder for custom HTML elements (Web Components).

    Supports:
    - Shadow DOM rendering with CSS imports.
    - Lazy loading of JavaScript dependencies.
    - Automatic state binding via set_state.
    - Decorator-style option registration via the `fun()` method.
    - Context manager protocol for clean definition syntax.

    Usage::

        with DefineWebComponent("my-element", shadow=True, js=[...], css=[...]) as comp:
            @comp.fun("init")
            def init(component):
                # initialization code
                pass

    Attributes:
        tag: Custom element tag name.
        shadow: Whether to use Shadow DOM.
        options: Dict of component lifecycle callbacks and settings.
        js: List of JS file URLs to load before init.
        css: List of CSS file URLs to load.
    """

    def __init__(self, tag, shadow=False, js=None, css=None, js_modules=False):
        """Initialize the component definition.

        Args:
            tag: Custom element tag name (e.g. 'my-component').
            shadow: Enable Shadow DOM (default False).
            js: List of JavaScript file URLs to load.
            css: List of CSS file URLs to load.
        """
        self.tag = tag
        self.shadow = shadow
        self.options = {}
        self.js = js
        self.css = css
        self.js_modules = js_modules
        self.modules = None

    def make_component(self):
        """Build and register the custom element with the browser.

        Wraps the init callback to load JS dependencies first, injects
        CSS into the template (for shadow DOM) or loads via link (light DOM),
        and registers the custom element via define_custom_element.
        """
        # Wrap init to load JS dependencies first
        if self.js and self.options.hasOwnProperty("init"):
            init = self.options["init"]

            _component = self

            def _init(component):
                nonlocal _component, init

                def _on_loadjs(modules=None):
                    nonlocal component, _component, init
                    component.modules = modules
                    init(component)

                if self.js:
                    if self.js_modules:
                        jsimp_many(_component.js, _on_loadjs)
                    else:
                        load_many_js(_component.js, _on_loadjs)
                else:
                    _on_loadjs()

            self.options["init"] = _init

        # Inject CSS: @import in shadow DOM, load_css for light DOM
        if self.css:
            for css in self.css:
                if self.shadow:
                    if self.options.hasOwnProperty("template"):
                        self.options["template"] = (
                            '<style>@import "' + css + '"</style>\n' + self.options["template"]
                        )
                    else:
                        self.options["template"] = '<style>@import "' + css + '"</style>\n'
                else:
                    load_css(css)

        # Automatically attach set_state if not provided
        if not self.options.hasOwnProperty("set_state"):
            self.options["set_state"] = set_state

        define_custom_element(self.tag, self.shadow, self.options)

    def fun(self, name):
        """Decorator to register a lifecycle callback.

        Usage::

            @comp.fun("init")
            def my_init(component):
                pass

        Args:
            name: The option key to set (e.g. 'init', 'set_state').

        Returns:
            A decorator function that registers the decorated function.
        """

        def decorator(funct):
            nonlocal self
            self.options[name] = funct
            return funct

        return decorator

    def __enter__(self):
        """Context manager entry - returns self for decorator usage."""
        return self

    def __exit__(self, type, value, traceback):
        """Context manager exit - triggers component registration."""
        self.make_component()


window.DefineWebComponent = DefineWebComponent


# =============================================================================
# Global event bus for cross-component communication
# =============================================================================


class GlobalBus:
    """Simple pub/sub event bus for communication between web components.

    Components register themselves with the bus and receive state updates
    via set_external_state. The bus can also emit named events to all
    registered components via handle_event.

    Usage::

        bus = GlobalBus()
        bus.register(my_component)
        bus.set_state({"theme": "dark"})
        bus.send_event("refresh", None)
    """

    def __init__(self):
        """Initialize an empty component registry and state dict."""
        self.components = []
        self.state = {}

    def set_state(self, state):
        """Broadcast state changes to all registered components.

        Only emits values that have actually changed from the last known state.

        Args:
            state: Dict of key-value pairs to broadcast.
        """
        if state:
            state2 = dict(state)
            for key, value in state2.items():
                if not (key in self.state and self.state[key] != value):
                    self.state[key] = value
                    self.emit(key, value)

    def send_event(self, name, value):
        """Send a named event to all registered components.

        Components that implement handle_event(name, value) will receive it.

        Args:
            name: Event name.
            value: Event payload.
        """
        for component in self.components:
            if component:
                if hasattr(component, "handle_event"):
                    component.handle_event(name, value)

    def emit(self, name, value):
        """Emit a state change to all registered components.

        Components that implement set_external_state({name: value}) will
        receive the update.

        Args:
            name: State key name.
            value: New state value.
        """
        for component in self.components:
            if component:
                if hasattr(component, "set_external_state"):
                    component.set_external_state({name: value})

    def register(self, component):
        """Register a component to receive state updates.

        Upon registration, the component immediately receives all current
        state values.

        Args:
            component: Component instance to register.
        """
        if not component in self.components:
            self.components.append(component)
            if hasattr(component, "set_external_state"):
                for key, value in self.state.items():
                    component.set_external_state({key: value})

    def unregister(self, component):
        """Remove a component from the bus.

        Args:
            component: Component instance to unregister.
        """
        if component in self.components:
            self.components.remove(component)


window.GlobalBus = GlobalBus
