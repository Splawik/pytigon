<pivottable>
    <div name="pivottablediv"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/jquery_plugins/pivottable";
    load_css(this.base_path + "/pivot.css");
    this.on("mount", function() {
        var self;
        self = this;
        load_js(self.base_path + "/pivot.js", function() {
            load_js(self.base_path + "/../jquery.ui/jquery-ui.min.js", function() {
                var data, options, pivottable;
                data = [ {
                    color: "blue",
                    shape: "circle"
                }, {
                    color: "red",
                    shape: "triangle"
                } ];
                options = {
                    rows: [ "color" ],
                    cols: [ "shape" ]
                };
                pivottable = jQuery(self.pivottablediv).pivotUI(data, options);
                self.pivottable = pivottable;
            });
        });
    });</script>
    
    
</pivottable>