var __name__ = '__main__';
var _xterm = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/xterm';
	var _on_loadjs = function () {
		var props = list (['width', 'height', 'x', 'y', 'href']);
		var template = "<div class = 'call_on_remove' name='xterm' v-bind:style='{ width: width, height: height}' ></div>";
		Terminal.applyAddon (fit);
		var mounted = function () {
			var self = this;
			var _next = function () {
				var address = location.hostname;
				if (location.port) {
					address += ':' + location.port;
				}
				address += self.href;
				if (location.protocol != 'https:') {
					var address = 'ws://' + address;
				}
				else {
					var address = 'wss://' + address;
				}
				var websocket = new WebSocket (address);
				var term = new Terminal ();
				term.open (self.$el);
				term.setOption ('fontFamily', 'monospace');
				term.setOption ('fontSize', 14);
				term.setOption ('lineHeight', 1.1);
				self.term = term;
				var on_remove = function () {
					var _on_close = function () {
						websocket = null;
						term.dispose ();
						term = null;
					};
					websocket.onclose = _on_close;
					if (websocket) {
						websocket.close ();
						websocket = null;
					}
				};
				self.$el.on_remove = on_remove;
				var _on_websocket_open = function () {
					var _fit_to_screen = function () {
						term.fit ();
						var s = JSON.stringify (dict ({'resize': dict ({'cols': term.cols, 'rows': term.rows})}));
						websocket.send (s);
					};
					var _on_key = function (key, ev) {
						var txt = JSON.stringify (dict ({'input': key}));
						websocket.send (txt);
					};
					var _on_message = function (evt) {
						term.write (evt.data);
					};
					term.on ('key', _on_key);
					websocket.onmessage = _on_message;
					jQuery (window).resize (_fit_to_screen);
					_fit_to_screen ();
					if (window.hasOwnProperty ('MOUNTED_COMPONENTS')) {
						window.MOUNTED_COMPONENTS++;
					}
				};
				websocket.onopen = _on_websocket_open;
			};
			Vue.nextTick (_next);
		};
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
	};
	load_many_js ((((base_path + '/xterm.js') + ';') + base_path) + '/fit.js', _on_loadjs);
	load_css (base_path + '/xterm.css');
};
Vue.component ('sch-xterm', _xterm);
