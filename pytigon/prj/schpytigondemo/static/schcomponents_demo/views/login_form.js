var request;
request = function flx_request (param, complete) {
    var auth, context, token;
    token = localStorage.getItem("api_token");
    if (_pyfunc_truthy(token)) {
        auth = true;
    } else {
        auth = false;
    }
    context = ({template: ".", auth: auth});
    complete(context);
    return null;
};

export {request};