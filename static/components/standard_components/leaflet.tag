<leaflet>
    <div name="mapdiv" style="width: { opts.width }; height: { opts.height };"></div>
    <script>
    
    
    
    this.base_path = BASE_PATH + "static/vanillajs_plugins/leaflet";
    load_css(this.base_path + "/leaflet.css");
    this.on("mount", function() {
        var self;
        self = this;
        load_js(self.base_path + "/leaflet.js", function() {
            var mapobj, maker;
            L.Icon.Default.imagePath = self.base_path + "/images";
            mapobj = L.map(self.mapdiv).setView([ 51.613007, 21.491859 ], 13);
            L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
                attribution: "&copy; <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors"
            }).addTo(mapobj);
            maker = L.marker([ 51.613007, 21.491859 ]);
            maker.addTo(mapobj);
            maker.bindPopup("<b>Hello world!</b><br />I am a popup.");
            maker.openPopup();
            self.mapobj = mapobj;
        });
    });</script>
    
    
</leaflet>