__pragma__ ('alias', 'S', '$')

LOADED_FILES = {}

def evalJSFromHtml(html):
    newElement = document.createElement('div')
    newElement.innerHTML = html

    scripts = newElement.getElementsByTagName("script")
    def eval_fun(id, value):
        eval(value.innerHTML)

    jQuery.each(scripts, eval_fun)


def mount_html(elem, html_txt):
    if window.COMPONENT_INIT and len(window.COMPONENT_INIT)>0:
        elem.empty()
        res = Vue.compile("<div>"+html_txt+"</div>")
        if elem and elem.length>0:
            vm = __new__(Vue( { 'render': res.render, 'staticRenderFns': res.staticRenderFns } ))
            component = vm.S__mount()

            def _append(index, value):
                if value:
                    elem[0].appendChild(value)

            jQuery.each(component.S__el.childNodes, _append)

            evalJSFromHtml(html_txt)
    else:
        elem.html(html_txt)

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
    #mimetype = 'text/html'
    #if 'odf' in content_disposition or 'ods' in content_disposition:
    #    mimetype = 'application/vnd.oasis.opendocument.formula'
    #elif 'pdf' in content_disposition:
    #    mimetype = 'application/pdf'
    #elif 'zip' in content_disposition:
    #    mimetype = 'application/x-compressed'
    #elif 'xls' in content_disposition:
    #    mimetype = 'application/excel'

    file_name = "temp.dat"
    var_list = content_disposition.split(';')
    for pos in var_list:
        if 'filename' in pos:
            file_name = pos.split('=')[1]
            break

    save_as(buf, file_name)


def ajax_get(url, complete, process_req=None):
    req = __new__(XMLHttpRequest())

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
        if process_blob:
            disp = req.getResponseHeader('Content-Disposition')
            if disp and 'attachment' in disp:
                download_binary_file(req.response, disp)
                complete(None)
            else:
                reader = __new__(FileReader())

                def _on_reader_load():
                    complete(reader.result)

                reader.onload = _on_reader_load
                reader.readAsText(req.response)
        else:
            complete(req.response)

    req.onload = _onload

    req.open('GET', url, True)
    req.send()

window.ajax_get = ajax_get

def ajax_load(elem, url, complete):

    def _onload(responseText):
        mount_html(elem, responseText)
        complete(responseText)

    ajax_get(url, _onload)

window.ajax_load = ajax_load

def _req_post(req, url, data, complete):
    process_blob = False
    try:
        req.responseType = "blob"
        process_blob = True
    except:
        pass
    def _onload():
        nonlocal process_blob
        if process_blob:
            disp = req.getResponseHeader('Content-Disposition')
            if disp and 'attachment' in disp:
                download_binary_file(req.response, disp)
                complete(None)
            else:
                reader = __new__(FileReader())

                def _on_reader_load():
                    complete(reader.result)

                reader.onload = _on_reader_load
                reader.readAsText(req.response)
        else:
            complete(req.response)

    req.onload = _onload

    req.open("POST", url, True)

    req.setRequestHeader("X-CSRFToken", Cookies.js_get('csrftoken'))

    if data.length:
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        #req.setRequestHeader("Content-length", data.length)
        #req.setRequestHeader("Connection", "close")

    req.send(data)


def ajax_post(url, data, complete, process_req=None):
    req = __new__(XMLHttpRequest())
    if process_req:
        process_req(req)
    _req_post(req, url, data, complete)

window.ajax_post = ajax_post

def ajax_submit(form, complete, data_filter=None, process_req=None):
    req = __new__(XMLHttpRequest())

    if process_req:
        process_req(req)

    if form.find("[type='file']").length > 0:
        form.attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
        data = __new__(FormData(form[0]))
        if data_filter:
            data = data_filter(data)
        #if not form.f("div").find("#progress").length == 1:
        if not form.find("#progress").length == 1:        
            form.find('div.inline-form-body').append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>")
            #form.closest("div").append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>")
        else:
            jQuery("#progress").width("0%")
        def _progressHandlingFunction(e):
            if e.lengthComputable:
                jQuery("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%")
        req.upload.addEventListener("progress", _progressHandlingFunction, False)
    else:
        data = form.serialize()
        if data_filter:
            data = data_filter(data)

    _req_post(req, corect_href(form.attr("action")), data, complete)

window.ajax_submit = ajax_submit

def get_page(elem):
    if elem.hasClass('.tab-pane'):
        return elem
    else:
        return elem.closest('.tab-pane')


def get_table_type(elem):
    tabsort = elem.find('.tabsort')
    if tabsort.length == 0:
        tabsort = get_page(elem).find('.tabsort')
    if tabsort.length>0:
        ret = tabsort.attr('table_type')
        if ret:
            return ret
        else:
            return "scrolled"
    else:
        return ""


def can_popup():
    if jQuery('.modal-open').length > 0:
    #if jQuery("div.dialog-form").hasClass('show') or jQuery("div.dialog-form-delete").hasClass('show') or jQuery("div.dialog-form-info").hasClass('show'):
        return False
    else:
        return True


def corect_href(href):
    if 'only_content' in href:
        return href
    else:
        if '?' in href:
            return href + '&only_content=1'
        else:
            return href + '?only_content=1'


def handle_class_click(fragment_obj, obj_class, fun):
    def _on_click(e):
        src_obj = jQuery(this)
        e.preventDefault()
        fun(this)
        return False
    fragment_obj.on( "click", "."+obj_class, _on_click)


def load_css(path):
    nonlocal LOADED_FILES
    if not (LOADED_FILES and path in LOADED_FILES):
        LOADED_FILES[path] = None
        req = __new__(XMLHttpRequest())

        def _onload():
            jQuery('<style type="text/css"></style>').html(req.responseText).appendTo("head")

        req.onload = _onload

        req.open('GET', path, True)
        req.send('')
window.load_css = load_css

def on_load_js(path):
    nonlocal LOADED_FILES
    if LOADED_FILES and path in LOADED_FILES:
        functions = LOADED_FILES[path]
        if functions:
            for fun in functions:
                fun()
        LOADED_FILES[path] = None


def load_js(path, fun):
    nonlocal LOADED_FILES
    if LOADED_FILES and path in LOADED_FILES:
        if LOADED_FILES[path]:
            LOADED_FILES[path].push(fun)
        else:
            fun()
    else:
        LOADED_FILES[path] = [fun,]
        req = __new__(XMLHttpRequest())
        def _onload():
            #jQuery.globalEval(req.responseText)

            script = document.createElement("script")
            script.text = req.responseText
            document.head.appendChild( script ).parentNode.removeChild( script )

            on_load_js(path)

        req.onload = _onload

        req.open('GET', path, True)
        req.send('')

window.load_js = load_js

def load_many_js(paths, fun):
    counter = 1

    def _fun():
        nonlocal counter
        counter = counter - 1
        if counter == 0:
            fun()

    for path in paths.split(';'):
        if path.length>0:
            counter = counter + 1
            load_js(path, _fun)
    _fun()

window.load_many_js = load_many_js

def history_push_state(title, url, data=None):
    url2 = url.split("?")[0]
    if data:
        data2 = [LZString.compress(data[0]),data[1]]
    else:
        data2 = title
    window.history.pushState(data2, title, url2)


def animate_combo(button, obj1, obj2,  obj1_style_off, obj1_style_on, obj2_style_off, obj2_style_on, speed, end=None):
    if end:
        end2 = end
    else:
        def end2():
            pass

    def _animate():
        if button.hasClass("on"):
            button.removeClass("on")
            obj1.animate(obj1_style_off, speed)
            obj2.animate(obj2_style_off, speed, 'swing', end2)
        else:
            button.addClass("on")
            obj1.animate(obj1_style_on, speed)
            obj2.animate(obj2_style_on, speed, 'swing', end2)

    button.click(_animate)

window.animate_combo = animate_combo

