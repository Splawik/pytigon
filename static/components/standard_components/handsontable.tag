<handsontable>
    <div name="handsontablediv"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/jquery_plugins";
    load_css(this.base_path + "/handsontable.full.css");
    this.on("mount", function() {
        var self;
        self = this;
        load_js(self.base_path + "/handsontable.full.js", function() {
            var data, htable;
            data = [ [ "Column A", "Column B", "Column C" ], [ "1", "2", "3" ] ];
            htable = new window.Handsontable(self.handsontablediv, {
                "data": data
            });
            self.htable = htable;
        });
    });</script>
    
    
</handsontable>