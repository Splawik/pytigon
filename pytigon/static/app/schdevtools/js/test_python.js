var __name__ = '__main__';
var Test = __class__ ('Test', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		self.value = 0;
	});},
	get_value: function () {
		var self = this;
		return self.value;
	}
});