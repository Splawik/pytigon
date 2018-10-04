var __name__ = '__main__';
var _xterm = function (resolve, reject) {
	var base_path = window.BASE_PATH + 'static/vanillajs_plugins/xterm';
	var _on_loadjs = function () {
		var props = list (['width', 'height', 'x', 'y', 'href']);
		var template = "<div name='xterm' v-bind:style='{ width: width, height: height}' ></div>";
		Terminal.applyAddon (fit);
		var mounted = function () {
			var address = this.href;
			var websocket = new WebSocket (address);
			var term = new Terminal ();
			term.open (this.$el);
			term.setOption ('fontFamily', 'monospace');
			term.setOption ('fontSize', 14);
			term.setOption ('lineHeight', 1.1);
			this.term = term;
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
			};
			websocket.onopen = _on_websocket_open;
		};
		resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
	};
	load_many_js ((((base_path + '/xterm.js') + ';') + base_path) + '/fit.js', _on_loadjs);
	load_css (base_path + '/xterm.css');
};
Vue.component ('sch-xterm', _xterm);
