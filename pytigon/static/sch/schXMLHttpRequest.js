PYTHON_URL = "http://127.0.0.1:8000/";

PSEUDO_IP = '127.0.0.2'
PYTHON_IP = '127.0.0.4';

PYTHON_PACKAGES = ['channels', 'daphne', 'pytigon-lib', 'pytigon', 'micropip',
    'requests', 'urllib3', 'fs', 'django-select2', 'bootstrap4',
    'django-allauth', 'Django', 'Twisted', 'django-appconf', 'fpdf', 'Transcrypt',
    'django-bootstrap4', 'django-bootstrap4-form', 'typed_ast', 'mypy',
    "python_version", "django-js-asset", "django-cache-url", "whitenoise", "certifi", "idna", "setuptools", "sqlparse", "asgiref", "chardet", "django-cors-headers",
    "incremental", "python-dateutil", "markdown2", "polib", "pytz"
]

var PYTHON_INIT = [
    "import sys",
    "import django",
    "import micropip",
    "import os",
    "import django",
    "import pytigon",
    "import platform",
    "import sys",
    "import django.contrib.staticfiles.views",
    "import pytigon.schserw.main_paths",
    "paths = pytigon.schserw.main_paths.get_main_paths()",
    "sys.path.append(paths['ROOT_PATH'])",
    "os.mkdir(paths['DATA_PATH'])",
    "import pytigon.pytigon_request",
    "pytigon.pytigon_request.init('schdevtools', 'auto', 'anawa')",
    "ret = pytigon.pytigon_request.request('/schdevtools/')",
    "REQUEST = '' "
].join('\n');


var PYTHON_REQUEST = [
    "import pytigon.pytigon_request",
    "RET = pytigon.pytigon_request.request('/schdevtools/').str()"
].join('\n');



function request() {
    pyodide.globals.REQUEST = "hello world";
    pyodide.runPython(PYTHON_REQUEST);
    ret = pyodide.globals.RET;
    return ret;
}


var ACTIONS = {};
var ACTION_ID = 0;


function set_action_data(data) {
    ACTION_ID += 1;
    ACTIONS[id] = data;
    return ACTION_ID;
}

function get_action_data(id) {
    if (id in ACTIONS) {
        return ACTIONS[id];
    } else {
        return null;
    }
}

function delete_action_data(id) {
    if (id in ACTIONS) {
        delete ACTIONS[id];
        return true;
    } else {
        return false;
    }
}

function str2ab(str) {
    var buf = new ArrayBuffer(str.length * 2); // 2 bytes for each char
    var bufView = new Uint16Array(buf);
    for (var i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}


function init_python() {
    return new Promise((resolve, reject) => {
        window.languagePluginUrl = PYTHON_URL;
        languagePluginLoader.then(() => {
            var packages = [];
            var p;
            pyodide._module.packages.dependencies['Pillow'] = [];
            pyodide._module.packages.dependencies['channels'] = [];
            for (p of PYTHON_PACKAGES) {
                packages.push(PYTHON_URL + p + ".js");
            }
            console.log(packages);
            pyodide.loadPackage(packages).then(() => {
                pyodide.runPython(PYTHON_INIT);
                resolve("");
            });
        });
    });
}


(function() {
    var oldXMLHttpRequest = XMLHttpRequest;
    modXMLHttpRequest = function() {
        var actual = new oldXMLHttpRequest();
        var self = this;

        this.onreadystatechange = null;
        this.onload = null;
        this._readyState = 0;
        this._responseText = "";
        this._status = 0;
        this.sch_local_request = false;
        this.url = null;

        actual.onreadystatechange = function() {
            if (self.onreadystatechange != null) return self.onreadystatechange();
        };

        actual.onload = function() {
            if (self.onload != null) return self.onload();
        }

        this.open = function(sMethod, sUrl, bAsync, sUser, sPassword) {
            self.url = sUrl;
            if (self.url.includes(PYTHON_IP) || self.url.includes(PSEUDO_IP)) {
                self.sch_local_request = true;
                return true;
            }
            return actual.open(sMethod, sUrl, bAsync, sUser, sPassword);
        };

        this.send = function(vData) {
            if (this.sch_local_request && self.url.includes(PSEUDO_IP)) {
                var data = {}

                function _on_response(txt) {
                    self.readyState = 4;
                    if (self.responseType == 'arraybuffer') {
                        self.response = str2ab(txt);
                    } else {
                        self.responseText = txt;
                    }
                    self.status = 200;
                    if (self.onreadystatechange != null) self.onreadystatechange();
                    if (self.onload != null) self.onload();
                    return;
                }
                data['callback'] = _on_response;
                if (vData) {
                    data['action'] = 'post';
                    data['data'] = vData;
                } else {
                    data['action'] = 'get';
                    data['data'] = null;
                }
                id = set_action_data(data);
                var xhr = new XMLHttpRequest();
                xhr.open('GET', "http://127.0.0.2/?:action??" + id);
                try {
                    xhr.send();
                } catch (e) {}
            } else if (this.sch_local_request && self.url.includes(PYTHON_IP)) {
                self.readyState = 4;
                self.responseText = request();
                self.response = self.responseText;
                console.log(self.responseText);
                self.status = 200;
                if (self.onreadystatechange != null) self.onreadystatechange();
                if (self.onload != null) self.onload();
                return null;
            } else {
                return actual.send(vData)
            }
        };

        this.setRequestHeader = function(key, value) {
            //if(this.sch_local_request) return;
            if (self.url.includes(PYTHON_IP) || self.url.includes(PSEUDO_IP)) return;
            return actual.setRequestHeader(key, value);
        };

        ["statusText", "responseType", "response",
            "responseXML", "upload"
        ].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() { return actual[item]; },
                set: function(val) { actual[item] = val; }
            });
        });

        ["readyState", "responseText", "status"].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() {
                    if (self["_" + item]) return self["_" + item];
                    else return actual[item];
                },
                set: function(val) { self["_" + item] = val; }
            });
        });

        //["readyState", "responseText", "status"].forEach(function (item) {
        //    Object.defineProperty(self, item, {
        //        get: function () { if (self["_" + item]) return self["_" + item]; else return actual[item]; },
        //        set: function (val) { self["_" + item] = val; }
        //    });
        //});

        ["ontimeout", "timeout", "withCredentials", "onerror", "onprogress"].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() { return actual[item]; },
                set: function(val) { actual[item] = val; }
            });
        });

        ["addEventListener", "abort", "getAllResponseHeaders",
            "getResponseHeader", "overrideMimeType"
        ].forEach(function(item) {
            Object.defineProperty(self, item, {
                value: function() { return actual[item].apply(actual, arguments); }
            });
        });

    }
    window.XMLHttpRequest = modXMLHttpRequest;
})();


function import_module(html_txt) {
    var encodedJs = encodeURIComponent(html_txt);
    var dataUri = 'data:text/javascript;charset=utf-8,' + encodedJs;
    import(dataUri);
}

window.import_module = import_module;

