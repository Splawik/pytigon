var TAG, TEMPLATE, comp, init, stub1_context, stub2_err;
TAG = "tele-room";
TEMPLATE = '<div class=\"container\">\n' +
    '        <div class=\"row\">\n' +
    '                <div class=\"col-md-12 my-3\">\n' +
    '                        <h2>Room</h2>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '        <div class=\"row\">\n' +
    '                <div class=\"col-md-12\">\n' +
    '                        <div class=\"f\">\n' +
    '                                <ptig-webrtc ref=\"webrtc\" width=\"100%\" data-bind=\":roomId;:src;:host\"></ptig-webrtc>\n' +
    '                        </div>\n' +
    '                </div>\n' +
    '        </div>\n' +
    '</div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, true));
comp = stub1_context.__enter__();
try {
    comp.options["attributes"] = ({roomId: null, host: null});
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        component.set_state(({src: window.BASE_PATH + "teleconference/teleconference/channel/"}));
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}