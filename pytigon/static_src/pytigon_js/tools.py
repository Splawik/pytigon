# import pytigon_js.resources as rc

LOADED_FILES = {}


class Loading:
    def __init__(self, element):
        self.load_type = None
        self.element = element
        if element:
            if element.classList.contains("ladda-button"):
                self.load_type = "ladda"
                self.ladda = None
        if not self.load_type:
            loading_indicator = document.getElementById("loading-indicator")
            if loading_indicator:
                self.load_type = "global"
                self.loading_indicator = loading_indicator

    def create(self):
        if self.load_type == "ladda":
            self.ladda = window.Ladda.create(self.element)

    def start(self):
        if self.load_type == "ladda" and self.ladda:
            self.ladda.start()
        elif self.load_type == "global":
            self.loading_indicator.style.display = "block"

    def set_progress(self, progress):
        if self.load_type == "ladda" and self.ladda:
            self.ladda.setProgress(progress)

    def stop(self):
        if self.load_type == "ladda" and self.ladda:
            self.ladda.stop()
        elif self.load_type == "global":
            self.loading_indicator.style.display = "none"

    def remove(self):
        if self.load_type == "ladda" and self.ladda:
            self.ladda.remove()
            self.ladda = None


def save_as(blob, file_name):
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


def download_binary_file(buf, content_disposition):
    # mimetype = 'text/html'
    # if 'odf' in content_disposition or 'ods' in content_disposition:
    #    mimetype = 'application/vnd.oasis.opendocument.formula'
    # elif 'pdf' in content_disposition:
    #    mimetype = 'application/pdf'
    # elif 'zip' in content_disposition:
    #    mimetype = 'application/x-compressed'
    # elif 'xls' in content_disposition:
    #    mimetype = 'application/excel'

    file_name = "temp.dat"
    var_list = content_disposition.split(";")
    for pos in var_list:
        if "filename" in pos:
            file_name = pos.split("=")[1]
            break

    save_as(buf, file_name)


def frontend_view(url, complete, param=None):
    url2 = url.replace(".fview", ".js")

    param2 = param
    if param:
        param2 = window.getParamsFromEncodedParams(param)
    else:
        if "?" in url:
            param2 = window.getParamsFromUrl(url)

    def _callback(module):
        nonlocal url, complete, param2

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
        ajax_get(url2, _callback)
    else:
        x = window.dynamic_import(url2, _callback)


def ajax_get(url, complete, process_req=None):
    if ".fview" in url:
        return frontend_view(url, complete, None)

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
        nonlocal process_blob
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
                    if req.status != 200 and req.status != 0:
                        console.log(reader.result)
                        window.open().document.write(reader.result)
                        complete("Error - details on new page")
                    else:
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
    # req.overrideMimeType('text/plain; charset=x-user-defined')
    req.send(None)


window.ajax_get = ajax_get


def _req_post(req, url, data, complete, content_type=None):
    if ".fview" in url:
        return frontend_view(url, complete, data)

    process_blob = False
    try:
        req.responseType = "blob"
        process_blob = True
    except:
        pass

    def _onload(event):
        nonlocal req, process_blob, complete, url
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

    req.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"))
    if content_type:
        if content_type != "pass":
            req.setRequestHeader("Content-Type", content_type)
    else:
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    # if data.length:
    #    req.setRequestHeader("Content-length", data.length)
    # req.setRequestHeader("Connection", "close")

    req.send(data)


def ajax_post(url, data, complete, process_req=None, content_type=None):
    req = XMLHttpRequest()
    if process_req:
        process_req(req)

    _req_post(req, url, data, complete, content_type)


window.ajax_post = ajax_post


def ajax_json(url, data, complete, process_req=None):
    def _complete(data_in):
        try:
            _data = JSON.parse(data_in)
        except:
            _data = data_in
        complete(_data)

    data2 = JSON.stringify(data)
    ajax_post(url, data2, _complete, None, "application/json")


window.ajax_json = ajax_json


def ajax_submit(_form, complete, data_filter=None, process_req=None, url=None):
    content_type = None
    req = XMLHttpRequest()
    form = jQuery(_form)

    if process_req:
        process_req(req)

    if form.find("[type='file']").length > 0:
        _form.setAttribute("enctype", "multipart/form-data")
        data = FormData(_form)
        if data_filter:
            data = data_filter(data)

        # content_type = "multipart/form-data; boundary=..."
        content_type = "pass"

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
        data = form.serialize()
        if data_filter:
            data = data_filter(data)

    if url:
        _req_post(req, url, data, complete, content_type)
    else:
        _req_post(
            req,
            correct_href(form.attr("action"), (_form[0],)),
            data,
            complete,
            content_type,
        )

    # if (
    #    _form[0].hasAttribute("data-region")
    #    and _form[0].getAttribute("data-region") == "table"
    # ):
    #    _req_post(req, corect_href(form.attr("action"), True), data, complete, content_type)
    # else:
    #    _req_post(req, corect_href(form.attr("action")), data, complete, content_type)


window.ajax_submit = ajax_submit


# def load_css(path):
#     global LOADED_FILES
#     if not (LOADED_FILES and path in LOADED_FILES):
#         LOADED_FILES[path] = None
#         req = __new__(XMLHttpRequest())
#
#         def _onload():
#             jQuery('<style type="text/css"></style>').html(req.responseText).appendTo(
#                 "head"
#             )
#
#         req.onload = _onload
#
#         req.open("GET", path, True)
#         req.send("")


def load_css(path, on_load=None):
    global LOADED_FILES
    if not (LOADED_FILES and path in LOADED_FILES):
        LOADED_FILES[path] = None
        req = XMLHttpRequest()

        def _onload():
            nonlocal req, on_load
            if on_load:
                on_load(req)
            else:
                jQuery('<style type="text/css"></style>').html(
                    req.responseText
                ).appendTo("head")

        req.onload = _onload

        req.open("GET", path, True)
        req.send("")


window.load_css = load_css


def on_load_js(path):
    global LOADED_FILES
    if LOADED_FILES and path in LOADED_FILES:
        functions = LOADED_FILES[path]
        if functions:
            for fun in functions:
                fun()
        LOADED_FILES[path] = None


def load_js(path, fun):
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
            # jQuery.globalEval(req.responseText)
            _requirejs = window.requirejs
            _require = window.require
            _define = window.define
            window.requirejs = None
            window.require = None
            window.define = None
            script = document.createElement("script")
            script.text = req.responseText
            document.head.appendChild(script).parentNode.removeChild(script)
            window.requirejs = _requirejs
            window.require = _require
            window.define = _define

            on_load_js(path)

        req.onload = _onload

        req.open("GET", path, True)
        req.send("")


window.load_js = load_js


def load_many_js(paths, fun):
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


def history_push_state(title, url, data=None):
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


def get_elem_from_string(html, selectors=None):
    temp = document.createElement("div")
    temp.classList.add("ajax-item")
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


def is_hidden(el):
    style = window.getComputedStyle(el)
    return style.display == "none"


window.is_hidden = is_hidden


def is_visible(el):
    return not is_hidden(el)


window.is_visible = is_visible

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
    global TEMPLATES
    if template_name in TEMPLATES:
        ret = TEMPLATES[template_name].replace("{title}", param["title"])
        if "href" in param:
            ret = ret.replace("{href}", param["href"])
        return ret
    return None


def super_query_selector(element, selector):
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


def super_insert(base_element, insert_selector, inserted_element):
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


_OPERATOR = (">>", "<<", ">", "(", ")")


def send_to_dom(html_text, base_elem):
    nonlocal _OPERATOR
    for operator in _OPERATOR:
        if "===" + operator in html_text:
            x = html_text.split("===" + operator)
            html = x[0]
            insert_selector = x[1] + ":" + operator
            inserted_element = get_elem_from_string(html, None)
            return super_insert(base_elem, insert_selector, inserted_element)
    return None


window.send_to_dom = send_to_dom


def remove_element(element):
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
                else:
                    aside.remove()

            jQuery.each(jQuery(element2).find(".plug"), _on_remove_aside)

            element2.remove()


window.remove_element = remove_element


def process_resize(target_element):
    param = {}
    param["w"] = window.innerWidth
    param["h"] = window.innerHeight
    body_rect = document.body.getBoundingClientRect()
    elements1 = Array.prototype.slice.call(
        target_element.querySelectorAll(".flexible_size")
    )
    elements2 = Array.prototype.slice.call(
        target_element.querySelectorAll(".flexible_size_round2")
    )
    elements3 = []
    if target_element.classList.contains(
        "flexible_size"
    ) or target_element.classList.contains("flexible_size_round2"):
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


def get_page(elem):
    if elem.hasClass(".tab-pane"):
        return elem
    else:
        return elem.closest(".tab-pane")


def get_table_type(elem):
    tabsort = elem.find(".tabsort")
    if tabsort.length == 0:
        tabsort = get_page(elem).find(".tabsort")
    if tabsort.length > 0:
        ret = tabsort.attr("table_type")
        if ret:
            return ret
    return ""


window.get_table_type = get_table_type


def can_popup():
    if jQuery(".modal-open").length > 0:
        return False
    else:
        return True


def correct_href(href, elements=None):
    if not href:
        return href

    only_table = False
    if elements != None:
        for element in elements:
            if (
                element != None
                and element.hasAttribute("data-region")
                and element.getAttribute("data-region").lower() == "table"
            ):
                only_table = True

    if only_table:
        if not "only_table" in href:
            if "?" in href:
                href += "&only_table=1"
            else:
                href += "?only_table=1"
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
            if not "only_content" in href:
                if "?" in href:
                    href += "&only_content=1"
                else:
                    href += "?only_content=1"

    if elements != None:
        for element in elements:
            if (
                element
                and element.hasAttribute("get-param")
                and element.getAttribute("get-param")
            ):
                if not element.getAttribute("get-param") in href:
                    if "?" in href:
                        href += "&" + element.getAttribute("get-param")
                    else:
                        href += "?" + element.getAttribute("get-param")
    return href


def remove_page_from_href(href):
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


def inline_maximize(elem):
    dialog = elem.closest("div.modal-content")
    if not dialog.classList.contains("maximized"):
        dialog.classList.add("maximized")

    b_min = dialog.querySelector("button.minimize")
    b_max = dialog.querySelector("button.maximize")
    b_min.style.display = "inline-block"
    b_max.style.display = "none"


window.inline_maximize = inline_maximize


def inline_minimize(elem):
    dialog = elem.closest("div.modal-content")
    if dialog.classList.contains("maximized"):
        dialog.classList.remove("maximized")

    b_min = dialog.querySelector("button.minimize")
    b_max = dialog.querySelector("button.maximize")
    b_min.style.display = "none"
    b_max.style.display = "inline-block"


window.inline_minimize = inline_minimize
