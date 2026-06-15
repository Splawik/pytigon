var BASE_PATH, TAG, TEMPLATE, comp, constructor, event_handler, init, save_click, stub1_context, stub2_err;
TAG = "ptig-wysiwygedit";
TEMPLATE = '        <style >\n' +
    '        :host { display: block; font-family: sans-serif; border: 1px solid #ccc; border-radius: 4px; }\n' +
    '        .toolbar { padding: 8px; border-bottom: 1px solid #ccc; background: #f9f9f9; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }\n' +
    '        .editor-content :first-child { margin-top: 0; }\n' +
    '        .editor-content > div { padding: 2px; }\n' +
    '        .editor-content table { border-collapse: collapse; table-layout: fixed; width: 100%; margin: 0; overflow: hidden; }\n' +
    '        .editor-content table td, .editor-content table th { border: 1px solid #ced4da; box-sizing: border-box; min-width: 1em; padding: 3px 5px; position: relative; vertical-align: top; }\n' +
    '        .editor-content table th { background-color: #f1f3f5; font-weight: bold; text-align: left; }\n' +
    '\n' +
    '        /* Kontener tabeli generowany przez Tiptap */\n' +
    '        .prose-mirror .tableWrapper {\n' +
    '          overflow-x: auto;\n' +
    '          margin: 1rem 0;\n' +
    '        }\n' +
    '\n' +
    '        /* Tabela musi mieć pozycjonowanie relatywne, aby uchwyty działały prawidłowo */\n' +
    '        .prose-mirror table {\n' +
    '          border-collapse: collapse;\n' +
    '          table-layout: fixed;\n' +
    '          width: 100%;\n' +
    '          margin: 0;\n' +
    '          overflow: hidden;\n' +
    '          position: relative; /* Kluczowe dla pozycjonowania uchwytów */\n' +
    '        }\n' +
    '\n' +
    '        .prose-mirror td, .prose-mirror th {\n' +
    '          min-width: 1em;\n' +
    '          border: 1px solid #ced4da;\n' +
    '          padding: 3px 5px;\n' +
    '          vertical-align: top;\n' +
    '          box-sizing: border-box;\n' +
    '          position: relative;\n' +
    '        }\n' +
    '\n' +
    '        /* --- STYLOWANIE UCHWYTÓW ZMIANY ROZMIARU (RESIZE HANDLES) --- */\n' +
    '\n' +
    '        /* Niewidoczna strefa łapania myszką na krawędzi kolumny */\n' +
    '        .prose-mirror .column-resize-handle {\n' +
    '          position: absolute;\n' +
    '          right: -2px;\n' +
    '          top: 0;\n' +
    '          bottom: -2px;\n' +
    '          width: 4px;\n' +
    '          z-index: 20;\n' +
    '          background-color: transparent;\n' +
    '          cursor: col-resize; /* Zmiana kursora na strzałki poziome */\n' +
    '        }\n' +
    '\n' +
    '        /* Wygląd linii w momencie, gdy użytkownik najeżdża myszką lub przeciąga krawędź */\n' +
    '        .prose-mirror .column-resize-handle:hover,\n' +
    '        .prose-mirror.resize-cursor .column-resize-handle {\n' +
    '          background-color: #3b82f6; /* Kolor linii (np. niebieski) */\n' +
    '        }\n' +
    '\n' +
    '        /* Wygląd wybranej komórki (opcjonalnie, przydatne przy zaznaczaniu) */\n' +
    '        .prose-mirror .selectedCell:after {\n' +
    '          z-index: 2;\n' +
    '          position: absolute;\n' +
    '          content: \"\";\n' +
    '          left: 0; right: 0; top: 0; bottom: 0;\n' +
    '          background: rgba(200, 200, 255, 0.4);\n' +
    '          pointer-events: none;\n' +
    '        }\n' +
    '\n' +
    '</style>\n' +
    '        <div class=\"toolbar\">\n' +
    '                <slot name=\"toolbar\" class=\"toolbar\">\n' +
    '                </slot>\n' +
    '        </div>\n' +
    '        <div class=\"editor-content p-1\"></div>\n' +
    '        <div class=\"editorframe p-1\">\n' +
    '                <div class=\"editor-container p-1\"></div>\n' +
    '        </div>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/_schcomponents/tiptap/";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "tiptap.js"], [], true));
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
        return null;
    };

    comp.options["constructor"] = constructor;
    init = function flx_init (component) {
        var Editor, Highlight, Image, StarterKit, TableKit, TextStyleKit, _handleToolbarChange, _handleToolbarClick, _handleToolbarInput, _updateToolbarStates, content, editor, editor_div, editor_module, extensions, onTransaction, onUpdate, on_save, state, toolbarSlot;
        editor_div = component.root.querySelector("div.editor-content");
        editor_module = component.modules[0];
        Editor = editor_module.Editor;
        StarterKit = editor_module.StarterKit;
        TextStyleKit = editor_module.TextStyleKit;
        Highlight = editor_module.Highlight;
        TableKit = editor_module.TableKit;
        Image = editor_module.Image;
        editor = null;
        _updateToolbarStates = (function flx__updateToolbarStates () {
            var _update_buttons, buttons, toolbarSlot;
            if ((!_pyfunc_truthy(editor))) {
                return null;
            }
            toolbarSlot = component.querySelector("div.toolbar");
            buttons = toolbarSlot.querySelectorAll("[data-command]");
            _update_buttons = (function flx__update_buttons (button) {
                var command, level, stateName;
                command = button.getAttribute("data-command");
                if ((_pyfunc_op_equals(command, "toggleBulletList") && (_pyfunc_truthy(editor.isActive("bulletList"))))) {
                    return button.classList.add("active");
                }
                if ((_pyfunc_op_equals(command, "toggleOrderedList") && (_pyfunc_truthy(editor.isActive("orderedList"))))) {
                    return button.classList.add("active");
                }
                if ((_pyfunc_op_equals(command, "toggleLink") && (_pyfunc_truthy(editor.isActive("link"))))) {
                    return button.classList.add("active");
                }
                if ((_pyfunc_op_equals(command, "insertImage") && (_pyfunc_truthy(editor.isActive("image"))))) {
                    return button.classList.add("active");
                }
                if (_pyfunc_op_equals(command, "toggleHeading")) {
                    level = (_pyfunc_truthy(parseInt(button.getAttribute("data-level"), 10))) || 1;
                    return button.classList.toggle("active", editor.isActive("heading", ({level: level})));
                }
                stateName = (_pymeth_replace.call(command, "toggle", "").toLowerCase)();
                button.classList.toggle("active", editor.isActive(stateName));
                return null;
            }).bind(this);

            buttons.forEach(_update_buttons);
            return null;
        }).bind(this);

        onTransaction = (function flx_onTransaction (ed, transaction) {
            _updateToolbarStates();
            return null;
        }).bind(this);

        onUpdate = (function flx_onUpdate (ed) {
            if ((_pyfunc_hasattr(component, "textarea") && _pyfunc_truthy(component.textarea))) {
                component.textarea.value = editor.getHTML();
            }
            return null;
        }).bind(this);

        extensions = [StarterKit, TextStyleKit, Highlight.configure(({multicolor: true})), TableKit.configure(({table: ({resizable: true})})), Image.configure(({inline: true, allowBase64: true, resize: ({enabled: true, alwaysPreserveAspectRatio: true})}))];
        if ((_pyfunc_hasattr(component, "textarea") && _pyfunc_truthy(component.textarea))) {
            content = component.textarea.value;
        } else {
            content = "<p>Enter text</p>";
        }
        editor = new Editor(({element: editor_div, extensions: extensions, content: content}));
        editor.on("transaction", onTransaction);
        editor.on("update", onUpdate);
        component.editor = editor;
        _handleToolbarClick = (function flx__handleToolbarClick (event) {
            var button, chain, command, level, url;
            button = event.target.closest("[data-command]");
            if (_pyfunc_truthy(((!_pyfunc_truthy(button))) || (!_pyfunc_truthy(editor)))) {
                return null;
            }
            command = button.getAttribute("data-command");
            chain = (editor.chain().focus)();
            if (_pyfunc_op_equals(command, "toggleHeading")) {
                level = (_pyfunc_truthy(parseInt(button.getAttribute("data-level"), 10))) || 1;
                return ((chain.toggleHeading(({level: level}))).run)();
            }
            if (_pyfunc_op_equals(command, "toggleLink")) {
                if (_pyfunc_truthy(editor.isActive("link"))) {
                    return (chain.unsetLink().run)();
                }
                url = window.prompt("Wpisz adres URL:");
                if (_pyfunc_truthy(url)) {
                    ((chain.setLink(({href: url}))).run)();
                }
                return null;
            }
            if (_pyfunc_op_equals(command, "insertTable")) {
                return ((chain.insertTable(({rows: 3, cols: 3, withHeaderRow: true}))).run)();
            }
            if (_pyfunc_op_equals(command, "addColumnBefore")) {
                return (chain.addColumnBefore().run)();
            }
            if (_pyfunc_op_equals(command, "addColumnAfter")) {
                return (chain.addColumnAfter().run)();
            }
            if (_pyfunc_op_equals(command, "deleteColumn")) {
                return (chain.deleteColumn().run)();
            }
            if (_pyfunc_op_equals(command, "addRowBefore")) {
                return (chain.addRowBefore().run)();
            }
            if (_pyfunc_op_equals(command, "addRowAfter")) {
                return (chain.addRowAfter().run)();
            }
            if (_pyfunc_op_equals(command, "deleteRow")) {
                return (chain.deleteRow().run)();
            }
            if (_pyfunc_op_equals(command, "deleteTable")) {
                return (chain.deleteTable().run)();
            }
            if ((_pyfunc_truthy(chain[command]) && ((_pyfunc_op_equals((chain[command].constructor), Function))))) {
                ((chain[command]()).run)();
            }
            return null;
        }).bind(this);

        _handleToolbarInput = (function flx__handleToolbarInput (event) {
            var command, input, value;
            input = event.target.closest("[data-command-input]");
            if (_pyfunc_truthy(((!_pyfunc_truthy(input))) || (!_pyfunc_truthy(editor)))) {
                return null;
            }
            command = input.getAttribute("data-command-input");
            value = input.value;
            if (_pyfunc_op_equals(command, "setColor")) {
                (((((editor.chain().focus)()).setColor)(value)).run)();
            }
            if (_pyfunc_op_equals(command, "setHighlight")) {
                (((((editor.chain().focus)()).setHighlight)(({color: value}))).run)();
            }
            return null;
        }).bind(this);

        _handleToolbarChange = (function flx__handleToolbarChange (event) {
            var _on_load, file, fileInput, reader;
            fileInput = event.target.closest("[data-command-file]");
            if (_pyfunc_truthy(((!_pyfunc_truthy(fileInput))) || ((!_pyfunc_truthy(editor))) || (!fileInput.files.length))) {
                return null;
            }
            file = fileInput.files[0];
            reader = new FileReader();
            _on_load = (function flx__on_load (e) {
                (((((editor.chain().focus)()).setImage)(({src: e.target.result}))).run)();
                fileInput.value = "";
                return null;
            }).bind(this);

            reader.onload = _on_load;
            reader.readAsDataURL(file);
            return null;
        }).bind(this);

        toolbarSlot = component.querySelector("div.toolbar");
        toolbarSlot.addEventListener("click", _handleToolbarClick);
        toolbarSlot.addEventListener("input", _handleToolbarInput);
        toolbarSlot.addEventListener("change", _handleToolbarChange);
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

    save_click = function flx_save_click (component, data, src, callback) {
        var _complete;
        if ((_pyfunc_op_equals(src.getAttribute("namespace"), component.getAttribute("namespace")))) {
            _complete = (function flx__complete () {
                callback();
                return null;
            }).bind(this);

            window.GLOBAL_BUS.send_event("on_log", component.editor.getHTML(), component, _complete);
        }
        return null;
    };

    event_handler = ({save_click: save_click});
    comp.options["init"] = init;
    comp.options["event_handler"] = event_handler;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}