<txtarea_editor>
    <div name="ceditor"></div>
    <script>
    
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins/ace/src-min';
    		this.rel_id = opts.rel_id;
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				ace.config.set ('basePath', self.base_path);
    				var editor = ace.edit (self.ceditor);
    				var txtarea = jQuery ('#' + self.rel_id).hide ();
    				editor.setOptions (dict ({'maxLines': 32}));
    				editor.setTheme ('ace/theme/textmate');
    				editor.getSession ().setMode ('ace/mode/markdown');
    				editor.getSession ().setValue (txtarea.val ());
    				var _on_change = function () {
    					txtarea.val (editor.getSession ().getValue ());
    				};
    				editor.getSession ().on ('change', _on_change);
    				self.editor = editor;
    			};
    			load_js (self.base_path + '/ace.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</txtarea_editor>