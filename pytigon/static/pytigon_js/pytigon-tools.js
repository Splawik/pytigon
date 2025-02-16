var PSEUDO_IP = '127.0.0.2'
var PYWEBVIEW_IP = '127.0.0.5'
var PYODIDE = null

var PYODIDE_ROUTER = []

function set_pyodide_paths (paths) {
  PYODIDE_ROUTER = paths
}

function pyodide_url (url) {
  let url2 = url.split('?')[0]
  if (
    (url2.endsWith('.db') || url2.endsWith('sw.js')) &&
    url2.includes('/static/')
  ) {
    return false
  }
  for (path of PYODIDE_ROUTER) {
    if (path.endsWith('*')) {
      if (url2.startsWith(path.slice(0, -1))) {
        return true
      }
    } else {
      if (path === url2) {
        return true
      }
    }
  }
  return false
}

var CALLBACK_ID = 0
var CALLBACK_HANDLER = {}

function callback_from_python (id, data) {
  CALLBACK_HANDLER[id](atob(data))
  delete CALLBACK_HANDLER[id]
}

function wx_get (url, params) {
  return new Promise(function (resolve, reject) {
    function callback (data) {
      resolve(data)
    }
    CALLBACK_HANDLER[CALLBACK_ID] = callback
    var message
    if (params != null && params != '')
      message = JSON.stringify({
        action: 'post',
        callback_id: CALLBACK_ID,
        url: url,
        params: params
      })
    else {
      message = JSON.stringify({
        action: 'get',
        callback_id: CALLBACK_ID,
        url: url
      })
    }
    CALLBACK_ID += 1
    wx_msg.postMessage(message)
  })
}

function pywebview_url (url) {
  if (window.hasOwnProperty('pywebview') || window.hasOwnProperty('wx_msg')) {
    return true
  }
  return false
}

async function pywebview_get_response (url, params) {
  console.log('A1')
  if (window.hasOwnProperty('wx_msg')) {
    console.log('A2')
    ret = await wx_get(url, params)
    console.log('A3')
    console.log(ret)
    return ret
  } else {
    if (params != null && params != '') {
      ret = await window.pywebview.api.get(url, params)
      return ret
    } else {
      ret = await window.pywebview.api.get(url, null)
      return ret
    }
  }
}

var PYTHON_PACKAGES = ['pytigon']

var PYTHON_INIT = `
print("=========================================== 1:")
import micropip
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
print("=========================================== 2:")
await micropip.install("pyquery")
print("=========================================== 3:")
try:
    import pytigon_lib
except:
    await micropip.install("pytigon")
print("=========================================== 4:")
from pytigon.pytigon_request import init, request
print("=========================================== 5:")
import js
print("=========================================== 6:")
from asgiref.sync import sync_to_async
print("=========================================== 7:")

def _init():
    init("$PRJ_NAME", "$USER", "$PASSWORD", "webview")

ret = await sync_to_async(_init)()
print("=========================================== 8:")

def _request(url, params=None):
    if params:
        params2 = params.to_py()
    else:
        params2 = None
    ret = request(url, params2, "webview")
    return ret

async def http_get(url, params=None):
    ret = await sync_to_async(_request)(url, params)
    return ret.str()

`

function pyodide_app_init (
  prj_name,
  base_url,
  url,
  application_template,
  language,
  user,
  password,
  callback
) {
  let pyodide = null
  async function main () {
    pyodide = await loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.18.1/full/'
    })
    pyodide.FS.rename(
      '/lib/python3.9/site-packages/pyodide',
      '/lib/python3.9/pyodide'
    )
    pyodide.FS.rename(
      '/lib/python3.9/site-packages/_pyodide',
      '/lib/python3.9/_pyodide'
    )
    //pyodide.FS.mount(pyodide.FS.filesystems.IDBFS, {}, '/home/web_user');
    pyodide.FS.mkdir('/lib/python3.9/site-packages/micropip')
    pyodide.FS.mount(
      pyodide.FS.filesystems.IDBFS,
      {},
      '/lib/python3.9/site-packages'
    )

    function sync_fs () {
      pyodide.FS.syncfs(true, async function (err) {
        async function init2 () {
          let save = false
          let example_dir = pyodide.FS.analyzePath(
            '/lib/python3.9/site-packages/micropip',
            true
          )
          if (!example_dir.exists) {
            save = true
          }
          await pyodide.loadPackage('packaging')
          await pyodide.loadPackage('pyparsing')
          await pyodide.loadPackage('pytz')
          await pyodide.loadPackage('setuptools')
          await pyodide.loadPackage('six')
          await pyodide.loadPackage('micropip')

          await pyodide.runPythonAsync(
            PYTHON_INIT.replaceAll('$PRJ_NAME', prj_name)
              .replaceAll('$BASE_URL', base_url)
              .replaceAll('$USER', user)
              .replaceAll('$PASSWORD', password)
          )
          PYODIDE = pyodide
          response = await fetch(url)
          if (save) {
            PYODIDE.FS.syncfs(false, function (err) {
              console.log('File system saved')
            })
          }
          await callback(response)
        }
        let db_dir = pyodide.FS.analyzePath(
          '/home/web_user/.pytigon/' + prj_name + '/' + prj_name + '.db',
          true
        )
        async function init3 (data) {
          //pyodide.FS.mkdir("/home/web_user/.pytigon");
          //pyodide.FS.mkdir("/home/web_user/.pytigon/"+prj_name);
          //pyodide.FS.writeFile("/home/web_user/.pytigon/"+prj_name+"/"+prj_name+".db", data);
          let db_file = pyodide.FS.open(
            '/home/web_user/.pytigon/' + prj_name + '/' + prj_name + '.db',
            'w'
          )
          pyodide.FS.write(db_file, data, 0, data.length, 0)
          pyodide.FS.close(db_file)
          await init2()
        }
        if (!db_dir.exists) {
          fetch(
            base_url + 'static/' + prj_name + '/install/' + prj_name + '.db'
          )
            .then(function (response) {
              //return response.text();
              return response.arrayBuffer()
              //init3(response.)
            })
            .then(function (buffer) {
              //let enc = new TextEncoder();
              //init3(enc.encode(buffer))
              let buffer2 = new Uint8Array(buffer)
              init3(buffer2)
            })
          //ajax_get("/static/"+prj_name+"/install/"+prj_name+".db", init3)
        } else {
          await init2()
        }
      })
    }

    navigator.serviceWorker.onmessage = event => {
      if (event.data && event.data.type === 'get_state') {
        pyodide.FS.mkdir('/home/web_user/.pytigon')
        pyodide.FS.mkdir('/home/web_user/.pytigon/' + prj_name)
        if (event.data.data) {
          let db_file = pyodide.FS.open(
            '/home/web_user/.pytigon/' + prj_name + '/' + prj_name + '.db',
            'w'
          )
          pyodide.FS.write(
            db_file,
            event.data.data.data,
            0,
            event.data.data.data.length,
            0
          )
          pyodide.FS.close(db_file)
        }
        sync_fs()
      }
    }

    navigator.serviceWorker.controller.postMessage({
      type: 'get_state',
      name: 'pytigon_db'
    })

    function onbeforeunload_sync () {
      if (PYODIDE) {
        let data = PYODIDE.FS.readFile(
          '/home/web_user/.pytigon/' + prj_name + '/' + prj_name + '.db',
          {}
        )
        navigator.serviceWorker.controller.postMessage({
          type: 'set_state',
          name: 'pytigon_db',
          data: data
        })
      }
    }

    window.onbeforeunload = onbeforeunload_sync
  }

  main()
}

window.pyodide_app_init = pyodide_app_init

async function pyodide_get_response (url, params) {
  if (params != null && params != '') {
    return await PYODIDE.globals.get('http_get')(url, params)
  } else {
    return await PYODIDE.globals.get('http_get')(url)
  }
}

/*
const constantMock = window.fetch;

window.fetch = async function() {
  console.log("FETCH: " + arguments[0])
  console.log(arguments)
  if (pyodide_url(arguments[0])) {
    ret = new Response(
      await pyodide_get_response(arguments[0]), {
        headers: {
          "Content-Type": "text/html"
        },
      }
    )
  } else if (pywebview_url(arguments[0])) {
    ret = new Response(
      await pywebview_get_response(arguments[0]), {
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
*/
var ACTIONS = {}
var ACTION_ID = 0

function set_action_data (data) {
  ACTION_ID += 1
  ACTIONS[id] = data
  return ACTION_ID
}

function get_action_data (id) {
  if (id in ACTIONS) {
    return ACTIONS[id]
  } else {
    return null
  }
}

function delete_action_data (id) {
  if (id in ACTIONS) {
    delete ACTIONS[id]
    return true
  } else {
    return false
  }
}

function str2ab (str) {
  var buf = new ArrayBuffer(str.length * 2) // 2 bytes for each char
  var bufView = new Uint16Array(buf)
  for (var i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i)
  }
  return buf
}
;(function () {
  var oldXMLHttpRequest = XMLHttpRequest
  modXMLHttpRequest = function () {
    var actual = new oldXMLHttpRequest()
    var self = this

    this.onreadystatechange = null
    this.onload = null
    this._readyState = 0
    this._responseText = ''
    this._status = 0
    this.sch_local_request = false
    this.url = null

    actual.onreadystatechange = function () {
      if (self.onreadystatechange != null) return self.onreadystatechange()
    }

    actual.onload = function () {
      if (self.onload != null) return self.onload()
    }

    this.open = function (
      sMethod,
      sUrl,
      bAsync = true,
      sUser = null,
      sPassword = null
    ) {
      console.log('XMLREQUEST: ' + sUrl)
      self.url = sUrl
      if (
        self.url.includes(PSEUDO_IP) ||
        pyodide_url(self.url) ||
        pywebview_url(self.url)
      ) {
        self.sch_local_request = true
        return true
      }
      return actual.open(sMethod, sUrl, bAsync, sUser, sPassword)
    }

    this.send = async function (vData) {
      if (this.sch_local_request && self.url.includes(PSEUDO_IP)) {
        var data = {}

        function _on_response (txt, py_callback) {
          self.readyState = 4
          if (self.responseType == 'arraybuffer') {
            self.response = str2ab(txt)
          } else {
            self.responseText = txt
          }
          self.status = 200
          if (self.onreadystatechange != null) self.onreadystatechange()
          if (self.onload != null) self.onload()
          return
        }

        if (vData) {
          py_function(['post', self.url, vData], _on_response)
        } else {
          py_function(['get', self.url, null])
        }
      } else if (this.sch_local_request && pyodide_url(self.url)) {
        self.readyState = 4

        if (vData) {
          const urlSearchParams = new URLSearchParams(vData)
          const params = Object.fromEntries(urlSearchParams.entries())
          self.responseText = await pyodide_get_response(self.url, params)
        } else {
          self.responseText = await pyodide_get_response(self.url)
        }
        self.response = self.responseText
        self.status = 200
        if (self.onreadystatechange != null) self.onreadystatechange()
        if (self.onload != null) self.onload()
        return null
      } else if (this.sch_local_request && pywebview_url(self.url)) {
        self.readyState = 4
        if (vData) {
          const urlSearchParams = new URLSearchParams(vData)
          const params = Object.fromEntries(urlSearchParams.entries())
          self.responseText = await pywebview_get_response(self.url, params)
        } else {
          self.responseText = await pywebview_get_response(self.url)
        }
        self.response = self.responseText
        self.status = 200
        if (self.onreadystatechange != null) self.onreadystatechange()
        if (self.onload != null) self.onload()
        return null
      } else {
        return actual.send(vData)
      }
    }

    this.setRequestHeader = function (key, value) {
      if (this.sch_local_request) return
      //if (pyodide_url(self.url) || self.url.includes(PSEUDO_IP)) return;
      return actual.setRequestHeader(key, value)
    }
    ;[
      'statusText',
      'responseType',
      'response',
      'responseXML',
      'upload'
    ].forEach(function (item) {
      Object.defineProperty(self, item, {
        get: function () {
          return actual[item]
        },
        set: function (val) {
          actual[item] = val
        }
      })
    })
    ;['readyState', 'responseText', 'status'].forEach(function (item) {
      Object.defineProperty(self, item, {
        get: function () {
          if (self['_' + item]) return self['_' + item]
          else return actual[item]
        },
        set: function (val) {
          self['_' + item] = val
        }
      })
    })

    //["readyState", "responseText", "status"].forEach(function (item) {
    //    Object.defineProperty(self, item, {
    //        get: function () { if (self["_" + item]) return self["_" + item]; else return actual[item]; },
    //        set: function (val) { self["_" + item] = val; }
    //    });
    //});
    ;[
      'ontimeout',
      'timeout',
      'withCredentials',
      'onerror',
      'onprogress'
    ].forEach(function (item) {
      Object.defineProperty(self, item, {
        get: function () {
          return actual[item]
        },
        set: function (val) {
          actual[item] = val
        }
      })
    })
    ;[
      'addEventListener',
      'abort',
      'getAllResponseHeaders',
      'getResponseHeader',
      'overrideMimeType',
      'responseURL'
    ].forEach(function (item) {
      Object.defineProperty(self, item, {
        value: function () {
          return actual[item].apply(actual, arguments)
        }
      })
    })
  }
  window.XMLHttpRequest = modXMLHttpRequest
})()

function import_module (html_txt) {
  var encodedJs = encodeURIComponent(html_txt)
  var dataUri = 'data:text/javascript;charset=utf-8,' + encodedJs
  try {
    require(dataUri)
  } catch (err) {
    console.log('Dynamic import is not supported')
  }
}

window.import_module = import_module

function jsimp (module) {
  return require(module)
}

window.jsimp = jsimp

function define_custom_element (tag, shadow, options) {
  class ProxyHTMLElement extends HTMLElement {
    static get observedAttributes () {
      if ('attributes' in options) {
        return Object.keys(options['attributes'])
      } else return []
    }

    constructor () {
      super()
      if (window.IN_MORPH_PROCESS) return
      this.state = {}
      this.options = options
      this.root = null
      this.attribute_actions_queue = []
      if ('global_state_actions' in options) {
        this.global_state_actions = options['global_state_actions']
      } else this.global_state_actions = {}
      if ('event_handler' in options) {
        this.event_handler = options['event_handler']
      } else this.event_handler = {}
      if ('constructor' in options) options['constructor'](this)
      if (shadow) {
        const shadowRoot = this.attachShadow({
          mode: 'open'
        })
        if ('template' in options) {
          shadowRoot.innerHTML = options['template']
          this.root = shadowRoot
        }
        if (this.state) {
          let state = this.state
          this.state = {}
          this.set_state(state)
        }
        if ('init' in options) options['init'](this)
        this.attributes_init()
      } else {
        if ('template' in options) this.innerHTML = options['template']
      }
      if (this.global_state_actions) {
        window.GLOBAL_BUS.register(this)
      }
    }

    attributes_init () {
      if (this.attribute_actions_queue) {
        let component = this
        this.attribute_actions_queue.forEach(function (item, index) {
          component.attributeChangedCallback(item[0], item[1], item[2])
        })
        this.attribute_actions_queue = []
      }
    }

    set_state (state) {
      if ('set_state' in options) {
        options['set_state'](this, state)
      }
    }

    set_external_state (state) {
      if (this.global_state_actions) {
        let component = this
        Object.keys(state).forEach(function (key) {
          if (key in component.global_state_actions) {
            component.global_state_actions[key](component, state[key])
          }
        })
      }
    }

    handle_event (name, value) {
      if (this.event_handler) {
        let component = this
        if (name in this.event_handler) {
          this.event_handler[name](component, value)
        }
      }
    }

    connectedCallback () {
      if (!shadow) {
        //if ("template" in options) this.innerHTML = options["template"];
        this.root = this
        if (this.state) {
          let state = this.state
          this.state = {}
          this.set_state(state)
        }
        if ('init' in options) options['init'](this)
        this.attributes_init()
      }
      if ('connectedCallback' in options) {
        options['connectedCallback'](this)
      }
    }

    disconnectedCallback () {
      if ('disconnectedCallback' in options) {
        options['disconnectedCallback'](this)
      }
      if (this.global_state_actions) {
        window.GLOBAL_BUS.unregister(this)
      }
    }

    attributeChangedCallback (name, oldVal, newVal) {
      if (!this.root) {
        if (this.attribute_actions_queue) {
          this.attribute_actions_queue.push([name, oldVal, newVal])
        }
        return
      }
      if ('attributeChangedCallback' in options) {
        options['attributeChangedCallback'](this, name, oldVal, newVal)
      } else {
        if ('attributes' in options) {
          if (options['attributes'][name])
            options['attributes'][name](this, oldVal, newVal)
          else
            this.set_state({
              [name]: newVal
            })
        }
      }
    }
  }
  customElements.define(tag, ProxyHTMLElement)
}

window.define_custom_element = define_custom_element

function syncfs () {
  return new Promise(resolve => {
    PYODIDE.FS.syncfs(false, function (err) {
      resolve(err)
    })
  })
}

async function sync_on_unload () {
  await syncfs()
}

async function dynamic_import (url, callback) {
  import(url).then(callback)
}

function getParamsFromUrl (url) {
  url = decodeURI(url)
  if (typeof url === 'string') {
    let params = url.split('?')
    let eachParamsArr = params[1].split('&')
    let obj = {}
    if (eachParamsArr && eachParamsArr.length) {
      eachParamsArr.map(param => {
        let keyValuePair = param.split('=')
        let key = keyValuePair[0]
        let value = keyValuePair[1]
        obj[key] = value
      })
    }
    return obj
  }
}

function getParamsFromEncodedParams (encoded_params) {
  let eachParamsArr = encoded_params.split('&')
  let obj = {}
  if (eachParamsArr && eachParamsArr.length) {
    eachParamsArr.map(param => {
      let keyValuePair = param.split('=')
      let key = keyValuePair[0]
      let value = keyValuePair[1]
      obj[key] = value
    })
  }
  return obj
}

function get_graphql () {
  token = localStorage.getItem('api_token')
  if (token) {
    return graphql(window.COMPONENT_INIT.graphql_pub, {
      headers: {
        authorization: 'JWT ' + token
      }
    })
  } else {
    return null
  }
}

function get_public_graphql () {
  return graphql(window.COMPONENT_INIT.graphql_pub)
}
