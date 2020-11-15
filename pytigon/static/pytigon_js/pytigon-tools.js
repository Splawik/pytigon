PYTHON_URL = "http://127.0.0.1:8000/";

PSEUDO_IP = "127.0.0.2";
PYTHON_IP = "127.0.0.4";

PYTHON_PACKAGES = [
  "channels",
  "daphne",
  "pytigon-lib",
  "pytigon",
  "micropip",
  "requests",
  "urllib3",
  "fs",
  "django-select2",
  "bootstrap4",
  "django-allauth",
  "Django",
  "Twisted",
  "django-appconf",
  "fpdf",
  "Transcrypt",
  "django-bootstrap4",
  "django-bootstrap4-form",
  "typed_ast",
  "mypy",
  "python_version",
  "django-js-asset",
  "django-cache-url",
  "whitenoise",
  "certifi",
  "idna",
  "setuptools",
  "sqlparse",
  "asgiref",
  "chardet",
  "django-cors-headers",
  "incremental",
  "python-dateutil",
  "markdown2",
  "polib",
  "pytz",
];

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
  "import pytigon_lib.schtools.main_paths",
  "paths = pytigon_lib.schtools.main_paths.get_main_paths()",
  "sys.path.append(paths['ROOT_PATH'])",
  "os.mkdir(paths['DATA_PATH'])",
  "import pytigon.pytigon_request",
  "pytigon.pytigon_request.init('schdevtools', 'auto', 'anawa')",
  "ret = pytigon.pytigon_request.request('/schdevtools/')",
  "REQUEST = '' ",
].join("\n");

var INLINE_DIALOG_UPDATE_HTML =
  "\
<div style='position:relative'>\
    <div class='dark_background'></div>\
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%;'>\
        <div class='modal-content'>\
            <div class='modal-header'>\
                <h4 class='modal-title'>Modal title</h4>\
                <button type='button' class='btn btn-outline-secondary minimize' data-dismiss='modal' onclick='popup_minimize(this)' style='diplay:none;'> \
                    <span class='fa fa-window-minimize'></span> \
                </button> \
                <button type='button' class='btn btn-outline-secondary maximize' data-dismiss='modal' onclick='popup_maximize(this)'> \
                    <span class='fa fa-window-maximize'></span> \
                </button> \
                <button type='button' class='close btn-raised' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            </div>\
            <div class='modal-body inline-update-modal-body'>\
                <div class='refr_target dialog-data-inner'></div>\
            </div>\
            <div class='modal-footer'>\
                <button type='button' class='btn btn-secondary' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
                <button type='button' class='btn btn-primary' onclick=\"javascript:on_edit_ok($(this).parent().parent().find('form:first'));return false;\">OK</button>\
            </div>\
        </div>\
    </div>\
</div>\
";

var INLINE_TABLE_HTML =
  "\
<div style='position:relative' style='height:100vh'>\
    <div class='dark_background'></div>\
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%; height:100%'>\
        <div class='modal-content' style='height:100%'>\
            <div class='modal-header'>\
                <h4 class='modal-title'>{{title}}</h4>\
                <button type='button' class='btn btn-outline-secondary minimize' data-dismiss='modal' onclick='popup_minimize(this)' style='diplay:none;'> \
                    <span class='fa fa-window-minimize'></span> \
                </button> \
                <button type='button' class='btn btn-outline-secondary maximize' data-dismiss='modal' onclick='popup_maximize(this)'> \
                    <span class='fa fa-window-maximize'></span> \
                </button> \
                <button type='button' class='close btn-raised' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            </div>\
            <div class='modal-body inline-table-modal-body'>\
                <div class='refr_target dialog-data-inner'></div>\
            </div>\
        </div>\
    </div>\
</div>\
";

var ABSOLUTE_HTML =
  "\
<div style='position:absolute; z-index:99; height:500px'>\
    <div class='dark_background'></div>\
    <div class='modal-dialog modal-dialog-inline' role='document' style='max-width: 100%; height: 100%;'>\
        <div class='modal-content' style='height:100%;'>\
            <div class='modal-header'>\
                <h4 class='modal-title'>{{title}}</h4>\
                <button type='button' class='btn btn-outline-secondary minimize' data-dismiss='modal' onclick='popup_minimize(this)' style='diplay:none;'> \
                    <span class='fa fa-window-minimize'></span> \
                </button> \
                <button type='button' class='btn btn-outline-secondary maximize' data-dismiss='modal' onclick='popup_maximize(this)'> \
                    <span class='fa fa-window-maximize'></span> \
                </button> \
                <button type='button' class='close btn-raised' data-dismiss='modal' aria-label='Close' onclick='on_cancel_inline($(this));return false'><span aria-hidden='true'>&times;</span></button>\
            </div>\
            <div class='modal-body inline-table-modal-body'>\
                <div class='refr_target dialog-data-inner'></div>\
            </div>\
        </div>\
    </div>\
</div>\
";

var INLINE_DIALOG_DELETE_HTML =
  "\
<div class='panel panel-default alert alert-danger'>\
    <div class='panel-body'>\
        <div class='refr_target dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
        <button type='button' class='btn btn-primary' onclick='on_delete_ok($(this));return false'>OK</button>\
    </div>\
</div>\
";

var INLINE_DIALOG_INFO_HTML =
  "\
<div class='panel panel-default'>\
    <div class='panel-body'>\
        <div class='refr_target dialog-data-inner'></div>\
    </div>\
    <div class='panel-footer'>\
        <button type='button' class='btn btn-default' onclick='on_cancel_inline($(this));return false'>Cancel</button>\
    </div>\
</div>\
";

var INLINE_FRAME_HTML =
  "\
<div>\
        <div class='frame-data-inner'></div>\
</div>\
";

var PYTHON_REQUEST = [
  "import pytigon.pytigon_request",
  "RET = pytigon.pytigon_request.request('/schdevtools/').str()",
].join("\n");

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
    languagePluginLoader.then(function () {
      var packages = [];
      var p;
      pyodide._module.packages.dependencies["Pillow"] = [];
      pyodide._module.packages.dependencies["channels"] = [];
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

/*
(function () {
  var oldXMLHttpRequest = XMLHttpRequest;
  modXMLHttpRequest = function () {
    var actual = new oldXMLHttpRequest();
    var self = this;

    this.onreadystatechange = null;
    this.onload = null;
    this._readyState = 0;
    this._responseText = "";
    this._status = 0;
    this.sch_local_request = false;
    this.url = null;

    actual.onreadystatechange = function () {
      if (self.onreadystatechange != null) return self.onreadystatechange();
    };

    actual.onload = function () {
      if (self.onload != null) return self.onload();
    };

    this.open = function (
      sMethod,
      sUrl,
      bAsync = true,
      sUser = null,
      sPassword = null
    ) {
      self.url = sUrl;
      if (self.url.includes(PYTHON_IP) || self.url.includes(PSEUDO_IP)) {
        self.sch_local_request = true;
        return true;
      }
      return actual.open(sMethod, sUrl, bAsync, sUser, sPassword);
    };

    this.send = function (vData) {
      if (this.sch_local_request && self.url.includes(PSEUDO_IP)) {
        var data = {};

        function _on_response(txt, py_callback) {
          self.readyState = 4;
          if (self.responseType == "arraybuffer") {
            self.response = str2ab(txt);
          } else {
            self.responseText = txt;
          }
          self.status = 200;
          if (self.onreadystatechange != null) self.onreadystatechange();
          if (self.onload != null) self.onload();
          return;
        }

        if (vData) {
          py_function(["post", self.url, vData], _on_response);
        } else {
          py_function(["get", self.url, null]);
        }

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
        return actual.send(vData);
      }
    };

    this.setRequestHeader = function (key, value) {
      //if(this.sch_local_request) return;
      if (self.url.includes(PYTHON_IP) || self.url.includes(PSEUDO_IP)) return;
      return actual.setRequestHeader(key, value);
    };

    ["statusText", "responseType", "response", "responseXML", "upload"].forEach(
      function (item) {
        Object.defineProperty(self, item, {
          get: function () {
            return actual[item];
          },
          set: function (val) {
            actual[item] = val;
          },
        });
      }
    );

    ["readyState", "responseText", "status"].forEach(function (item) {
      Object.defineProperty(self, item, {
        get: function () {
          if (self["_" + item]) return self["_" + item];
          else return actual[item];
        },
        set: function (val) {
          self["_" + item] = val;
        },
      });
    });

    //["readyState", "responseText", "status"].forEach(function (item) {
    //    Object.defineProperty(self, item, {
    //        get: function () { if (self["_" + item]) return self["_" + item]; else return actual[item]; },
    //        set: function (val) { self["_" + item] = val; }
    //    });
    //});

    [
      "ontimeout",
      "timeout",
      "withCredentials",
      "onerror",
      "onprogress",
    ].forEach(function (item) {
      Object.defineProperty(self, item, {
        get: function () {
          return actual[item];
        },
        set: function (val) {
          actual[item] = val;
        },
      });
    });

    [
      "addEventListener",
      "abort",
      "getAllResponseHeaders",
      "getResponseHeader",
      "overrideMimeType",
    ].forEach(function (item) {
      Object.defineProperty(self, item, {
        value: function () {
          return actual[item].apply(actual, arguments);
        },
      });
    });
  };
  window.XMLHttpRequest = modXMLHttpRequest;
})();
*/

function import_module(html_txt) {
  var encodedJs = encodeURIComponent(html_txt);
  var dataUri = "data:text/javascript;charset=utf-8," + encodedJs;
  try {
    require(dataUri);
  } catch (err) {
    console.log("Dynamic import is not supported");
  }
}

window.import_module = import_module;

function jsimp(module) {
  return require(module);
}

window.jsimp = jsimp;

function define_custom_element(tag, shadow, options) {
  class ProxyHTMLElement extends HTMLElement {
    static get observedAttributes() {
      if ("attributes" in options) {
        return Object.keys(options["attributes"]);
      } else return [];
    }

    constructor() {
      super();
      this.state = {};
      this.options = options;
      this.root = null;
      this.attribute_actions_queue = [];
      if ("global_state_actions" in options) {
        this.global_state_actions = options["global_state_actions"];
      } else this.global_state_actions = {};
      if ("constructor" in options) options["constructor"](this);
      if (shadow) {
        const shadowRoot = this.attachShadow({ mode: "open" });
        if ("template" in options) {
          shadowRoot.innerHTML = options["template"];
          this.root = shadowRoot;
        }
        if (this.state) {
          let state = this.state;
          this.state = {};
          this.set_state(state);
        }
        if ("init" in options) options["init"](this);
        this.attributes_init();
      }
      if (this.global_state_actions) {
        window.GLOBAL_BUS.register(this);
      }
    }

    attributes_init() {
      if (this.attribute_actions_queue) {
        let component = this;
        this.attribute_actions_queue.forEach(function (item, index) {
          component.attributeChangedCallback(item[0], item[1], item[2]);
        });
        this.attribute_actions_queue = [];
      }
    }

    set_state(state) {
      if ("set_state" in options) {
        options["set_state"](this, state);
      }
    }

    set_external_state(state) {
      if (this.global_state_actions) {
        let component = this;
        Object.keys(state).forEach(function (key) {
          if (key in component.global_state_actions) {
            component.global_state_actions[key](component, state[key]);
          }
        });
      }
    }

    connectedCallback() {
      if (!shadow) {
        if ("template" in options) this.innerHTML = options["template"];
        this.root = this;
        if (this.state) {
          let state = this.state;
          this.state = {};
          this.set_state(state);
        }
        if ("init" in options) options["init"](this);
        this.attributes_init();
      }
      if ("connectedCallback" in options) {
        options["connectedCallback"](this);
      }
    }

    disconnectedCallback() {
      if ("disconnectedCallback" in options) {
        options["disconnectedCallback"](this);
      }
      if (this.global_state_actions) {
        window.GLOBAL_BUS.unregister(this);
      }
    }

    attributeChangedCallback(name, oldVal, newVal) {
      if (!this.root) {
        this.attribute_actions_queue.push([name, oldVal, newVal]);
        return;
      }
      if ("attributeChangedCallback" in options) {
        options["attributeChangedCallback"](this, name, oldVal, newVal);
      } else {
        if ("attributes" in options) {
          if (options["attributes"][name])
            options["attributes"][name](this, oldVal, newVal);
          else this.set_state({ [name]: newVal });
        }
      }
    }
  }
  customElements.define(tag, ProxyHTMLElement);
}

window.define_custom_element = define_custom_element;
