<txtarea_editor>
    <div name="ceditor"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins/ace/src-min";
    this.rel_id = opts.rel_id;
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/ace.js", function () {
            var editor, txtarea;
            ace.config.set("basePath", self.base_path);
            editor = ace.edit(self.ceditor);
            txtarea = $("#" + self.rel_id).hide();
            editor.setOptions((function(){
                var ρσ_d = {};
                ρσ_d["maxLines"] = 32;
                return ρσ_d;
            }).call(this));
            editor.setTheme("ace/theme/textmate");
            editor.getSession().setMode("ace/mode/markdown");
            editor.getSession().setValue(txtarea.val());
            editor.getSession().on("change", function () {
                txtarea.val(editor.getSession().getValue());
            });
            self.editor = editor;
        });
    });</script>
    
    
</txtarea_editor>