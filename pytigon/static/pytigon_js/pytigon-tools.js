var PSEUDO_IP = "127.0.0.2";
var PYODIDE = null;

var PYODIDE_ROUTER = []

function set_pyodide_paths(paths) {
  PYODIDE_ROUTER = paths;
}

function pyodide_url(url) {
  let url2 = url.split('?')[0]
  for (path of PYODIDE_ROUTER) {
    if (path.endsWith('*')) {
      if (url2.startsWith(path.slice(0, -1))) {
        return true;
      }
    } else {
      if (path === url2) {
        return true;
      }
    }
  }
  return false;
}

var PYTHON_PACKAGES = [
  "pytigon",
];

var PYTHON_INIT = `
import micropip
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
await micropip.install("pyquery")
try:
    import pytigon_lib
except:
    await micropip.install("pytigon")

from pytigon.pytigon_request import init, request
import js
from asgiref.sync import sync_to_async

def _init():
    init("$PRJ_NAME", "$USER", "$PASSWORD")

ret = await sync_to_async(_init)()

def _request(url):
    ret = request(url)
    return ret

async def http_get(url):
    ret = await sync_to_async(_request)(url)
    return ret.str()
`

function pyodide_app_init(prj_name, base_url, url, application_template, language, user, password, callback) {
  let pyodide = null;
  async function main() {
    pyodide = await loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
    });
    pyodide.FS.rename("/lib/python3.9/site-packages/pyodide", "/lib/python3.9/pyodide")
    pyodide.FS.rename("/lib/python3.9/site-packages/_pyodide", "/lib/python3.9/_pyodide")
    pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, '/home/web_user');
    pyodide.FS.mkdir('/lib/python3.9/site-packages/micropip')
    pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, '/lib/python3.9/site-packages');
    pyodide.FS.syncfs(true, async function(err) {
      let save = false;
      let example_dir = pyodide.FS.analyzePath("/lib/python3.9/site-packages/micropip", true)
      if(!example_dir.exists) {
          save = true;
      }
      await pyodide.loadPackage("packaging");
      await pyodide.loadPackage("pyparsing");
      await pyodide.loadPackage("pytz");
      await pyodide.loadPackage("setuptools");
      await pyodide.loadPackage("six");
      await pyodide.loadPackage("micropip");

      await pyodide.runPythonAsync(PYTHON_INIT.replaceAll('$PRJ_NAME', prj_name).replaceAll("$BASE_URL", base_url).replaceAll('$USER', user).replaceAll('$PASSWORD', password));
      PYODIDE = pyodide
      response = await fetch(url);
      if(save) {
          PYODIDE.FS.syncfs(false, function(err) {
            console.log("File system saved")
          });
      }
      await callback(response);
    });
  }
  main();
}

window.pyodide_app_init = pyodide_app_init

async function get_response(url) {
  return await PYODIDE.globals.get("http_get")(url);
}

const constantMock = window.fetch;

window.fetch = async function() {
  console.log("FETCH: " + arguments[0])
  console.log(arguments)
  if (pyodide_url(arguments[0])) {
    ret = new Response(
      await get_response(arguments[0]), {
        headers: {
          "Content-Type": "text/html"
        },
      }
    )
  } else {
    ret = constantMock.apply(this, arguments)
  }
  return ret
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
    };

    this.open = function(
      sMethod,
      sUrl,
      bAsync = true,
      sUser = null,
      sPassword = null
    ) {
      console.log("XMLREQUEST: " + sUrl);
      self.url = sUrl;
      if (self.url.includes(PSEUDO_IP) || pyodide_url(self.url)) {
        self.sch_local_request = true;
        return true;
      }
      return actual.open(sMethod, sUrl, bAsync, sUser, sPassword);
    };

    this.send = async function(vData) {
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
      } else if (this.sch_local_request && pyodide_url(self.url)) {
        self.readyState = 4;
        self.responseText = await get_response(self.url);
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

    this.setRequestHeader = function(key, value) {
      if (this.sch_local_request) return;
      //if (pyodide_url(self.url) || self.url.includes(PSEUDO_IP)) return;
      return actual.setRequestHeader(key, value);
    };

    ["statusText", "responseType", "response", "responseXML", "upload"].forEach(
      function(item) {
        Object.defineProperty(self, item, {
          get: function() {
            return actual[item];
          },
          set: function(val) {
            actual[item] = val;
          },
        });
      }
    );

    ["readyState", "responseText", "status"].forEach(function(item) {
      Object.defineProperty(self, item, {
        get: function() {
          if (self["_" + item]) return self["_" + item];
          else return actual[item];
        },
        set: function(val) {
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
    ].forEach(function(item) {
      Object.defineProperty(self, item, {
        get: function() {
          return actual[item];
        },
        set: function(val) {
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
    ].forEach(function(item) {
      Object.defineProperty(self, item, {
        value: function() {
          return actual[item].apply(actual, arguments);
        },
      });
    });
  };
  window.XMLHttpRequest = modXMLHttpRequest;
})();

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
        const shadowRoot = this.attachShadow({
          mode: "open"
        });
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
        this.attribute_actions_queue.forEach(function(item, index) {
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
        Object.keys(state).forEach(function(key) {
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
          else this.set_state({
            [name]: newVal
          });
        }
      }
    }
  }
  customElements.define(tag, ProxyHTMLElement);
}

window.define_custom_element = define_custom_element;

function syncfs() {
  return new Promise(resolve => {
    PYODIDE.FS.syncfs(false, function(err) {
      resolve(err)
    });
  });
}

async function sync_on_unload() {
  await syncfs();
}

function onbeforeunload_sync() {
  if(PYODIDE) {
    sync_on_unload()
   }
}

window.onbeforeunload = onbeforeunload_sync;
