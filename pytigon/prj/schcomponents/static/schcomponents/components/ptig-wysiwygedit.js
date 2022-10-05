var BASE_PATH, TAG, TEMPLATE, comp, constructor, init, stub1_context, stub2_err;
TAG = "ptig-wysiwygedit";
TEMPLATE = '        <slot></slot>\n' +
    '        <div class=\"editorframe\">\n' +
    '                <div class=\"editor-container\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/quill";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/shadowquill.js"], [BASE_PATH + "/quill.snow.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null, name: null});
    comp.options["template"] = TEMPLATE;
    constructor = function flx_constructor (component) {
        var toolbar_div;
        component.textarea = component.querySelector("textarea");
        if (_pyfunc_truthy(component.textarea)) {
            component.textarea.style.display = "none";
        }
        toolbar_div = component.querySelector("div[slot='toolbar']");
        if (_pyfunc_truthy(toolbar_div)) {
            component.toolbar = window.JSON.parse(toolbar_div.innerHTML);
        } else {
            component.toolbar = null;
        }
        return null;
    };

    comp.options["constructor"] = constructor;
    init = function flx_init (component) {
        var editor, editor_div, editor_options, on_change, on_save, state, sync;
        editor_div = component.root.querySelector("div.editor-container");
        editor_options = ({modules: ({syntax: false}), theme: "snow"});
        if (_pyfunc_truthy(component.toolbar)) {
            editor_options["modules"]["toolbar"] = component.toolbar;
        }
        editor = new Quill(editor_div, editor_options);
        component.editor = editor;
        sync = (function flx_sync () {
            if ((component.textarea.childNodes.length > 0)) {
                (jQuery(component.textarea).text)(editor_div.children[0].innerHTML);
            } else {
                (jQuery(component.textarea).text)("");
            }
            return null;
        }).bind(this);

        on_change = (function flx_on_change () {
            component.set_state(({changed: true}));
            return null;
        }).bind(this);

        if (_pyfunc_truthy(component.textarea)) {
            editor.setContents([]);
            if ((component.textarea.childNodes.length > 0)) {
                editor.clipboard.dangerouslyPasteHTML(0, component.textarea.childNodes[0].nodeValue);
            }
            editor.on("text-change", sync);
        } else {
            editor.on("text-change", on_change);
        }
        on_save = (function flx_on_save (event) {
            var _on_ajax, ajax_options, href;
            if (_pyfunc_truthy(event.currentTarget.hasAttribute("href"))) {
                href = event.currentTarget.getAttribute("href");
                ajax_options = ({method: "POST", url: href, dataType: "html", data: ({data: editor_div.children[0].innerHTML})});
                _on_ajax = (function flx__on_ajax () {
                    component.set_state(({changed: false}));
                    return null;
                }).bind(this);

                (jQuery.ajax(ajax_options).done)(_on_ajax);
            }
            return null;
        }).bind(this);

        state = ({on_save: on_save, changed: false});
        component.set_state(state);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}