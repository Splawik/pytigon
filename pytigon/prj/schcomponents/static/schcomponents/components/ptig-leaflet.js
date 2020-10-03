// Transcrypt'ed from Python, 2020-10-03 09:12:22
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var TAG = 'ptig-leaflet';
export var TEMPLATE = '        <div class=\"leafletframe\" data-bind=\"style-width:width;style-height:height\">\n' +
    '                <div class=\"leafletdiv\" style=\"width:100%;height:100%\"></div>\n' +
    '        </div>\n' +
    '        <slot></slot>\n' +
    '\n' +
    '';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/leaflet';
var comp = DefineWebComponent (TAG, true, [BASE_PATH + '/leaflet.js'], [BASE_PATH + '/leaflet.css']);
try {
	comp.__enter__ ();
	comp.options ['attributes'] = dict ({'width': null, 'height': null});
	comp.options ['template'] = TEMPLATE;
	var constructor = comp.fun ('constructor') (function (component) {
		component.makers = [];
		var process_slot = function (slot) {
			component.makers.append (tuple ([slot.getAttribute ('x'), slot.getAttribute ('y'), slot.getAttribute ('txt')]));
		};
		component ['process_slot'] = process_slot;
	});
	var init = comp.fun ('init') (function (component) {
		var div = component.root.querySelector ('div.leafletdiv');
		L.Icon.Default.imagePath = BASE_PATH + '/images';
		if (component.hasAttribute ('x')) {
			var x = float (component.getAttribute ('x'));
		}
		else {
			var x = 0;
		}
		if (component.hasAttribute ('y')) {
			var y = float (component.getAttribute ('y'));
		}
		else {
			var y = 0;
		}
		if (component.hasAttribute ('z')) {
			var z = float (component.getAttribute ('z'));
		}
		else {
			var z = 13;
		}
		var mapobj = L.map (div).setView ([x, y], z);
		L.tileLayer ('http://{s}.tile.osm.org/{z}/{x}/{y}.png', dict ({'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'})).addTo (mapobj);
		if (component.makers) {
			for (var pos of component.makers) {
				var maker = L.marker ([pos [0], pos [1]]);
				maker.addTo (mapobj);
				maker.bindPopup (pos [2]);
				maker.openPopup ();
			}
		}
		component ['mapobj'] = mapobj;
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}
var comp = DefineWebComponent ('ptig-maker', false);
try {
	comp.__enter__ ();
	comp.options ['template'] = '';
	var init = comp.fun ('init') (function (component) {
		component.parentNode.process_slot (component);
	});
	comp.__exit__ ();
}
catch (__except0__) {
	if (! (comp.__exit__ (__except0__.name, __except0__, __except0__.stack))) {
		throw __except0__;
	}
}

//# sourceMappingURL=input.map