var comp, event_handler, init, refresh_bi_chart, refresh_bi_page, refresh_bi_project, stub1_context, stub2_err;
stub1_context = (new DefineWebComponent("refresh-bi-charts", true));
comp = stub1_context.__enter__();
try {
    init = function flx_init (component) {
        return null;
    };

    refresh_bi_project = function flx_refresh_bi_project (component, data) {
        var chart_list, item, prj_name, stub3_seq, stub4_itr;
        prj_name = data;
        chart_list = Array.prototype.slice.call(document.querySelectorAll((("div.bi_" + prj_name) + " div.active .bi_prj_") + prj_name));
        stub3_seq = chart_list;
        if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
        for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
            item = stub3_seq[stub4_itr];
            window.refresh_ajax_frame(item);
            console.log("REFRESH_BI_PROJECT", item);
        }
        return null;
    };

    refresh_bi_page = function flx_refresh_bi_page (component, data) {
        var chart_list, item, page_name, stub5_seq, stub6_itr;
        page_name = data;
        chart_list = Array.prototype.slice.call(document.querySelectorAll(".bi_page_" + page_name));
        stub5_seq = chart_list;
        if ((typeof stub5_seq === "object") && (!Array.isArray(stub5_seq))) { stub5_seq = Object.keys(stub5_seq);}
        for (stub6_itr = 0; stub6_itr < stub5_seq.length; stub6_itr += 1) {
            item = stub5_seq[stub6_itr];
            window.refresh_ajax_frame(item);
            console.log("REFRESH_BI_PAGE", item);
        }
        return null;
    };

    refresh_bi_chart = function flx_refresh_bi_chart (component, data) {
        var chart_list, chart_name, item, stub7_seq, stub8_itr;
        chart_name = data;
        chart_list = Array.prototype.slice.call(document.querySelectorAll(".bi_chart_" + chart_name));
        stub7_seq = chart_list;
        if ((typeof stub7_seq === "object") && (!Array.isArray(stub7_seq))) { stub7_seq = Object.keys(stub7_seq);}
        for (stub8_itr = 0; stub8_itr < stub7_seq.length; stub8_itr += 1) {
            item = stub7_seq[stub8_itr];
            window.refresh_ajax_frame(item);
            console.log("REFRESH_BI_CHART", item);
        }
        return null;
    };

    event_handler = ({refresh_bi_project: refresh_bi_project, refresh_bi_page: refresh_bi_page, refresh_bi_chart: refresh_bi_chart});
    comp.options["init"] = init;
    comp.options["event_handler"] = event_handler;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}