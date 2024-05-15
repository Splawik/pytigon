var GLOBAL_TIMER, _on_time;
_on_time = function flx__on_time () {
    var d;
    d = new Date();
    GLOBAL_BUS.emit("time_str", _pymeth_replace.call(d.toISOString(), "T", " ").slice(0,19));
    return null;
};

GLOBAL_TIMER = setInterval(_on_time, 1000);