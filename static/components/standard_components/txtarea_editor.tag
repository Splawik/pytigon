<txtarea_editor>
    <div name="ceditor"></div>
    <script>
    
    
    
    base_path = BASE_PATH + "static/vanillajs_plugins/ace/src-min";
    this.rel_id = opts.rel_id;
    self = this;
    this.on("mount", function() {
        load_js(base_path + "/ace.js", function() {
            var editor, txtarea;
            ace.config.set("basePath", base_path);
            editor = ace.edit(self.ceditor);
            txtarea = $("#" + self.rel_id).hide();
            editor.setOptions({
                maxLines: 32
            });
            editor.setTheme("ace/theme/textmate");
            editor.getSession().setMode("ace/mode/markdown");
            editor.getSession().setValue(txtarea.val());
            editor.getSession().on("change", function() {
                txtarea.val(editor.getSession().getValue());
            });
            self.editor = editor;
        });
    });</script>
    
    
</txtarea_editor>