
		var _video = function (resolve, reject) {
			var base_path = window.BASE_PATH + 'static/vanillajs_plugins/video-js';
			var _on_loadjs = function () {
				var props = list (['width', 'height', 'src', 'type']);
				var template = '\n            <video name=\'videodiv\' class=\'video-js vjs-default-skin\' controls preload=\'auto\' v-bind:style=\'{ width: width, height: height}\'>\n                <source v-bind:src=this.src v-bind:type=this.type />\n                <p class=\'vjs-no-js\'>To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>\n            </video>\n        ';
				var mounted = function () {
					videojs.options.flash.swf = 'video-js.swf';
					var _on_video = function () {
						// pass;
					};
					var player = videojs (this.$el, dict ({}), _on_video);
					this.player = player;
				};
				resolve (dict ({'props': props, 'template': template, 'mounted': mounted}));
			};
			load_js (base_path + '/video.min.js', _on_loadjs);
			load_css (base_path + '/video-js.min.css');
		};
		Vue.component ('sch-video', _video);
		__pragma__ ('<all>')
			__all__._video = _video;
		__pragma__ ('</all>')
	