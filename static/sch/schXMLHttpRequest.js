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
            if (self.onreadystatechange != null) self.onreadystatechange();
        };

        actual.onload = function () {
            if (self.onload != null) self.onload();
        }

        this.open = function(sMethod, sUrl, bAsync, sUser, sPassword) {
            self.url = sUrl;
            if(window.location.host == "127.0.0.2" && ( sMethod == 'POST' || navigator.userAgent.indexOf("Windows") != -1  )
               && (sUrl.indexOf("/static") == -1 )
            )
            {
                self.sch_local_request = true;
                return null;
            }
            var ret = actual.open(sMethod, sUrl, bAsync, sUser, sPassword);
            self.overrideMimeType('text/xml; charset=utf-8');
            return ret;
        };

        this.send = function(vData) {
            if (this.sch_local_request) {
                var sUrl2, sUrl3;
                if(self.url.slice(0,1) == "/") sUrl2 = window.location.protocol + "//" + window.location.host + self.url;
                else sUrl2 = self.url;
                sUrl3 = self.url.split("?")[0]
                function xx(txt) {
                    self.readyState = 4;
                    self.responseText = txt;
                    self.status = 200;
                    if(self.onreadystatechange != null) self.onreadystatechange();
                    if(self.onload != null) self.onload();
                    return;
                }

                if("ajax_get_response_fun" in window) {
                    window.ajax_get_response_fun[sUrl3] = xx;
                }
                else {   
                    window.ajax_get_response_fun = {};
                    window.ajax_get_response_fun[sUrl3] = xx;
                }

                if(vData) {
                    //hack
                    var data=vData;
                    if((navigator.userAgent.indexOf("Windows") != -1 ) || (!!document.documentMode == true ))
                        console.log(":ajax_post??"+ sUrl2+"??"+btoa(data));
                    else
                        window.open("http://127.0.0.2/?:ajax_post??"+ sUrl2+"??"+btoa(data));
                }
                else {
                    if((navigator.userAgent.indexOf("Windows") != -1 ) || (!!document.documentMode == true ))
                        console.log(":ajax_get??"+ sUrl2);
                    else
                        window.open("http://127.0.0.2/?:ajax_get??"+ sUrl2);
                }

                return null;
            }
            else {
                if(vData) {
                    self.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                    self.setRequestHeader("Content-length", vData.length);
                    self.setRequestHeader("Connection", "close");
                }
                actual.send(vData)
            }
        };

        this.setRequestHeader = function(key, value) {
            if(this.sch_local_request) return;
            return actual.setRequestHeader(key, value);
        };

        [ "statusText", "responseType", "response",
          "responseXML", "upload"].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() {return actual[item];}
            });
        });

        ["readyState", "responseText", "status"].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() { if(self["_"+item]) return self["_"+item]; else return actual[item]; },
                set: function(val) { self["_"+item] = val;  }
            });
        });

        ["ontimeout", "timeout", "withCredentials", "onerror", "onprogress"].forEach(function(item) {
            Object.defineProperty(self, item, {
                get: function() {return actual[item];},
                set: function(val) {actual[item] = val;}
            });
        });

        ["addEventListener", "abort", "getAllResponseHeaders",
         "getResponseHeader", "overrideMimeType"].forEach(function(item) {
            Object.defineProperty(self, item, {
                value: function() {return actual[item].apply(actual, arguments);}
            });
        });
    }
    window.XMLHttpRequest = modXMLHttpRequest;
})();
