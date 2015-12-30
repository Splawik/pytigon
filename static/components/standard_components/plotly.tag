<plotly>
    <div name="plotlydiv" style="width:{ opts.width };height:{ opts.height };" modebar="false"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins";
    this.on("mount", function() {
        var self;
        self = this;
        load_js(self.base_path + "/plotly-latest.min.js", function() {
            var data, layout, plot;
            data = [ {
                values: [ 19, 26, 55 ],
                labels: [ "Residential", "Non-Residential", "Utility" ],
                type: "pie"
            } ];
            layout = {
                "height": 400,
                "width": 500
            };
            plot = Plotly.newPlot(self.plotlydiv, data, layout, {
                "displayModeBar": true,
                "showLink": false,
                "displaylogo": false,
                "scrollZoom": true,
                "modeBarButtonsToRemove": [ "sendDataToCloud" ]
            });
            self.plot = plot;
        });
    });</script>
    
    
</plotly>