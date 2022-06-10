var request;
request = function flx_request (param, complete) {
    var callback, db;
    try {
        (document.getElementsByName("task")[0]).value = "";
    } catch(err_2) {
        {
        }
    }
    db = new PouchDB("todo");
    if (_pyfunc_truthy(param["task"])) {
        db.put(({_id: ((new Date()).toJSON)(), description: param["task"]}));
        navigator.vibrate(1000);
    }
    callback = (function flx_callback (table) {
        var context;
        context = ({template: ".", table: table["rows"]});
        complete(context);
        return null;
    }).bind(this);

    ((db.allDocs(({include_docs: true}))).then)(callback);
    return null;
};

export {request};