
		var Test = __class__ ('Test', [object], {
			get __init__ () {return __get__ (this, function (self) {
				self.value = 0;
			});},
			get get_value () {return __get__ (this, function (self) {
				return self.value;
			});}
		});
		__pragma__ ('<all>')
			__all__.Test = Test;
		__pragma__ ('</all>')
	