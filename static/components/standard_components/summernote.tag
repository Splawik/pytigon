<summernote>
    <div class="inline">
                    <button onclick={save} class="btn btn-sm btn-primary">
                            <span class="fa fa-floppy-o"></span>
                    </button>
    </div>
    <div class="inline inline_title">
            <strong>{opts.title}</strong>
    </div>
    <div name="summernote"></div>
    <style >
        summernote div.inline {
            display: inline-block;
        }
        summernote div.inline_title {
            margin-left: 10px;
        }
        summernote button.btn {
            margin: 0px;
        }
    </style>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/bootstrap_plugins/summernote";
    this.value = opts.value;
    this.href = opts.href;
    load_css(this.base_path + "/summernote.css");
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/summernote.min.js", function () {
            var editor, rect;
            editor = jQuery(self.summernote);
            rect = self.summernote.getBoundingClientRect();
            self.summernote.style.position = "absolute";
            self.summernote.style.top = rect.top + 2 + "px";
            self.summernote.style.right = "5px";
            self.summernote.style.bottom = "5px";
            self.summernote.style.left = "5px";
            editor.html(atob(self.value));
            editor.summernote();
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
                    ρσ_d[data] = self.editor.summernote("code");
                    return ρσ_d;
                }).call(this);
                return ρσ_d;
            }).call(this);
            jQuery.ajax(ajax_options).done(function () {
                self.update();
            });
        }
    };
    Object.defineProperties(on_save, {
        __argnames__ : {value: ["e"]}
    });
    </script>
    
    
</summernote>