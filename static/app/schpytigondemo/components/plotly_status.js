var __name__ = '__main__';
var _sch_plotly_status = function (resolve, reject) {
	var data = function () {
		return dict ({'txt': 'START'});
	};
	var template = '<span>{{txt}}</span>';
	var created = function () {
		var this_obj = this;
		var on_event = function (data) {
			if (__in__ ('destination', data) && data ['destination'] == 'plotly/plotly-status/') {
				this_obj.txt = data ['points'] [0] ['x'];
			}
		};
		global_vue_bus.$on ('plotly', on_event);
	};
	resolve (dict ({'data': data, 'template': template, 'created': created}));
};
Vue.component ('sch-plotly-status', _sch_plotly_status);
