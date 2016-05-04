<plotly>
    <div name="plotlydiv" style="width:{ opts.width };height:{ opts.height };" modebar="false"></div>
    <script>
    
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins';
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				var data = list ([dict ({'values': list ([19, 26, 55]), 'labels': list (['Residential', 'Non-Residential', 'Utility']), 'type': 'pie'})]);
    				var layout = dict ({'height': 400, 'width': 500});
    				var plot = Plotly.newPlot (self.plotlydiv, data, layout, dict ({'displayModeBar': true, 'showLink': false, 'displaylogo': false, 'scrollZoom': true, 'modeBarButtonsToRemove': list (['sendDataToCloud'])}));
    				self.plot = plot;
    			};
    			load_js (self.base_path + '/plotly-latest.min.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</plotly>