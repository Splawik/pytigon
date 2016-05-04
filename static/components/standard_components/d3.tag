<d3>
    <div name="d3div" style="width:{ opts.width };height:{ opts.height };"></div>
    <script>
    
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins';
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				var sampleSVG = d3.select (self.d3div).append ('svg').attr ('width', 100).attr ('height', 100);
    				var _on_mouseover = function () {
    					d3.select (this).style ('fill', 'aliceblue');
    				};
    				var _on_mouseout = function () {
    					d3.select (this).style ('fill', 'white');
    				};
    				sampleSVG.append ('circle').style ('stroke', 'gray').style ('fill', 'white').attr ('r', 40).attr ('cx', 50).attr ('cy', 50).on ('mouseover', _on_mouseover).on ('mouseout', _on_mouseout);
    			};
    			load_js (self.base_path + '/plotly-latest.min.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</d3>