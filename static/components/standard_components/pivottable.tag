<pivottable>
    <div name="pivottablediv"></div>
    <script>
    
    		this.base_path = BASE_PATH + 'static/jquery_plugins/pivottable';
    		load_css (this.base_path + '/pivot.css');
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				var _on_loadjs2 = function () {
    					var data = list ([dict ({'color': 'blue', 'shape': 'circle'}), dict ({'color': 'red', 'shape': 'triangle'})]);
    					var options = dict ({'rows': list (['color']), 'cols': list (['shape'])});
    					var pivottable = jQuery (self.pivottablediv).pivotUI (data, options);
    					self.pivottable = pivottable;
    				};
    				load_js (self.base_path + '/../jquery.ui/jquery-ui.min.js', _on_loadjs2);
    			};
    			load_js (self.base_path + '/pivot.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</pivottable>