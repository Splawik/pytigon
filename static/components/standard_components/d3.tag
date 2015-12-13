<d3>
    <div name="d3div" width={ opts.width } height={ opts.height }></div>
    <script>
    base_path = BASE_PATH + "static/vanillajs_plugins";
    self = this;
    this.on("mount", function() {
        load_js(base_path + "/plotly-latest.min.js", function() {
            var sampleSVG;
            sampleSVG = d3.select(self.d3div).append("svg").attr("width", 100).attr("height", 100);
            sampleSVG.append("circle").style("stroke", "gray").style("fill", "white").attr("r", 40).attr("cx", 50).attr("cy", 50).on("mouseover", function() {
                d3.select(this).style("fill", "aliceblue");
            }).on("mouseout", function() {
                d3.select(this).style("fill", "white");
            });
        });
    });</script>
    
    
</d3>