var BASE_PATH, TAG, comp, init, stub1_context, stub2_err;
TAG = "ptig-db2";
BASE_PATH = window.BASE_PATH + "static/vanillajs_plugins";
stub1_context = (new DefineWebComponent(TAG, true, [BASE_PATH + "/pouchdb/pouchdb-7.3.0.min.js"]));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = "";
    init = function flx_init (component) {
        var db, fun, obj, p;
        db = new Dexie("TestDatabase");
        (db.version(1).stores)(({friends: "++id, name, age"}));
        fun = (function flx_fun (friends) {
            console.log(friends);
            return null;
        }).bind(this);

        (((((db.friends.where("age").above)(15)).toArray)()).then)(fun);
        obj = ({name: "Kinga", age: 18, street: "East 13:th Street"});
        p = (function flx_p (result) {
            console.log(result);
            return null;
        }).bind(this);

        (db.friends.add(obj).then)(p);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}