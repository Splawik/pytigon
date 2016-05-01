<video-js>
    <video name="videodiv" class="video-js vjs-default-skin" controls preload="auto" width={ opts.width } height={ opts.height }>
            <source src={ opts.src } type={ opts.type }></source>
            <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
    </video>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins/video-js";
    jQuery(self.videodiv).on("contextmenu", (function() {
        var ρσ_anonfunc = function (e) {
            e.preventDefault();
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["e"]}
        });
        return ρσ_anonfunc;
    })());
    load_css(this.base_path + "/video-js.min.css");
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/video.min.js", function () {
            var player;
            videojs.options.flash.swf = "video-js.swf";
            player = videojs(self.videodiv, {}, function () {
            });
            self.player = player;
        });
    });</script>
    
    
</video-js>