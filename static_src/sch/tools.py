__pragma__ ('alias', 'S', '$')

LOADED_FILES = {}

FIRST_INIT = True
FRAGMENT_INIT_FUN = []

def register_fragment_init_fun(fun):
    global FRAGMENT_INIT_FUN
    FRAGMENT_INIT_FUN.append(fun)

def fragment_init(elem=None):
    global FIRST_INIT, FRAGMENT_INIT_FUN

    if elem:
        elem2 = elem
    else:
        elem2 = window.ACTIVE_PAGE.page

    format = {
        'singleDatePicker': True,
        'showDropdowns': True,
        "buttonClasses": "btn",
        "applyClass": "btn-success align-top",
        "cancelClass": "btn-danger btn-sm align-top",
        "timePicker24Hour": True,
        "autoApply": True,
        'locale': {
            'format': 'YYYY-MM-DD',
            "separator": "-",
            'applyLabel': "&nbsp; OK &nbsp;",
            'cancelLabel': "<i class='fa fa-close'></i>",
        }
    }

    d = elem2.find('div.form-group .datefield input')
    d.daterangepicker(format)

    format['locale']['format'] = 'YYYY-MM-DD HH:mm'
    format['timePicker'] = True
    format['timePickerIncrement'] = 30

    d = elem2.find('div.form-group .datetimefield input')
    d.daterangepicker(format)


    jQuery('.selectpicker').selectpicker()

    def _on_blur(e):
        if e['type'] == 'focus' or this.value.length > 0:
            test = True
        else:
            test = False
        jQuery(this).parents('.form-group').toggleClass('focused',test)

    elem2.find('.label-floating .form-control').on('focus blur', _on_blur).trigger('blur')

    def load_inline_frame():
        frame = jQuery(this)
        frame.append(INLINE_FRAME_HTML)
        obj2 = frame.find("div.frame-data-inner")
        if obj2.length > 0:
            url = frame.attr('href')
            def complete(txt):
                pass
            ajax_load(obj2, url, complete)

    elem2.find('.inline_frame').each(load_inline_frame)

    elem2.find('.django-select2').djangoSelect2({'width': 'calc(100% - 48px)'})

    def init_select2_ctrl():
        sel2 = jQuery(this)
        src = sel2.closest(".input-group")
        if src.length == 1:
            if src[0].hasAttribute("item_id"):
                id = src.attr('item_id')
                if id:
                    text = src.attr('item_str')
                    sel2.append(jQuery("<option>", { "value": id, "text": text }))
                    sel2.val(id.toString())
                    sel2.trigger('change')

    elem2.find('.django-select2').each(init_select2_ctrl)

    if window.BASE_FRAGMENT_INIT:
        window.BASE_FRAGMENT_INIT()

    #datatable_onresize()

    for fun in FRAGMENT_INIT_FUN:
        fun(elem2)


def evalJSFromHtml(html):
    newElement = document.createElement('div')
    newElement.innerHTML = html

    scripts = newElement.getElementsByTagName("script")
    def eval_fun(id, value):
        eval(value.innerHTML)

    jQuery.each(scripts, eval_fun)


def evalCSSFromHtml(html, elem):
    newElement = document.createElement('div')
    newElement.innerHTML = html

    css = newElement.getElementsByTagName("style")
    def eval_fun(id, value):
        #elem.append("<style scoped></style>")
        #if value.id:
        #eval(value.innerHTML)
        #s = jQuery("<style scoped></style>")
        jQuery(value).attr('scoped', 'scoped')
        #s.innerHTML = value
        elem.append(value)

    jQuery.each(css, eval_fun)


MOUNT_INIT_FUN = []

def register_mount_fun(fun):
    global MOUNT_INIT_FUN
    MOUNT_INIT_FUN.append(fun)

def mount_html(elem, html_txt, run_fragment_init=True, component_init=True):
    global MOUNT_INIT_FUN
    if component_init and window.COMPONENT_INIT and len(window.COMPONENT_INIT)>0:
        try:
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
                evalCSSFromHtml(html_txt, elem)
        except:
            elem.html(html_txt)
    else:
        elem.html(html_txt)

    if run_fragment_init:
        fragment_init(elem)

    if MOUNT_INIT_FUN:
        for fun in MOUNT_INIT_FUN:
            fun(elem)

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

    req.open('GET', url, True)
    #req.overrideMimeType('text/plain; charset=x-user-defined')
    req.send(None)

window.ajax_get = ajax_get

def ajax_load(elem, url, complete):

    def _onload(responseText):
        mount_html(elem, responseText)
        complete(responseText)

    ajax_get(url, _onload)

window.ajax_load = ajax_load

def _req_post(req, url, data, complete, content_type):
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

    req.setRequestHeader("X-CSRFToken", Cookies.js_get('csrftoken'))
    if content_type:
        req.setRequestHeader('Content-Type', content_type)
    elif data.length:
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
    content_type = None
    req = __new__(XMLHttpRequest())

    if process_req:
        process_req(req)

    if form.find("[type='file']").length > 0:
        #form.attr( "enctype", "multipart/form-data" ).attr( "encoding", "multipart/form-data" )
        data = __new__(FormData(form[0]))
        if data_filter:
            data = data_filter(data)
        #if not form.f("div").find("#progress").length == 1:

        #var parameters = [];
        #for(var pair of data.entries()) {
        #    parameters.push(
        #        encodeURIComponent(pair[0]) + '=' +
        #        encodeURIComponent(pair[1])
        #    )
        #}
        #data = parameters.join('&');
        content_type = 'multipart/form-data'

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

    _req_post(req, corect_href(form.attr("action")), data, complete, content_type)

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
    return ""


def can_popup():
    if jQuery('.modal-open').length > 0:
    #if jQuery("div.dialog-form").hasClass('show') or jQuery("div.dialog-form-delete").hasClass('show') or jQuery("div.dialog-form-info").hasClass('show'):
        return False
    else:
        return True


def corect_href(href, only_table=False):
    if only_table:
        if 'only_table' in href:
            return href
    elif 'only_content' in href:
        return href

    if only_table:
        if '?' in href:
            return href + '&only_table=1'
        else:
            return href + '?only_table=1'
    else:
        if '?' in href:
            return href + '&only_content=1'
        else:
            return href + '?only_content=1'


def remove_page_from_href(href):
    x = href.split("?")
    if len(x)>1:
        x2 = x[1].split('&')
        if len(x2) > 1:
            x3 = []
            for pos in x2:
                if not 'page=' in pos:
                    x3.append(pos)
            return x[0]+'?'+ ("".join(x3))
        else:
            if 'page=' in x2[0]:
                return x2
            else:
                return href
    return href

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

window.history_push_state = history_push_state


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

#window.icons = {
#    'refresh': 'fa-refresh', 'toggle': 'fa-toggle-on fa-lg', 'columns': 'fa-th-list', 'detailOpen': 'fa-plus-square',
#     'detailClose': 'fa-minus-square'
#}

window.icons = {
    'time': 'fa fa-clock-o',
    'date': 'fa fa-calendar',
    'up': 'fa fa-chevron-up',
    'down': 'fa fa-chevron-down',
    'previous': 'fa fa-chevron-left',
    'next': 'fa fa-chevron-right',
    'today': 'fa fa-calendar-check-o',
    'clear': 'fa fa-trash',
    'close': 'fa fa-times',
    'paginationSwitchDown': 'fa-chevron-down',
    'paginationSwitchUp': 'fa-chevron-up',
    'refresh': 'fa-refresh',
    'toggle': 'fa-list-alt',
    'columns': 'fa-th',
    'detailOpen': 'fa-plus',
    'detailClose': 'fa-minus'
}

def get_and_run_script(url, elem, e):
    def _on_load_js(html_text):
        nonlocal elem, e
        object = jQuery(elem)
        x = jQuery(html_text).html()
        if x:
            eval(x)
        object = None
    ajax_get(url, _on_load_js)
