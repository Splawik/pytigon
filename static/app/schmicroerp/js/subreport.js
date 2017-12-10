var subreport_dragstart = function (ev) {
	ev.dataTransfer.setData ('text', ev.target.getAttribute ('name'));
};
var subreport_drop = function (ev, base_path) {
	ev.preventDefault ();
	if (ev.target.tagName == 'LABEL') {
		var target = ev.target;
	}
	else {
		var target = ev.target.parentElement;
	}
	var data = ev.dataTransfer.getData ('text');
	var data2 = target.getAttribute ('name');
	if (data2 != data) {
		var href = ((((base_path + '/schreports/table/Report/') + data) + '/') + data2) + '/action/move_to/';
		ajax_get (href, standard_on_data (jQuery (target), href));
	}
};
var subreport_ondragenter = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		jQuery (ev.target).addClass ('bg-success');
	}
};
var subreport_ondragleave = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		jQuery (ev.target).removeClass ('bg-success');
	}
};
var subreport_ondragover = function (ev) {
	if (ev.target.tagName == 'LABEL') {
		ev.preventDefault ();
	}
};
