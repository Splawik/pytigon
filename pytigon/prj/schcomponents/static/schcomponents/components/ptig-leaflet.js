// Transcrypt'ed from Python, 2020-02-09 15:01:46
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var BASE_PATH = window.BASE_PATH + 'static/vanillajs_plugins/leaflet';
export var _marker = dict ({'props': ['x', 'y', 'txt'], 'template': ''});
Vue.component ('ptig-marker', _marker);
export var ptig_leaflet = function () {
	var props = ['width', 'height', 'x', 'y'];
	var template = "<div name='mapdiv' v-bind:style='{ width: width, height: height}' ></div>";
	var mounted = function () {
		L.Icon.Default.imagePath = BASE_PATH + '/images';
		var mapobj = L.map (this.$el).setView ([this.x, this.y], 13);
		L.tileLayer ('http://{s}.tile.osm.org/{z}/{x}/{y}.png', dict ({'attribution': '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'})).addTo (mapobj);
		var _process_slot = function (slot) {
			if (slot.tag == 'ptig-maker') {
				var maker = L.marker ([slot.data.attrs.x, slot.data.attrs.y]);
				maker.addTo (mapobj);
				maker.bindPopup (slot.data.attrs.txt);
				maker.openPopup ();
			}
		};
		this.$slots.default.forEach (_process_slot);
		this.mapobj = mapobj;
	};
	return dict ({'props': props, 'template': template, 'mounted': mounted});
};
register_vue_component ('ptig-leaflet', ptig_leaflet, [BASE_PATH + '/leaflet.js'], [BASE_PATH + '/leaflet.css']);

//# sourceMappingURL=input.map