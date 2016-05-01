<code_editor>
    <div class="inline">
                    <button disabled={ !changed } onclick={save} class="btn btn-sm btn-primary">
                            <span class="fa fa-floppy-o"></span>
                    </button>
    </div>
    <div class="inline inline_title">
            <strong>{opts.title}</strong>
    </div>
    <div name="ceditor"></div>
    <style >
        code_editor div.inline {
            display: inline-block;
        }
        code_editor div.inline_title {
            margin-left: 10px;
        }
        code_editor button.btn {
            margin: 0px;
        }
    </style>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins/ace/src-min";
    this.value = opts.value;
    this.href = opts.href;
    this.changed = false;
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/ace.js", function () {
            var editor, rect;
            ace.config.set("basePath", self.base_path);
            editor = ace.edit(self.ceditor);
            rect = editor.container.getBoundingClientRect();
            editor.container.style.position = "absolute";
            editor.container.style.top = rect.top + 2 + "px";
            editor.container.style.right = "5px";
            editor.container.style.bottom = "5px";
            editor.container.style.left = "5px";
            editor.setTheme("ace/theme/textmate");
            editor.getSession().setMode("ace/mode/python");
            editor.setOptions((function(){
                var ρσ_d = {};
                ρσ_d[minLines] = 32;
                return ρσ_d;
            }).call(this));
            editor.on("input", (function() {
                var ρσ_anonfunc = function (e) {
                    var f, tag;
                    f = jQuery(":focus");
                    if (f.length > 0) {
                        tag = f.get(0).nodeName.toLowerCase();
                    } else {
                        (tag === "" || typeof tag === "object" && ρσ_equals(tag, ""));
                    }
                    if ((tag === "textarea" || typeof tag === "object" && ρσ_equals(tag, "textarea"))) {
                        self.changed = true;
                        self.update();
                    } else {
                        setTimeout(function () {
                            editor.focus();
                        }, 0);
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            editor.getSession().setValue(atob(self.value));
            self.editor = editor;
        });
    });
    save(e) {
        var ajax_options;
        if (this.href) {
            ajax_options = (function(){
                var ρσ_d = {};
                ρσ_d[method] = "POST";
                ρσ_d[url] = this.href;
                ρσ_d[dataType] = "html";
                ρσ_d[data] = (function(){
                    var ρσ_d = {};
                    ρσ_d[data] = self.editor.getValue();
                    return ρσ_d;
                }).call(this);
                return ρσ_d;
            }).call(this);
            jQuery.ajax(ajax_options).done(function () {
                self.changed = false;
                self.update();
            });
        }
    };
    Object.defineProperties(on_save, {
        __argnames__ : {value: ["e"]}
    });
    </script>
    
    
</code_editor>