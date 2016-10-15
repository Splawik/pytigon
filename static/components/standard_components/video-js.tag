<video-js>
    <video name="videodiv" class="video-js vjs-default-skin" controls preload="auto" width={ opts.width } height={ opts.height }>
            <source src={ opts.src } type={ opts.type }></source>
            <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
    </video>
    <script>
    
    		var __symbols__ = ['__esv5__'];
    		this.base_path = BASE_PATH + 'static/vanillajs_plugins/video-js';
    		var _on_contextmenu = function (e) {
    			e.preventDefault ();
    		};
    		jQuery (self.videodiv).on ('contextmenu', _on_contextmenu);
    		load_css (this.base_path + '/video-js.min.css');
    		var _on_mount = function () {
    			var self = this;
    			var _on_loadjs = function () {
    				videojs.options.flash.swf = 'video-js.swf';
    				var _on_video = function () {
    					// pass;
    				};
    				var player = videojs (self.videodiv, dict ({}), _on_video);
    				self.player = player;
    			};
    			load_js (self.base_path + '/video.min.js', _on_loadjs);
    		};
    		this.on ('mount', _on_mount);
    		__pragma__ ('<all>')
    			__all__._on_contextmenu = _on_contextmenu;
    			__all__._on_mount = _on_mount;
    		__pragma__ ('</all>')
    	</script>
    
    
</video-js>