
		var mounted = function () {
			var txtarea = jQuery (this.$el);
			txtarea.addClass ('vue');
			var base_path = window.BASE_PATH + 'static/vanillajs_plugins/ace/src-min';
			var _on_loadjs = function () {
				ace.config.set ('basePath', base_path);
				var a = jQuery ('<div></div>');
				txtarea.after (a);
				var editor = ace.edit (a [0]);
				editor.setOptions (dict ({'maxLines': 32}));
				editor.setTheme ('ace/theme/textmate');
				editor.getSession ().setMode ('ace/mode/markdown');
				editor.getSession ().setValue (txtarea.val ());
				txtarea.hide ();
				var _on_change = function () {
					txtarea.val (editor.getSession ().getValue ());
				};
				editor.getSession ().on ('change', _on_change);
			};
			load_js (base_path + '/ace.js', _on_loadjs);
		};
		var target = jQuery ('body') [0];
		var process_mutations = function (mutations) {
			var _process_mutation = function (mutation) {
				var newNodes = mutation.addedNodes;
				if (newNodes != null) {
					var nodes = jQuery (newNodes);
					var _process_node = function () {
						var node = jQuery (this);
						var txtarray = node.find ('textarea.ceditor');
						if (txtarray.length > 0 && !(txtarray.hasClass ('vue'))) {
							var _process_txt = function () {
								var vm = new Vue (dict ({'el': this, 'mounted': mounted}));
							};
							txtarray.each (_process_txt);
						}
					};
					nodes.each (_process_node);
				}
			};
			mutations.forEach (_process_mutation);
		};
		var observer = new MutationObserver (process_mutations);
		var config = dict ({'attributes': false, 'childList': true, 'characterData': true, 'subtree': true});
		observer.observe (target, config);
		__pragma__ ('<all>')
			__all__.config = config;
			__all__.mounted = mounted;
			__all__.observer = observer;
			__all__.process_mutations = process_mutations;
			__all__.target = target;
		__pragma__ ('</all>')
	