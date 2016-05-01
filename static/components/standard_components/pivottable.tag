<pivottable>
    <div name="pivottablediv"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/jquery_plugins/pivottable";
    load_css(this.base_path + "/pivot.css");
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/pivot.js", function () {
            load_js(self.base_path + "/../jquery.ui/jquery-ui.min.js", function () {
                var data, options, pivottable;
                data = ρσ_list_decorate([ (function(){
                    var ρσ_d = {};
                    ρσ_d["color"] = "blue";
                    ρσ_d["shape"] = "circle";
                    return ρσ_d;
                }).call(this), (function(){
                    var ρσ_d = {};
                    ρσ_d["color"] = "red";
                    ρσ_d["shape"] = "triangle";
                    return ρσ_d;
                }).call(this) ]);
                options = (function(){
                    var ρσ_d = {};
                    ρσ_d["rows"] = ρσ_list_decorate([ "color" ]);
                    ρσ_d["cols"] = ρσ_list_decorate([ "shape" ]);
                    return ρσ_d;
                }).call(this);
                pivottable = jQuery(self.pivottablediv).pivotUI(data, options);
                self.pivottable = pivottable;
            });
        });
    });</script>
    
    
</pivottable>