"""
Utility functions and helper classes for the Pytigon client-side framework.

Provides:
- Loading indicators (Ladda buttons and global spinner).
- AJAX communication (GET, POST, JSON, form submit, file upload).
- Dynamic JS/CSS loading with dependency tracking.
- DOM manipulation helpers (query, insert, remove, resize).
- URL manipulation (correct_href, join_urls, history push state).
- Template rendering and dialog positioning.
- File download and error handling.
"""

# =============================================================================
# Loaded file tracking (prevents duplicate JS/CSS loads)
# =============================================================================

LOADED_FILES = {}


# =============================================================================
# Loading indicator management
# =============================================================================


class Loading:
    """Manage loading indicators for AJAX operations.

    Supports two modes:
    - 'ladda': Ladda button animation on the triggering element.
    - 'global': A global loading-indicator element.

    Usage::

        loading = Loading(element)
        loading.create()
        loading.start()
        # ... async operation ...
        loading.stop()
        loading.remove()
    """

    def __init__(self, element):
        """Initialize the loading manager for a given element.

        Detects whether to use Ladda (if the element has .ladda-button)
        or the global loading indicator.

        Args:
            element: The DOM element that triggered the operation.
        """
        self.load_type = None
        if hasattr(element, "data") and getattr(element, "data"):
            self.element = getattr(element, "data")
        else:
            self.element = element
        if self.element:
            if self.element.classList.contains("ladda-button"):
                self.load_type = "ladda"
                self.ladda = None
        if not self.load_type:
            loading_indicator = document.getElementById("loading-indicator")
            if loading_indicator:
                self.load_type = "global"
                self.loading_indicator = loading_indicator

    def create(self):
        """Create the Ladda instance if in ladda mode."""
        if self.load_type == "ladda":
            self.ladda = window.Ladda.create(self.element)

    def start(self):
        """Start the loading animation."""
        if self.load_type == "ladda" and self.ladda:
            self.ladda.start()
        elif self.load_type == "global":
            self.loading_indicator.style.display = "block"

    def set_progress(self, progress):
        """Update the Ladda progress bar.

        Args:
            progress: Progress value between 0 and 1.
        """
        if self.load_type == "ladda" and self.ladda:
            self.ladda.setProgress(progress)

    def stop(self):
        """Stop the loading animation."""
        if self.load_type == "ladda" and self.ladda:
            self.ladda.stop()
        elif self.load_type == "global":
            self.loading_indicator.style.display = "none"

    def remove(self):
        """Remove the Ladda instance and clean up."""
        if self.load_type == "ladda" and self.ladda:
            self.ladda.remove()
            self.ladda = None


# =============================================================================
# File download
# =============================================================================


def save_as(blob, file_name):
    """Trigger a file download in the browser.

    Creates a temporary anchor element with a blob URL, clicks it,
    and cleans up after a short delay.

    Args:
        blob: Blob or File object to download.
        file_name: Suggested file name for the download.
    """
    url = window.URL.createObjectURL(blob)

    anchor_elem = document.createElement("a")
    anchor_elem.style = "display: none"
    anchor_elem.href = url
    anchor_elem.download = file_name

    document.body.appendChild(anchor_elem)
    anchor_elem.click()

    document.body.removeChild(anchor_elem)

    def _():
        window.URL.revokeObjectURL(url)

    setTimeout(_, 1000)


# =============================================================================
# Error handling
# =============================================================================


def standard_error_handler(req):
    """Display a standard error dialog for failed AJAX requests.

    For 500 errors: opens the response in a new window.
    For other errors: shows a SweetAlert2 error dialog.

    Args:
        req: The XMLHttpRequest object with .status and .response.
    """
    if req.status != 200:
        reader = FileReader()

        def _on_reader_load():
            nonlocal req, reader
            if req.status == 500:
                console.log(reader.result)
                window.open().document.write(reader.result)
            else:
                Swal.fire(
                    {
                        "icon": "error",
                        "title": "Error: %d" % req.status,
                        "text": reader.result,
                    }
                )

        reader.onload = _on_reader_load
        reader.readAsText(req.response)


window.standard_error_handler = standard_error_handler


def download_binary_file(buf, content_disposition):
    """Download a binary file from a server response.

    Parses the Content-Disposition header to extract the filename.

    Args:
        buf: Binary blob data.
        content_disposition: Content-Disposition header string.
    """
    file_name = "temp.dat"
    var_list = content_disposition.split(";")
    for pos in var_list:
        if "filename" in pos:
            file_name = pos.split("=")[1]
            break

    save_as(buf, file_name)


# =============================================================================
# Frontend view rendering
# =============================================================================


def frontend_view(url, complete, callback_on_error=None, param=None):
    """Render a frontend view (.fview) URL.

    Loads the corresponding .js module, invokes its request function
    with parameters, and optionally renders a Nunjucks template.

    Args:
        url: The .fview URL to process.
        complete: Callback receiving the rendered result.
        callback_on_error: Optional error callback.
        param: Optional parameters for the view.
    """
    url2 = window.process_href(url.replace(".fview", ".js"), None)

    param2 = param
    if param:
        param2 = window.getParamsFromEncodedParams(param)
    else:
        if "?" in url:
            param2 = window.getParamsFromUrl(url)

    def _callback(module):
        nonlocal url, complete, callback_on_error, param2

        def _callback2(context):
            if jQuery.type(context) == "object" and context["template"]:

                def _callback3(template_str):
                    nonlocal context
                    res = window.nunjucks.renderString(template_str, context)
                    complete(res)

                template = context["template"]
                if template == ".":
                    template = url.replace(".fview", ".html")
                ajax_get(template, _callback3)
            else:
                complete(context)

        if window.hasOwnProperty("cordova") or location.protocol == "file:":
            r = eval(module.replace("export", ""))
            r(param2, _callback2)
        else:
            module["request"](param2, _callback2)

    if window.hasOwnProperty("cordova") or location.protocol == "file:":
        ajax_get(url2, _callback, callback_on_error)
    else:
        x = window.dynamic_import(url2, _callback)


# =============================================================================
# AJAX GET
# =============================================================================


def ajax_get(url, complete, callback_on_error=None, process_req=None):
    """Perform an AJAX GET request.

    Handles .fview URLs via frontend_view, binary downloads, redirects,
    and standard text responses.

    Args:
        url: The URL to fetch.
        complete: Callback receiving the response text.
        callback_on_error: Optional error callback.
        process_req: Optional callback to configure the XHR before send.

    Returns:
        The XMLHttpRequest object.
    """
    if ".fview" in url:
        return frontend_view(url, complete, callback_on_error, None)

    req = XMLHttpRequest()

    if process_req:
        process_req(req)

    process_blob = False
    try:
        req.responseType = "blob"
        process_blob = True
    except:
        pass

    def _onload():
        nonlocal complete, callback_on_error, process_blob, req

        if req.status != 200:
            if callback_on_error:
                callback_on_error(req)
            else:
                standard_error_handler(req)
            return

        if not req.response:
            complete(req.responseText)
        elif process_blob:
            disp = req.getResponseHeader("Content-Disposition")
            if disp and "attachment" in disp:
                download_binary_file(req.response, disp)
                complete(None)
            else:
                reader = FileReader()

                def _on_reader_load():
                    nonlocal disp, req
                    if req.status != 200 and req.status != 0:
                        console.log(reader.result)
                        window.open().document.write(reader.result)
                        complete("Error - details on new page")
                    else:
                        if disp == "redirect":
                            url2data = reader.result.split("|")

                            def _complete2(data):
                                nonlocal url2data
                                element = complete(data)
                                if element:
                                    next_href = url2data[1]
                                    next_target = url2data[2]
                                    query = url2data[3]
                                    element = element.querySelector(query)

                                    def _callback_next(data):
                                        nonlocal element, next_target, next_href
                                        if next_target.startswith("inline"):
                                            t = next_target.replace("inline", "")
                                            if t == "_info":
                                                s = "INLINE_INFO"
                                            elif t == "_delete":
                                                s = "INLINE_DELETE"
                                            elif t == "_edit":
                                                s = "INLINE_EDIT"
                                            else:
                                                s = "INLINE"
                                            return window._on_inline(
                                                element,
                                                get_elem_from_string(data),
                                                next_href,
                                                {},
                                                None,
                                                s,
                                            )
                                        elif next_target.startswith("popup"):
                                            t = next_target.replace("popup", "")
                                            if t == "_info":
                                                s = "MODAL_INFO"
                                            elif t == "_delete":
                                                s = "MODAL_DELETE"
                                            elif t == "_edit":
                                                s = "MODAL_EDIT"
                                            else:
                                                s = "MODAL"
                                            return window._on_popup(
                                                element,
                                                get_elem_from_string(data),
                                                next_href,
                                                {},
                                                None,
                                                s,
                                            )
                                        else:
                                            return window.on_new_tab(
                                                element,
                                                get_elem_from_string(data),
                                                next_href,
                                                {},
                                                None,
                                            )

                                    ajax_get(next_href, _callback_next)

                                return element

                            return ajax_get(url2data[0], _complete2)

                        complete(reader.result)

                reader.onload = _on_reader_load
                reader.readAsText(req.response)
        else:
            if req.status != 200 and req.status != 0:
                console.log(req.response)
                window.open().document.write(req.response)
                complete("Error - details on new page")
            else:
                complete(req.response)

    req.onload = _onload

    req.open("GET", url, True)
    req.send(None)
    return req


window.ajax_get = ajax_get


# =============================================================================
# AJAX POST (internal helper and public API)
# =============================================================================


def _req_post(req, url, data, complete, callback_on_error=None, content_type=None):
    """Internal POST request handler.

    Handles .fview URLs, blob responses, and standard text responses.
    """
    if ".fview" in url:
        return frontend_view(url, complete, callback_on_error, data)

    process_blob = False
    try:
        req.responseType = "blob"
        process_blob = True
    except:
        pass

    def _onload(event):
        nonlocal req, process_blob, complete, callback_on_error, url

        if not req.status in (200, 500):
            if callback_on_error:
                callback_on_error(req)
            else:
                standard_error_handler(req)
            return

        if not req.response:
            complete(req.responseText)
        elif process_blob:
            disp = req.getResponseHeader("Content-Disposition")
            if disp and "attachment" in disp:
                download_binary_file(req.response, disp)
                complete(None)
            else:
                reader = FileReader()

                def _on_reader_load():
                    nonlocal req, reader
                    if req.status != 200 and req.status != 0:
                        console.log(reader.result)
                        window.open().document.write(reader.result)
                        complete("Error - details on new page")
                    complete(reader.result)

                reader.onload = _on_reader_load
                reader.readAsText(req.response)
        else:
            if req.status != 200 and req.status != 0:
                console.log(req.response)
                window.open().document.write(req.response)
                complete("Error - details on new page")
            complete(req.response)

    req.onload = _onload

    req.open("POST", url, True)

    # Set CSRF token and content type headers
    req.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"))
    if content_type:
        if content_type != "pass":
            req.setRequestHeader("Content-Type", content_type)
    else:
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")

    req.send(data)
    return req


def ajax_post(url, data, complete, callback_on_error, process_req=None, content_type=None):
    """Perform an AJAX POST request.

    Args:
        url: The URL to post to.
        data: Form data string or FormData object.
        complete: Callback receiving the response text.
        callback_on_error: Error callback.
        process_req: Optional callback to configure the XHR before send.
        content_type: Content-Type header value, or 'pass' to skip.

    Returns:
        The XMLHttpRequest object.
    """
    req = XMLHttpRequest()
    if process_req:
        process_req(req)

    _req_post(req, url, data, complete, callback_on_error, content_type)
    return req


window.ajax_post = ajax_post


# =============================================================================
# AJAX JSON
# =============================================================================


def ajax_json(url, data, complete, callback_on_error, process_req=None):
    """Perform an AJAX POST with JSON content type.

    Stringifies the data object and sends it as application/json.

    Args:
        url: The URL to post to.
        data: Data object to stringify and send.
        complete: Callback receiving the parsed JSON response.
        callback_on_error: Error callback.
        process_req: Optional XHR configuration callback.
    """

    def _complete(data_in):
        try:
            _data = JSON.parse(data_in)
        except:
            _data = data_in
        complete(_data)

    data2 = JSON.stringify(data)
    return ajax_post(url, data2, _complete, callback_on_error, None, "application/json")


window.ajax_json = ajax_json


# =============================================================================
# AJAX Form Submit (with file upload support)
# =============================================================================


def ajax_submit(
    _form,
    complete,
    callback_on_error=None,
    data_filter=None,
    process_req=None,
    url=None,
):
    """Submit a form via AJAX with automatic file upload detection.

    If the form contains file inputs, uses FormData with progress tracking.
    Otherwise, serializes the form data.

    Args:
        _form: The form DOM element.
        complete: Callback receiving the response.
        callback_on_error: Error callback.
        data_filter: Optional function to transform form data before send.
        process_req: Optional XHR configuration callback.
        url: Optional override URL (falls back to form action).
    """
    content_type = None
    req = XMLHttpRequest()
    form = jQuery(_form)

    if process_req:
        process_req(req)

    if form.find("[type='file']").length > 0:
        # File upload path
        _form.setAttribute("enctype", "multipart/form-data")
        data = FormData(_form)
        if data_filter:
            data = data_filter(data)

        content_type = "pass"

        # Show progress bar
        if not form.find("#progress").length == 1:
            form.find("div.inline-form-body").append(
                "<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>"
            )
        else:
            jQuery("#progress").width("0%")

        def _progressHandlingFunction(self, e):
            if e.lengthComputable:
                jQuery("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%")

        req.upload.addEventListener("progress", _progressHandlingFunction, False)

        for pair in data.entries():
            print(pair[0] + ": " + pair[1])

    else:
        # Standard form data path
        data = form.serialize()
        if data_filter:
            data = data_filter(data)

    if url:
        return _req_post(req, url, data, complete, callback_on_error, content_type)
    else:
        return _req_post(
            req,
            correct_href(form.attr("action"), (_form[0],)),
            data,
            complete,
            callback_on_error,
            content_type,
        )


window.ajax_submit = ajax_submit


# =============================================================================
# Dynamic CSS loading
# =============================================================================


def load_css(path, on_load=None):
    """Dynamically load a CSS file.

    Prevents duplicate loads by tracking loaded files. If no on_load
    callback is provided, injects a <style> tag into <head>.

    Args:
        path: URL of the CSS file.
        on_load: Optional callback receiving the XHR on load.
    """
    global LOADED_FILES
    if not (LOADED_FILES and path in LOADED_FILES):
        LOADED_FILES[path] = None
        req = XMLHttpRequest()

        def _onload():
            nonlocal req, on_load
            if on_load:
                on_load(req)
            else:
                jQuery('<style type="text/css"></style>').html(req.responseText).appendTo("head")

        req.onload = _onload

        req.open("GET", path, True)
        req.send("")


window.load_css = load_css


# =============================================================================
# Dynamic JavaScript loading
# =============================================================================


def on_load_js(path):
    """Execute callbacks registered for a loaded JS file.

    Args:
        path: URL of the JS file that was loaded.
    """
    global LOADED_FILES
    if LOADED_FILES and path in LOADED_FILES:
        functions = LOADED_FILES[path]
        if functions:
            for fun in functions:
                fun()
        LOADED_FILES[path] = None


def load_js(path, fun):
    """Dynamically load a JavaScript file and execute a callback.

    Supports deduplication: if already loading, queues the callback.
    If already loaded, executes immediately.

    Args:
        path: URL of the JS file to load.
        fun: Callback to execute after the script loads.
    """
    global LOADED_FILES
    if LOADED_FILES and path in LOADED_FILES:
        if LOADED_FILES[path]:
            LOADED_FILES[path].push(fun)
        else:
            fun()
    else:
        LOADED_FILES[path] = [fun]
        req = XMLHttpRequest()

        def _onload():
            # Save and restore requirejs/require/define to avoid conflicts
            _requirejs = window.requirejs
            _require = window.require
            _define = window.define
            window.requirejs = None
            window.require = None
            window.define = None
            script = document.createElement("script")

            # script.text = req.responseText
            # document.head.appendChild(script).parentNode.removeChild(script)

            blob = Blob([req.responseText], {"type": "application/javascript"})
            script.src = URL.createObjectURL(blob)

            def _onload2():
                URL.revokeObjectURL(script.src)
                # document.head.removeChild(script)
                window.requirejs = _requirejs
                window.require = _require
                window.define = _define
                on_load_js(path)

            script.onload = _onload2
            document.head.appendChild(script).parentNode.removeChild(script)

            # window.requirejs = _requirejs
            # window.require = _require
            # window.define = _define

            # on_load_js(path)

        req.onload = _onload

        req.open("GET", path, True)
        req.send("")


window.load_js = load_js


def load_many_js(paths, fun):
    """Load multiple JS files in order, executing a callback when all done.

    Supports the '|' separator to create loading groups: files before '|'
    are loaded before those after.

    Args:
        paths: List of JS file URLs. May contain '|' as a stage separator.
        fun: Callback executed after all files are loaded.
    """
    counter = 1
    next_step = None

    def _fun():
        nonlocal counter, next_step
        counter = counter - 1
        if counter == 0:
            if next_step != None:
                load_many_js(next_step, fun)
            else:
                fun()

    for path in paths:
        if path.length > 0:
            if next_step != None:
                next_step.append(path)
            else:
                if path == "|":
                    next_step = []
                else:
                    counter = counter + 1
                    load_js(path, _fun)
    _fun()


window.load_many_js = load_many_js


# =============================================================================
# Browser history
# =============================================================================


def history_push_state(title, url, data=None):
    """Push a state entry to the browser history.

    Converts the URL to a subpage query parameter format.

    Args:
        title: History entry title.
        url: URL for the history entry.
        data: Optional data tuple [html_content, element_id] for state restoration.
    """
    if not url or url == "/":
        url2 = url
    else:
        url2 = "?subpage=" + URL(url, "http://127.0.0.1").pathname
    if data:
        data2 = [LZString.compress(data[0]), data[1]]
    else:
        data2 = title
    window.history.pushState(data2, title, url2)


window.history_push_state = history_push_state


# =============================================================================
# DOM element creation from HTML strings
# =============================================================================


def get_elem_from_string(html, selectors=None):
    """Create a DOM element from an HTML string.

    Wraps the HTML in a temporary div.ajax-temp-item.

    Args:
        html: HTML string to parse.
        selectors: Optional CSS selector to extract a specific child.

    Returns:
        A DOM element or the temporary container if multiple children.
    """
    temp = document.createElement("div")
    temp.classList.add("ajax-temp-item")
    temp.innerHTML = html
    if selectors:
        element = temp.querySelector(selectors)
        return element
    else:
        if temp.childNodes.length == 1:
            return temp.childNodes[0]
        else:
            return temp


window.get_elem_from_string = get_elem_from_string


# =============================================================================
# Animation
# =============================================================================


def animate_combo(
    button,
    obj1,
    obj2,
    obj1_style_off,
    obj1_style_on,
    obj2_style_off,
    obj2_style_on,
    speed,
    end=None,
):
    """Toggle animation between two states for paired elements.

    When the button is clicked, toggles between 'on' and 'off' states,
    animating obj1 and obj2 with CSS transitions.

    Args:
        button: jQuery button element that toggles the state.
        obj1: First jQuery element to animate.
        obj2: Second jQuery element to animate.
        obj1_style_off: CSS properties for obj1 when button is OFF.
        obj1_style_on: CSS properties for obj1 when button is ON.
        obj2_style_off: CSS properties for obj2 when button is OFF.
        obj2_style_on: CSS properties for obj2 when button is ON.
        speed: Animation duration or None for instant.
        end: Optional callback after animation completes.
    """
    if end:
        end2 = end
    else:

        def end2():
            pass

    def _animate():
        if button.hasClass("on"):
            button.removeClass("on")

            if speed:
                obj1.animate(obj1_style_off, speed)
            else:
                obj1.css(obj1_style_off)

            obj1.removeClass("off")
            obj1.addClass("on")

            if speed:
                obj2.animate(obj2_style_off, speed, "linear", end2)
            else:
                obj2.css(obj2_style_off)
                end2()

            obj2.removeClass("on")
            obj2.addClass("off")
        else:
            button.addClass("on")

            if speed:
                obj1.animate(obj1_style_on, speed)
            else:
                obj1.css(obj1_style_on)

            obj1.removeClass("on")
            obj1.addClass("off")

            if speed:
                obj2.animate(obj2_style_on, speed, "linear", end2)
            else:
                obj2.css(obj2_style_on)
                end2()

            obj2.removeClass("off")
            obj2.addClass("on")

    button.click(_animate)


window.animate_combo = animate_combo


# =============================================================================
# Default icon mapping
# =============================================================================

window.icons = {
    "time": "fa fa-clock-o",
    "date": "fa fa-calendar",
    "up": "fa fa-chevron-up",
    "down": "fa fa-chevron-down",
    "previous": "fa fa-chevron-left",
    "next": "fa fa-chevron-right",
    "today": "fa fa-calendar-check-o",
    "clear": "fa fa-trash",
    "close": "fa fa-times",
    "paginationSwitchDown": "fa-chevron-down",
    "paginationSwitchUp": "fa-chevron-up",
    "refresh": "fa-refresh",
    "toggle": "fa-list-alt",
    "columns": "fa-th",
    "detailOpen": "fa-plus",
    "detailClose": "fa-minus",
}


# =============================================================================
# Visibility helpers
# =============================================================================


def is_hidden(el):
    """Check if an element is hidden via computed style.

    Args:
        el: DOM element.

    Returns:
        bool: True if display:none.
    """
    style = window.getComputedStyle(el)
    return style.display == "none"


window.is_hidden = is_hidden


def is_visible(el):
    """Check if an element is visible.

    Args:
        el: DOM element.

    Returns:
        bool: True if not hidden.
    """
    return not is_hidden(el)


window.is_visible = is_visible


# =============================================================================
# Template system
# =============================================================================
# Template keys map to pre-defined HTML templates from pytigon_js.resources

TEMPLATES = {
    "MODAL_EDIT": MODAL_EDIT,
    "MODAL_INFO": MODAL_INFO,
    "MODAL_DELETE": MODAL_DELETE,
    "MODAL_ERROR": MODAL_ERROR,
    "INLINE_EDIT": INLINE_EDIT,
    "INLINE_INFO": INLINE_INFO,
    "INLINE_DELETE": INLINE_DELETE,
    "INLINE_ERROR": INLINE_ERROR,
}


def get_template(template_name, param):
    """Get a rendered template string with parameter substitution.

    Replaces {title} and {href} placeholders in the template.

    Args:
        template_name: Key into the TEMPLATES dict.
        param: Dict with 'title' and optionally 'href' keys.

    Returns:
        str: The rendered template, or None if template not found.
    """
    global TEMPLATES
    if template_name in TEMPLATES:
        ret = TEMPLATES[template_name].replace("{title}", param["title"])
        if "href" in param:
            ret = ret.replace("{href}", param["href"])
        return ret
    return None


# =============================================================================
# DOM query helpers
# =============================================================================


def super_query_selector(element, selector):
    """Enhanced query selector with path-like syntax.

    Supports special path segments:
    - '..' : parent element
    - '.'  : current element (no-op)
    - '^selector' : closest ancestor matching selector
    - 'selector' : querySelector

    Multiple segments are separated by '/'.

    Args:
        element: Starting DOM element.
        selector: Path string (e.g. '../div.content/^.modal').

    Returns:
        The matched element or None.
    """
    x = selector.split("/")
    e = element
    for pos in x:
        if pos == "..":
            e = e.parentElement
        elif pos == ".":
            pass
        elif pos.startswith("^"):
            e = e.closest(pos[1:])
        else:
            e = e.querySelector(pos)
        if not e:
            return None
    return e


window.super_query_selector = super_query_selector


# =============================================================================
# DOM insertion helpers
# =============================================================================


def super_insert(base_element, insert_selector, inserted_element):
    """Insert an element relative to a target using a position selector.

    Selector format: 'path:position' where position is one of:
    - 'overwrite' / '>' : replace content
    - 'append_first' / '<<' : insert as first child
    - 'append' / '>>' : append as last child
    - 'after' / ')' : insert after target
    - 'before' / '(' : insert before target
    - 'class' : copy classes from inserted to target

    Args:
        base_element: Starting DOM element.
        insert_selector: Position selector string.
        inserted_element: Element to insert.

    Returns:
        The target element or None if not found.
    """
    if insert_selector and ":" in insert_selector:
        x = insert_selector.split(":")
        if x[0]:
            element = super_query_selector(base_element, x[0])
        else:
            element = base_element
        selector2 = x[1]
    else:
        if insert_selector:
            element = super_query_selector(base_element, insert_selector)
        else:
            element = base_element
        selector2 = None

    if not element:
        return None

    if selector2 in ("overwrite", ">"):
        element.innerHTML = ""
        element.appendChild(inserted_element)
    elif selector2 in ("append_first", "<<"):
        element.insertBefore(inserted_element, element.firstChild)
    elif selector2 in ("append", ">>"):
        element.appendChild(inserted_element)
    elif selector2 in ("after", ")"):
        element.parentElement.insertBefore(inserted_element, element.nextSibling)
    elif selector2 in ("before", "("):
        element.parentElement.insertBefore(inserted_element, element)
    elif selector2 == "class":
        for c in Array.prototype.slice.call(inserted_element.classList):
            element.classList.add(c)
    else:
        if hasattr(element, selector2):
            getattr(element, selector2)(inserted_element)
        else:
            element.appendChild(inserted_element)

    return element


window.super_insert = super_insert


# =============================================================================
# HTML-to-DOM with position markers
# =============================================================================

_OPERATOR = (">>", "<<", ">", "(", ")")


def send_to_dom(html_text, base_elem):
    """Parse HTML text and insert it into the DOM based on position markers.

    If the HTML contains ===operator followed by a selector, inserts
    the parsed content at the specified position relative to base_elem.

    Args:
        html_text: HTML string possibly containing ===operator markers.
        base_elem: Base element for relative insertion.

    Returns:
        The result of super_insert, or None if no operator found.
    """
    global _OPERATOR
    for operator in _OPERATOR:
        if "===" + operator in html_text:
            x = html_text.split("===" + operator)
            html = x[0]
            insert_selector = x[1] + ":" + operator
            inserted_element = get_elem_from_string(html, None)
            return super_insert(base_elem, insert_selector, inserted_element)
    return None


window.send_to_dom = send_to_dom


# =============================================================================
# Element removal
# =============================================================================


def remove_element(element):
    """Remove an element from the DOM with cleanup callbacks.

    Handles:
    - .call_on_remove callbacks before removal.
    - .plug elements with modal dialogs (hides modals first).
    - String selectors (removes all matches).

    Args:
        element: DOM element, or CSS selector string.
    """
    if element:

        def _on_remove(index, value):
            value.on_remove()

        if isinstance(element, str):
            elements = Array.prototype.slice.call(document.querySelectorAll(element))
        else:
            elements = [element]

        for element2 in elements:
            jQuery.each(jQuery(element2).find(".call_on_remove"), _on_remove)

            def _on_remove_aside(index, value):
                dialog = value.firstElementChild
                if dialog and dialog.hasAttribute("modal"):
                    if window.hasOwnProperty("bootstrap"):
                        d = bootstrap.Modal(dialog)
                        d.hide()
                    else:
                        jQuery(dialog).modal("hide")

            jQuery.each(jQuery(element2).find(".plug"), _on_remove_aside)

            element2.remove()


window.remove_element = remove_element


# =============================================================================
# Responsive resize handler
# =============================================================================


def process_resize(target_element):
    """Process resize events for flexible_size elements.

    Calculates viewport dimensions and element offsets, then triggers
    size adjustments on elements with .flexible_size or
    .flexible_size_round2 classes, either via their process_resize
    callback or by applying data-size attribute formatting.

    Args:
        target_element: Root element to scan for resizable children.
    """
    param = {}
    param["w"] = window.innerWidth
    param["h"] = window.innerHeight
    body_rect = document.body.getBoundingClientRect()
    elements1 = Array.prototype.slice.call(target_element.querySelectorAll(".flexible_size"))
    elements2 = Array.prototype.slice.call(target_element.querySelectorAll(".flexible_size_round2"))
    elements3 = []
    if target_element.classList.contains("flexible_size") or target_element.classList.contains(
        "flexible_size_round2"
    ):
        elements3.append(target_element)
    for elements in (elements1, elements2, elements3):
        for elem in elements:
            elem_rect = elem.getBoundingClientRect()
            if elem.parentElement:
                parent_rect = elem.getBoundingClientRect()
                param["parent_offset_x"] = elem_rect.top - parent_rect.top
                param["parent_offset_y"] = elem_rect.left - parent_rect.left
            else:
                param["parent_offset_y"] = 0
                param["parent_offset_x"] = 0
            param["body_offset_y"] = elem_rect.top - body_rect.top
            param["body_offset_x"] = elem_rect.left - body_rect.left

            if hasattr(elem, "process_resize"):
                elem.process_resize(param)
            else:
                size_desc = elem.hasAttribute("data-size")
                if size_desc:
                    size_style = size_desc.format(param)
                    elem.style.cssText = size_style
                else:
                    h = (param["h"] - param["body_offset_y"] - 5) + "px"
                    elem.style.height = h
                    elem.setAttribute("height", h)


window.process_resize = process_resize


# =============================================================================
# Table type detection
# =============================================================================


def get_page(elem):
    """Get the closest .tab-pane ancestor of an element.

    Args:
        elem: jQuery element.

    Returns:
        jQuery element matching .tab-pane.
    """
    if elem.hasClass(".tab-pane"):
        return elem
    else:
        return elem.closest(".tab-pane")


def get_table_type(elem):
    """Detect the table_type attribute from a .tabsort element.

    Searches within the element and its parent page.

    Args:
        elem: jQuery element.

    Returns:
        str: The table_type value, or empty string.
    """
    tabsort = elem.find(".tabsort")
    if tabsort.length == 0:
        tabsort = get_page(elem).find(".tabsort")
    if tabsort.length > 0:
        ret = tabsort.attr("table_type")
        if ret:
            return ret
    return ""


window.get_table_type = get_table_type


# =============================================================================
# Modal stacking prevention
# =============================================================================


def can_popup():
    """Check if a modal popup can be opened (no existing modal is open).

    Returns:
        bool: True if no .modal-open element exists.
    """
    if jQuery(".modal-open").length > 0:
        return False
    else:
        return True


# =============================================================================
# URL utilities
# =============================================================================


def correct_href(href, elements=None):
    """Add fragment parameters to a URL based on element context.

    Automatically appends:
    - 'fragment=table-content' for table region elements.
    - 'fragment=page-content' for other elements.
    - Custom get-param attributes from elements.

    Args:
        href: The URL to modify.
        elements: Tuple of DOM elements providing context.

    Returns:
        str: The modified URL.
    """
    if not href:
        return href

    if "fragment=" in href:
        return href

    only_table = False
    if elements != None:
        for element in elements:
            if (
                element != None
                and element.hasAttribute("data-region")
                and "table" in element.getAttribute("data-region").lower()
            ):
                only_table = True

    if only_table:
        if "?" in href:
            href += "&fragment=table-content"
        else:
            href += "?fragment=table-content"
    else:
        only_content = True
        if elements != None:
            for element in elements:
                if (
                    element != None
                    and element.hasAttribute("target")
                    and element.getAttribute("target").lower() in ("_top", "_blank")
                ):
                    only_content = False

        if only_content:
            if "?" in href:
                href += "&fragment=page-content"
            else:
                href += "?fragment=page-content"

    if elements != None:
        for element in elements:
            if element and element.hasAttribute("get-param") and element.getAttribute("get-param"):
                if not element.getAttribute("get-param") in href:
                    if "?" in href:
                        href += "&" + element.getAttribute("get-param")
                    else:
                        href += "?" + element.getAttribute("get-param")
    return href


def remove_page_from_href(href):
    """Remove 'page=' parameter from a URL.

    Args:
        href: URL string.

    Returns:
        str: URL without page parameters.
    """
    x = href.split("?")
    if len(x) > 1:
        x2 = x[1].split("&")
        if len(x2) > 1:
            x3 = []
            for pos in x2:
                if not "page=" in pos:
                    x3.append(pos)
            return x[0] + "?" + ("".join(x3))
        else:
            if "page=" in x2[0]:
                return x2
            else:
                return href
    return href


# =============================================================================
# Inline dialog maximize/minimize
# =============================================================================


def inline_maximize(elem):
    """Maximize an inline dialog (add .maximized class, toggle buttons)."""
    dialog = elem.closest("div.modal-content")
    if not dialog.classList.contains("maximized"):
        dialog.classList.add("maximized")

    b_min = dialog.querySelector("button.minimize")
    b_max = dialog.querySelector("button.maximize")
    b_min.style.display = "inline-block"
    b_max.style.display = "none"


window.inline_maximize = inline_maximize


def inline_minimize(elem):
    """Minimize an inline dialog (remove .maximized class, toggle buttons)."""
    dialog = elem.closest("div.modal-content")
    if dialog.classList.contains("maximized"):
        dialog.classList.remove("maximized")

    b_min = dialog.querySelector("button.minimize")
    b_max = dialog.querySelector("button.maximize")
    b_min.style.display = "none"
    b_max.style.display = "inline-block"


window.inline_minimize = inline_minimize


# =============================================================================
# Element URL accessors
# =============================================================================


def element_get_url(element):
    """Get the URL from an element's href, action, or src attribute.

    Args:
        element: DOM element.

    Returns:
        str: The first found URL attribute value, or None.
    """
    for attr in ("href", "action", "src"):
        if element.hasAttribute(attr):
            return element.getAttribute(attr)
    return None


window.element_get_url = element_get_url


def element_set_url(element, url):
    """Set the URL on an element's href, action, or src attribute.

    Only sets the first matching attribute.

    Args:
        element: DOM element.
        url: URL value to set.
    """
    for attr in ("href", "action", "src"):
        if element.hasAttribute(attr):
            element.setAttribute(attr, url)
            return


window.element_set_url = element_set_url


def join_urls(url1, url2):
    """Merge two URLs, combining their query parameters.

    url2's parameters override url1's for same keys.

    Args:
        url1: Base URL.
        url2: URL with parameters to merge.

    Returns:
        str: Combined URL.
    """
    d = {}
    if not "?" in url2:
        return url1
    if "?" in url1:
        url1base, x = url1.split("?", 1)
        for item in x.split("&"):
            y = item.split("=", 1)
            if len(y) > 1:
                d[y[0]] = y[1]
            else:
                d[y[0]] = ""
    else:
        url1base = url1
    z, xx = url2.split("?", 1)
    for item in xx.split("&"):
        y = item.split("=", 1)
        if len(y) > 1:
            d[y[0]] = y[1]
        else:
            d[y[0]] = ""
    url1base += "?"
    for key, value in d.items():
        url1base += key + "=" + value + "&"
    return url1base[:-1]


window.join_urls = join_urls


def add_param2url(url, param):
    """Append a query parameter to a URL.

    Args:
        url: Base URL.
        param: Parameter string (e.g. 'key=value').

    Returns:
        str: URL with appended parameter.
    """
    if "?" in url:
        return url + "&" + param
    else:
        return url + "?" + param


window.add_param2url = add_param2url
