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
    
    		var __symbols__ = ['__esv5__'];
    		this.base_path = BASE_PATH + 'static/bootstrap_plugins/summernote';
    		this.value = opts.value;
    		this.href = opts.href;
    		load_css (this.base_path + '/summernote.css');
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				var editor = jQuery (self.summernote);
    				var rect = self.summernote.getBoundingClientRect ();
    				self.summernote.style.position = 'absolute';
    				self.summernote.style.top = (rect.top + 2) + 'px';
    				self.summernote.style.right = '5px';
    				self.summernote.style.bottom = '5px';
    				self.summernote.style.left = '5px';
    				editor.html (atob (self.value));
    				editor.summernote ();
    				self.editor = editor;
    			};
    			load_js (self.base_path + '/summernote.min.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		var on_save = function (e) {
    			if (this.href) {
    				var ajax_options = dict ([[method, 'POST'], [url, this.href], [dataType, 'html'], [data, dict ([[data, self.editor.summernote ('code')]])]]);
    				var _on_ajax = function () {
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
    
    
</summernote>