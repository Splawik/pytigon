var BASE_PATH, TAG, comp, init, stub1_context, stub2_err;
TAG = "ptig-db";
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/pouchdb/pouchdb-7.3.0.min.js"]));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = "";
    init = function flx_init (component) {
        var db, obj, on_created, on_error, on_list, options;
        db = new PouchDB("TestUsersDB");
        obj = ({name: "Kinga", age: 18, street: "East 13:th Street"});
        on_created = (function flx_on_created (result) {
            console.log(result);
            return null;
        }).bind(this);

        on_error = (function flx_on_error (err) {
            console.log(error);
            return null;
        }).bind(this);

        (((db.bulkDocs([obj]).then)(on_created)).catch)(on_error);
        options = ({include_docs: true, attachments: false});
        on_list = (function flx_on_list (result) {
            var doc, stub3_seq, stub4_itr;
            stub3_seq = result.rows;
            if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
            for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                doc = stub3_seq[stub4_itr];
                console.log(doc);
            }
            return null;
        }).bind(this);

        (((db.allDocs(options).then)(on_list)).catch)(on_error);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}