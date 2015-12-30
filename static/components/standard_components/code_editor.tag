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
    this.on("mount", function() {
        var self;
        self = this;
        load_js(self.base_path + "/ace.js", function() {
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
            editor.setOptions({
                minLines: 32
            });
            editor.on("input", function(e) {
                var f, tag;
                f = jQuery(":focus");
                if (f.length > 0) {
                    tag = f.get(0).nodeName.toLowerCase();
                } else {
                    tag === "";
                }
                if (tag === "textarea") {
                    self.changed = true;
                    self.update();
                } else {
                    setTimeout(function() {
                        editor.focus();
                    }, 0);
                }
            });
            editor.getSession().setValue(atob(self.value));
            self.editor = editor;
        });
    });
    save(e) {
        var ajax_options;
        if (this.href) {
            ajax_options = {
                method: "POST",
                url: this.href,
                dataType: "html",
                data: {
                    data: self.editor.getValue()
                }
            };
            jQuery.ajax(ajax_options).done(function() {
                self.changed = false;
                self.update();
            });
        }
    }</script>
    
    
</code_editor>