<handsontable>
    <div name="handsontablediv"></div>
    <script>
    
    
    
    ՐՏ_print("uuu1");
    base_path = BASE_PATH + "static/jquery_plugins";
    self = this;
    ՐՏ_print("uuu2");
    load_css(base_path + "/handsontable.full.css");
    ՐՏ_print("uuu3");
    this.on("mount", function() {
        ՐՏ_print("uuu5");
        load_js(base_path + "/handsontable.full.js", function() {
            var data, htable;
            ՐՏ_print("uuu6");
            data = [ [ "Column A", "Column B", "Column C" ], [ "1", "2", "3" ] ];
            alert(window.Handsontable);
            alert(window.Handsontable.constructor);
            htable = new window.Handsontable(self.handsontablediv, {
                "data": data
            });
            self.htable = htable;
            ՐՏ_print("uuu7");
        });
    });
    ՐՏ_print("uuu4");</script>
    
    
</handsontable>