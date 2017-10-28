var subreport_dragstart = function (ev) {
	ev.dataTransfer.setData ('id', ev.target.getAttribute ('name'));
};
var subreport_drop = function (ev, base_path) {
	ev.preventDefault ();
	var data = ev.dataTransfer.getData ('id');
	var data2 = ev.target.getAttribute ('name');
	if (data2 != data) {
		var href = ((((base_path + '/schreports/table/Report/') + data) + '/') + data2) + '/action/move_to';
		ajax_get (href, standard_on_data (jQuery (ev.target), href));
	}
};
var subreport_ondragenter = function (ev) {
	jQuery (ev.target).addClass ('bg-success');
};
var subreport_ondragleave = function (ev) {
	jQuery (ev.target).removeClass ('bg-success');
};
var subreport_ondragover = function (ev) {
	ev.preventDefault ();
};
