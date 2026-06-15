var request;
request = function flx_request (param, complete) {
    var _callback, data;
    _callback = (function flx__callback (result) {
        var context;
        localStorage.setItem("api_token", result.data.tokenAuth.token);
        context = ({template: ".", param: result});
        complete(context);
        return null;
    }).bind(this);

    data = ({query: "mutation ($username: String!, $password: String!) { tokenAuth(username: $username, password: $password) { token } }", variables: ({username: param.username, password: param.password})});
    window.graphql_public_client(data, _callback);
    return null;
};

export {request};