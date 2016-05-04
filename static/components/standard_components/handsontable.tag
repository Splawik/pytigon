<handsontable>
    <div name="handsontablediv"></div>
    <script>
    
    		this.base_path = BASE_PATH + 'static/jquery_plugins';
    		load_css (this.base_path + '/handsontable.full.css');
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				var data = list ([list (['Column A', 'Column B', 'Column C']), list (['1', '2', '3'])]);
    				var htable = __new_window.Handsontable (self.handsontablediv, dict ({'data': data}));
    				self.htable = htable;
    			};
    			load_js (self.base_path + '/handsontable.full.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</handsontable>