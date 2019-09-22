	__nest__ (
		__all__,
		'tabmenuitem', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tabmenuitem';
					var TabMenuItem = __class__ ('TabMenuItem', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, id, title, url, data) {
							if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
								var data = null;
							};
							self.id = id;
							self.title = jQuery.trim (title);
							self.url = url;
							self.data = data;
						});}
					});
					__pragma__ ('<all>')
						__all__.TabMenuItem = TabMenuItem;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);
