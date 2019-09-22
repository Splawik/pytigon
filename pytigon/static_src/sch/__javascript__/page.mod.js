	__nest__ (
		__all__,
		'page', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'page';
					var Page = __class__ ('Page', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, id, page) {
							self.id = id;
							self.page = page;
						});},
						get set_href () {return __get__ (this, function (self, href) {
							self.page.attr ('_href', href);
						});},
						get get_href () {return __get__ (this, function (self) {
							return self.page.attr ('_href');
						});}
					});
					__pragma__ ('<all>')
						__all__.Page = Page;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);
