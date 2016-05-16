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
    
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins/ace/src-min';
    		this.value = opts.value;
    		this.href = opts.href;
    		this.changed = false;
    		var _on_mount = function () {
    			var self = this;
    			var _on_load = function () {
    				ace.config.set ('basePath', self.base_path);
    				var editor = ace.edit (self.ceditor);
    				var rect = editor.container.getBoundingClientRect ();
    				editor.container.style.position = 'absolute';
    				editor.container.style.top = (rect.top + 2) + 'px';
    				editor.container.style.right = '5px';
    				editor.container.style.bottom = '5px';
    				editor.container.style.left = '5px';
    				editor.setTheme ('ace/theme/textmate');
    				editor.getSession ().setMode ('ace/mode/python');
    				console.log("X1");
                    editor.setOptions ({minLines: 32});
                    console.log("X2");
    				var _on_input = function (e) {
    					var f = jQuery (':focus');
    					if (f.length > 0) {
    						var tag = f.get (0).nodeName.toLowerCase ();
    					}
    					else {
    						tag == '';
    					}
    					if (tag == 'textarea') {
    						self.changed = true;
    						self.update ();
    					}
    					else {
    						var _on_timeout = function () {
    							editor.focus ();
    						};
    						setTimeout (_on_timeout, 0);
    					}
    				};
                    console.log("U1");
    				editor.on ('input', _on_input);
                    console.log("U2");
                    console.log(this.value);
    				editor.getSession ().setValue (atob (self.value));
                    console.log("U3");
    				self.editor = editor;
                    console.log("U4");
    			};
    			load_js (self.base_path + '/ace.js', _on_load);
                console.log("U5");

    		};
    		this.on ('mount', _on_mount);
    		var on_save = function (e) {
    			if (this.href) {
    				var ajax_options = dict ([[method, 'POST'], [url, this.href], [dataType, 'html'], [data, dict ([[data, self.editor.getValue ()]])]]);
    				var _on_ajax = function () {
    					self.changed = false;
    					self.update ();
    				};
    				jQuery.ajax (ajax_options).done (_on_ajax);
    			}
    		};
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    			__all__.on_save = on_save;
    		__pragma__ ('</all>')
    	</script>
    
    
</code_editor>