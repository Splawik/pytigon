<plotly>
    <div name="plotlydiv" style="width:{ opts.width };height:{ opts.height };" modebar="false"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins";
    this.on("mount", function () {
        var self;
        self = this;
        load_js(self.base_path + "/plotly-latest.min.js", function () {
            var data, layout, plot;
            data = ρσ_list_decorate([ (function(){
                var ρσ_d = {};
                ρσ_d["values"] = ρσ_list_decorate([ 19, 26, 55 ]);
                ρσ_d["labels"] = ρσ_list_decorate([ "Residential", "Non-Residential", "Utility" ]);
                ρσ_d["type"] = "pie";
                return ρσ_d;
            }).call(this) ]);
            layout = (function(){
                var ρσ_d = {};
                ρσ_d["height"] = 400;
                ρσ_d["width"] = 500;
                return ρσ_d;
            }).call(this);
            plot = Plotly.newPlot(self.plotlydiv, data, layout, (function(){
                var ρσ_d = {};
                ρσ_d["displayModeBar"] = true;
                ρσ_d["showLink"] = false;
                ρσ_d["displaylogo"] = false;
                ρσ_d["scrollZoom"] = true;
                ρσ_d["modeBarButtonsToRemove"] = ρσ_list_decorate([ "sendDataToCloud" ]);
                return ρσ_d;
            }).call(this));
            self.plot = plot;
        });
    });</script>
    
    
</plotly>