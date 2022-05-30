var request;
request = function flx_request (param, complete) {
    var callback, db;
    db = new PouchDB("test");
    db.put(({_id: ((new Date()).toJSON)(), name: "ABC"}));
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