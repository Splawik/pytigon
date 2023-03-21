var BASE_PATH, TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "ptig-video";
TEMPLATE = '        <video name=\"videodiv\" class=\"video-js vjs-default-skin\" controls preload=\"auto\" data-bind=\"style-width:width;style-height:height\">\n' +
    '                <source data-bind=\"attr-src:src;attr-type:type\">\n' +
    '                        <p class=\"vjs-no-js\">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href=\"http://videojs.com/html5-video-support/\" target=\"_blank\">supports HTML5 video</a></p></p>\n' +
    '                </source>\n' +
    '        </video>\n' +
    '\n' +
    '';
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins/video-js";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/video.min.js"], [BASE_PATH + "/video-js.min.css"]));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({width: null, height: null, src: null, type: null});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var _on_video, div;
        div = component.root.querySelector("video");
        videojs.options.flash.swf = "video-js.swf";
        _on_video = (function flx__on_video () {
            return null;
        }).bind(this);

        component.player = videojs(div, ({}), _on_video);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}