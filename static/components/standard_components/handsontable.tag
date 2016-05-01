<handsontable>
    <div name="handsontablediv"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/jquery_plugins";
    load_css(this.base_path + "/handsontable.full.css");
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/handsontable.full.js", function () {
            var data, htable;
            data = ρσ_list_decorate([ ρσ_list_decorate([ "Column A", "Column B", "Column C" ]), ρσ_list_decorate([ "1", "2", "3" ]) ]);
            htable = new window.Handsontable(self.handsontablediv, (function(){
                var ρσ_d = {};
                ρσ_d["data"] = data;
                return ρσ_d;
            }).call(this));
            self.htable = htable;
        });
    });</script>
    
    
</handsontable>