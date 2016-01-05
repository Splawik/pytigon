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
            console.log("\n" + sUrl);

            if(sUrl.slice(0, 9) == "static://" || window.location.host == "127.0.0.2") {  
                this.sch_local_request = true;
                return null;
            }
            return actual.open(sMethod, sUrl, bAsync, sUser, sPassword)
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
                    //var data = JSON.stringify(vData.getAll());
                    var data=vData;
                    if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true ))
                        document.location.href = "http://localbrowser/?ajax_post??"+ sUrl2+"??"+btoa(data);
                    else
                        document.title = ":ajax_post??"+ sUrl2+"??"+btoa(data);
                }
                else {
                    if((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true ))
                        document.location.href = "http://localbrowser/?ajax_get??"+ sUrl2;
                    else
                        //alert("FFFF")
                        //alert(sUrl2)
                        console.log(sUrl2)
                        document.title = ":";
                        document.title = ":ajax_get??"+ sUrl2;
                        document.title = ":";
                }

                return null;
            }
            else {
                actual.send(vData)
            }
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
         "getResponseHeader", "overrideMimeType", "setRequestHeader"].forEach(function(item) {
            Object.defineProperty(self, item, {
                value: function() {return actual[item].apply(actual, arguments);}
            });
        });
    }
    window.XMLHttpRequest = modXMLHttpRequest;
})();
