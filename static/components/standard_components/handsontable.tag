<handsontable>
    <div name="handsontablediv"></div>
    <script>
    
    
    
    base_path = BASE_PATH + "static/jquery_plugins";
    self = this;
    load_css(base_path + "/handsontable.full.css");
    this.on("mount", function() {
        load_js(base_path + "/handsontable.full.js", function() {
            var data, htable;
            data = [ [ "Column A", "Column B", "Column C" ], [ "1", "2", "3" ] ];
            htable = new window.Handsontable(self.handsontablediv, {
                "data": data
            });
            self.htable = htable;
        });
    });</script>
    
    
</handsontable>