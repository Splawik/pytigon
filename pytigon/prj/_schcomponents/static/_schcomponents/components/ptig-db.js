var BASE_PATH, DB, PROMISE, TAG, TEMPLATE, comp, get_database, init, stub1_context, stub2_err;
TAG = "ptig-db";
BASE_PATH = window.BASE_PATH + "static/_schcomponents/rxdb/";
PROMISE = null;
DB = null;
get_database = async function flx_get_database (module) {
    var PROMISE, initDatabase, todoSchema;
    if ((!_pyfunc_truthy(PROMISE))) {
        todoSchema = ({version: 0, primaryKey: "id", type: "object", properties: ({id: ({type: "string", maxLength: 36}), title: ({type: "string"}), done: ({type: "boolean"}), createdAt: ({type: "string", format: "date-time"})}), required: ["title", "done"]});
        initDatabase = (async function flx_initDatabase () {
            var _pre_insert;
            if ((!_pyfunc_truthy(DB))) {
                DB = await module.createRxDatabase(({name: "pytigon_component", storage: module.getRxStorageDexie()}));
                await DB.addCollections(({todos: ({schema: todoSchema})}));
                _pre_insert = (function flx__pre_insert (docData) {
                    if ((!_pyfunc_truthy(docData.id))) {
                        docData.id = window.v7();
                    }
                    if ((!_pyfunc_truthy(docData.createdAt))) {
                        docData.createdAt = ((new Date()).toISOString)();
                    }
                    return null;
                }).bind(this);

                DB.todos.preInsert(_pre_insert);
            }
            return DB;
        }).bind(this);

        PROMISE = initDatabase();
    }
    return PROMISE;
};

TEMPLATE = '        <div name=\"db\" class=\"db\"></div>\n' +
    '\n' +
    '';
stub1_context = (new DefineWebComponent(TAG, false, [BASE_PATH + "rxdb.js"], [], true));
comp = stub1_context.__enter__();
try {
    comp.options["template"] = TEMPLATE;
    init = function flx_init (component) {
        var div, module, on_error, test2;
        module = component.modules[0];
        div = component.root.querySelector("div");
        on_error = (function flx_on_error (err) {
            console.error(err);
            return null;
        }).bind(this);

        test2 = (function flx_test2 (db) {
            var go, test, uncompletedTodos;
            uncompletedTodos = null;
            test = (async function flx_test () {
                var h, insertResult, newTodos, row, stub3_seq, stub4_itr, table, table2, uncompletedTodos;
                newTodos = [({title: "Buy groceries", isCompleted: false}), ({title: "Read RxDB documentation", isCompleted: true})];
                insertResult = await db.todos.bulkInsert(newTodos);
                uncompletedTodos = await ((_pymeth_find.call(db.todos, (({selector: ({isCompleted: false})})))).exec)();
                table = Array.prototype.slice.call(uncompletedTodos);
                table2 = [];
                h = "<table>";
                stub3_seq = table;
                if ((typeof stub3_seq === "object") && (!Array.isArray(stub3_seq))) { stub3_seq = Object.keys(stub3_seq);}
                for (stub4_itr = 0; stub4_itr < stub3_seq.length; stub4_itr += 1) {
                    row = stub3_seq[stub4_itr];
                    console.log("- ", row.id, row.title, row.createdAt);
                    _pymeth_append.call(table2, ({id: row.id, title: row.title, createdAt: row.createdAt, isCompleted: row.isCompleted}));
                    h = _pyfunc_op_add(h, ((((((("<tr><td>" + row.id) + "</td><td>") + row.title) + "</td><td>") + row.createdAt) + "</td><td>") + row.isCompleted) + "</td></tr>\n");
                }
                h += "</table>";
                div.innerHTML = h;
                return table2;
            }).bind(this);

            go = (function flx_go (table) {
                console.log(table);
                return null;
            }).bind(this);

            (test().then)(go);
            return null;
        }).bind(this);

        (get_database(module).then)(test2);
        return null;
    };

    comp.options["init"] = init;
} catch(err_0)  { stub2_err=err_0;
} finally {
    if (stub2_err) { if (!stub1_context.__exit__(stub2_err.name || "error", stub2_err, null)) { throw stub2_err; }
    } else { stub1_context.__exit__(null, null, null); }
}