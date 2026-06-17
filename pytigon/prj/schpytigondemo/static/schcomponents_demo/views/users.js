var request;
request = function flx_request (param, complete) {
    var _callback, data;
    _callback = (function flx__callback (result) {
        var context;
        context = ({template: ".", users: result.data["users"]});
        complete(context);
        return null;
    }).bind(this);

    data = ({query: "query { users { id, username, email } }"});
    window.graphql_client(data, _callback);
    return null;
};

export {request};