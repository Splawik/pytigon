from pytigon_js.tools import (
    ajax_get,
    ajax_post,
    ajax_load,
    ajax_submit,
    load_css,
    load_js,
    load_many_js,
)


def component_fun(component, name):
    def decorator(funct):
        component[name] = funct
        return funct

    return decorator


window.component_fun = component_fun


def set_state(component, state):
    spec = ("!", "?", "*", "0", "+", "-", "%")
    if "state_actions" in component.options:
        state_actions = component.options["state_actions"]
    else:
        state_actions = []
    for key in Object.js_keys(state):
        value = state[key]
        if component.root != None:
            for c in (component.root, component):
                nodes = c.querySelectorAll('[data-bind*="' + key + '"]')
                for node in nodes:
                    xx = node.getAttribute("data-bind")
                    for x in xx.split(";"):
                        if not x.lower().endswith(key.lower()):
                            continue
                        mod_fun = None
                        if ":" in x:
                            x2 = x.split(":", 1)
                            element_selector = x2[0]
                            data_selector = x2[1]
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

                        if element_selector:
                            if element_selector.startswith("style-"):
                                node.style[element_selector[6:]] = value2
                            elif element_selector.startswith("attr-"):
                                old_value = node.getAttribute(element_selector[5:], "")
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
        if key in state_actions:
            if key in component.state:
                state_actions[key](component, component.state[key], value)
            else:
                state_actions[key](component, None, value)
        component.state[key] = value


class DefineWebComponent(object):
    def __init__(self, tag, shadow=False, js=None, css=None):
        self.tag = tag
        self.shadow = shadow
        self.options = {}
        self.js = js
        self.css = css

    def make_component(self):
        if self.js and "init" in self.options:
            init = self.options["init"]

            def _init(component):
                nonlocal self, init

                def _on_loadjs():
                    nonlocal self, init, component
                    init(component)

                load_many_js(self.js, _on_loadjs)

            self.options["init"] = _init

        if self.css:
            for css in self.css:
                if self.shadow:
                    if "template" in self.options:
                        self.options["template"] = (
                            '<style>@import "'
                            + css
                            + '"</style>\n'
                            + self.options["template"]
                        )
                    else:
                        self.options["template"] = (
                            '<style>@import "' + css + '"</style>\n'
                        )
                else:
                    load_css(css)

        if not "set_state" in self.options:
            self.options["set_state"] = set_state

        define_custom_element(self.tag, self.shadow, self.options)

    def fun(self, name):
        def decorator(funct):
            nonlocal self
            self.options[name] = funct
            return funct

        return decorator

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.make_component()


window.DefineWebComponent = DefineWebComponent


class GlobalBus:
    def __init__(self):
        self.components = []
        self.state = {}

    def set_state(self, state):
        if state:
            state2 = dict(state)
            for key, value in state2.items():
                if not (key in self.state and self.state[key] != value):
                    self.state[key] = value
                    self.emit(key, value)

    def emit(self, name, value):
        for component in self.components:
            if component:
                if hasattr(component, "set_external_state"):
                    component.set_external_state({name: value})

    def register(self, component):
        if not component in self.components:
            self.components.append(component)
            for key, value in self.state.items():
                self.emit(key, value)

    def unregister(self, component):
        if component in self.components:
            self.components.remove(component)