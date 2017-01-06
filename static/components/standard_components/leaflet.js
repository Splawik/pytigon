
		var _marker = dict ({'props': list (['x', 'y', 'txt']), 'template': ''});
		Vue.component ('sch-marker', _marker);
		var _leaflet = function (resolve, reject) {
			var base_path = window.BASE_PATH + 'static/vanillajs_plugins/leaflet';
			var _on_loadjs = function () {
				var props = list (['width', 'height', 'x', 'y']);
				var template = "<div name='mapdiv' v-bind:style='{ width: width, height: height}' ></div>";
				var mounted = function () {
					L.Icon.Default.imagePath = base_path + '/images';
					var mapobj = L.map (this.$el).setView (list ([this.x, this.y]), 13);
					L.tileLayer ('http://{s}.tile.osm.org/{z}/{x}/{y}.png', dict ({'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'})).addTo (mapobj);
					var _process_slot = function (slot) {
						if (slot.tag == 'sch-maker') {
							var maker = L.marker (list ([slot.data.attrs.x, slot.data.attrs.y]));
							maker.addTo (mapobj);
							maker.bindPopup (slot.data.attrs.txt);
							maker.openPopup ();
						}
					};
					this.$slots.default.forEach (_process_slot);
					this.mapobj = mapobj;
				};
				resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
			};
			load_js (base_path + '/leaflet.js', _on_loadjs);
			load_css (base_path + '/leaflet.css');
		};
		Vue.component ('sch-leaflet', _leaflet);
		__pragma__ ('<all>')
			__all__._leaflet = _leaflet;
			__all__._marker = _marker;
		__pragma__ ('</all>')
	