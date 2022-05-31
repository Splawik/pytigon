var request;
request = function flx_request (param, complete) {
    var _callback, graph, q;
    graph = get_graphql();
    if (_pyfunc_truthy(graph)) {
        q = graph("query { users { id, username, email } }");
        _callback = (function flx__callback (result) {
            var context;
            context = ({template: ".", result: result});
            complete(context);
            return null;
        }).bind(this);

        (q().then)(_callback);
    }
    return null;
};

export {request};