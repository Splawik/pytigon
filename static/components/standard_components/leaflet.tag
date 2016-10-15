<leaflet>
    <div name="mapdiv" style="width: { opts.width }; height: { opts.height };"></div>
    <script>
    
    		var __symbols__ = ['__esv5__'];
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins/leaflet';
    		load_css (this.base_path + '/leaflet.css');
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				L.Icon.Default.imagePath = self.base_path + '/images';
    				var mapobj = L.map (self.mapdiv).setView (list ([51.613007, 21.491859]), 13);
    				L.tileLayer ('http://{s}.tile.osm.org/{z}/{x}/{y}.png', dict ({'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'})).addTo (mapobj);
    				var maker = L.marker (list ([51.613007, 21.491859]));
    				maker.addTo (mapobj);
    				maker.bindPopup ('<b>Hello world!</b><br />I am a popup.');
    				maker.openPopup ();
    				self.mapobj = mapobj;
    			};
    			load_js (self.base_path + '/leaflet.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</leaflet>