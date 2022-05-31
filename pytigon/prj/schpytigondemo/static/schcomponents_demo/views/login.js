var request;
request = function flx_request (param, complete) {
    var _callback, auth, graph;
    graph = get_public_graphql();
    auth = graph("mutation (@autodeclare) { tokenAuth(username: $username, password: $password) { token } }");
    _callback = (function flx__callback (result) {
        var context;
        localStorage.setItem("api_token", result.tokenAuth.token);
        context = ({template: ".", param: result});
        complete(context);
        return null;
    }).bind(this);

    ((auth(({username: param.username, password: param.password}))).then)(_callback);
    return null;
};

export {request};