/**
 * 3D Text plugin for jQuery
 * v1.0
 * Creates 3D text using CSS3 text-shadows
 *
 * By Craig Buckler, @craigbuckler, http://optimalworks.net
 *
 * As featured on SitePoint.com:
 * http://www.sitepoint.com/css3-3d-text-jquery-plugin/
 *
 * Please use as you wish at your own risk.
 */

(function($) {

	// jQuery plugin definition
	$.fn.text3d = function(opts) {
	
		// default configuration
		var config = $.extend({}, {
			depth: 5,
			angle: 100,
			color: "#ddd",
			lighten: -0.15,
			shadowDepth: 10,
			shadowAngle: 80,
			shadowOpacity: 0.3
		}, opts);
		
		// to radians
		config.angle = config.angle * Math.PI / 180;
		config.shadowAngle = config.shadowAngle * Math.PI / 180;
		
		// create text shadow
		function TextShadow(e) {
		
			var s = "", i, f, x, y, c;
			
			// 3D effect
			for (i = 1; i <= config.depth; i++) {
				x = Math.round(Math.cos(config.angle) * i);
				y = Math.round(Math.sin(config.angle) * i);
				c = ColorLuminance(config.color, (i-1)/(config.depth-1)*config.lighten);
				s += x+"px "+y+"px 0 "+c+",";
			}
			
			// shadow
			for (f = 1, i = 1; f <= config.shadowDepth; i++) {
				f = f+i;
				x = Math.round(Math.cos(config.shadowAngle) * f);
				y = Math.round(Math.sin(config.shadowAngle) * f);
				c = config.shadowOpacity - ((config.shadowOpacity - 0.1) * i/config.shadowDepth);
				s += x+"px "+y+"px "+f+"px rgba(0,0,0,"+c+"),";
			}
			
			e.style.textShadow = s.substr(0, s.length-1);		
		}
		
		
		// return lighter (+lum) or darker (-lum) color
		function ColorLuminance(hex, lum) {

			// validate hex string
			hex = String(hex).replace(/[^0-9a-f]/gi, '');
			if (hex.length < 6) {
				hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
			}
			lum = lum || 0;
			
			// convert to decimal and change luminosity
			var rgb = "#", c, i;
			for (i = 0; i < 3; i++) {
				c = parseInt(hex.substr(i*2,2), 16);
				c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
				rgb += ("00"+c).substr(c.length);
			}

			return rgb;
		}

		
		// initialization
		this.each(function() {
			TextShadow(this);
		});

		return this;
	};

})(jQuery);


// initialize all expanding textareas
jQuery(function() {
	jQuery(".text3d").text3d();
});
