LOADED_FILES = {}

def download_binary_file(buf, content_disposition):
    l = buf.length
    buffer = __new__(ArrayBuffer(l))
    view = __new__(Uint8Array(buffer))
    for i in range(l):
        view[i] = buf.charCodeAt(i)
    mimetype = 'text/html'
    if 'odf' in content_disposition or 'ods' in content_disposition:
        mimetype = 'application/vnd.oasis.opendocument.formula'
    elif 'pdf' in content_disposition:
        mimetype = 'application/pdf'
    elif 'zip' in content_disposition:
        mimetype = 'application/x-compressed'
    elif 'xls' in content_disposition:
        mimetype = 'application/excel'
    blob = __new__(Blob([view], {'type': mimetype }))
    blobURL = window.URL.createObjectURL(blob)
    window.open(blobURL)


def ajax_get(url, complete):
    req = __new__(XMLHttpRequest())

    def _onload():
        disp = req.getResponseHeader('Content-Disposition')
        if disp and 'attachment' in disp:
            download_binary_file(req.response, disp)
            complete(None)
        else:
            complete(req.responseText)

    req.onload = _onload

    req.open('GET', url, True)
    req.send()

window.ajax_get = ajax_get

def ajax_load(elem, url, complete):

    def _onload(responseText):
        elem.html(responseText)
        complete(responseText)

    ajax_get(url, _onload)

window.ajax_load = ajax_load

def _req_post(req, url, data, complete):
    def _onload():
        disp = req.getResponseHeader('Content-Disposition')
        if disp and 'attachment' in disp:
            download_binary_file(req.response, disp)
            complete(None)
        else:
            complete(req.responseText)
    req.onload = _onload

    req.open("POST", url, True)

    req.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'))

    if data.length:
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        req.setRequestHeader("Content-length", data.length)
        req.setRequestHeader("Connection", "close")

    req.send(data)


def ajax_post(url, data, complete):
    req = __new__(XMLHttpRequest())
    _req_post(req, url, data, complete)

window.ajax_post = ajax_post

def ajax_submit(form, complete):
    req = __new__(XMLHttpRequest())

    if form.find("[type='file']").length > 0:
        form.attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
        data = __new__(FormData(form[0]))
        form.closest("div").append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>")
        def _progressHandlingFunction(e):
            if e.lengthComputable:
                jQuery("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%")
        req.upload.addEventListener("progress", _progressHandlingFunction, False)
    else:
        data = form.serialize()

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
    if jQuery("div.dialog-form").hasClass('in') or jQuery("div.dialog-form-delete").hasClass('in') or jQuery("div.dialog-form-info").hasClass('in'):
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
            jQuery.globalEval(req.responseText)
            on_load_js(path)

        req.onload = _onload

        req.open('GET', path, True)
        req.send('')

window.load_js = load_js

def load_many_js(paths, fun):
    counter = 0

    def _fun():
        nonlocal counter
        counter = counter - 1
        if counter == 0:
            fun()

    for path in paths.split(paths, ';'):
        if path.lenght()>0:
            counter = counter + 1
            load_js(path, _fun)


window.load_many_js = load_many_js

def history_push_state(title, url, data=None):
    url2 = url.split("?")[0]
    if data:
        data2 = [LZString.compress(data[0]),data[1]]
    else:
        data2 = title
    window.history.pushState(data2, title, url2)

