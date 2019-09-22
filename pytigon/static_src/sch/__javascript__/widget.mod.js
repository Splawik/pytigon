	__nest__ (
		__all__,
		'widget', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'widget';
					var humanFileSize = function (bytes, si) {
						if (si) {
							var thresh = 1000;
						}
						else {
							var thresh = 1024;
						}
						if (Math.abs (bytes) < thresh) {
							return tuple ([bytes + ' B', 0]);
						}
						if (si) {
							var units = list (['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']);
						}
						else {
							var units = list (['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']);
						}
						var u = -(1);
						while (true) {
							bytes /= thresh;
							u++;
							if (!(Math.abs (bytes) >= thresh && u < units.length - 1)) {
								break;
							}
						}
						return tuple ([(bytes.toFixed (1) + ' ') + units [u], u + 1]);
					};
					var img_field = function (elem) {
						var txt = jQuery (elem).val ().py_replace (new RegExp ('^.*[\\\\ /]'), '');
						jQuery (elem).closest ('label').find ('.upload').html (txt);
						if (elem.files && elem.files [0]) {
							var file_name = elem.files [0].name;
							var ext = list (['.jpeg', '.jpg', '.svg', '.gif', '.png']);
							var test = false;
							var __iterable0__ = ext;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (__in__ (pos, file_name.lower ())) {
									var test = true;
									break;
								}
							}
							if (test) {
								var reader = new FileReader ();
								var _onload = function (e) {
									var x = jQuery (elem).closest ('label').find ('.img');
									if (x.length > 0) {
										x.remove ();
									}
									var img = jQuery ("<img class='img' />");
									img.insertAfter (jQuery (elem).closest ('label').find ('input'));
									img.attr ('src', e.target.result);
								};
								reader.onload = _onload;
								reader.readAsDataURL (elem.files [0]);
							}
							else {
								var x = jQuery (elem).closest ('label').find ('.img');
								if (x.length > 0) {
									x.remove ();
								}
								var __left0__ = humanFileSize (elem.files [0].size, true);
								var size = __left0__ [0];
								var level = __left0__ [1];
								var ext = ((((elem.files [0].type + "<br><span class='size_level_") + level) + "'>") + size) + '</span>';
								var img = jQuery ("<p class='img' />");
								img.insertAfter (jQuery (elem).closest ('label').find ('input'));
								img.html (ext);
							}
						}
					};
					window.img_field = img_field;
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.humanFileSize = humanFileSize;
						__all__.img_field = img_field;
					__pragma__ ('</all>')
				}
			}
		}
	);
