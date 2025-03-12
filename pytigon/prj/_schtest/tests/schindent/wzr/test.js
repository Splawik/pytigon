var Test, test, test2;
Test = function () {
    _pyfunc_op_instantiate(this, arguments);
}
Test.prototype._base_class = Object;
Test.prototype.__name__ = "Test";

Test.prototype.__init__ = function () {
    this.a = 1;
    return null;
};

Test.prototype.test = function () {
    if (!(_pyfunc_op_equals(this.a, 1))) { throw _pyfunc_op_error('AssertionError', "_pyfunc_op_equals(this.a, 1)");}
    this.a = 2;
    if (!(_pyfunc_op_equals(this.a, 2))) { throw _pyfunc_op_error('AssertionError', "_pyfunc_op_equals(this.a, 2)");}
    return null;
};


test = function flx_test () {
    var t;
    t = new Test();
    t.test();
    return null;
};

test2 = function flx_test2 () {
    new window.Alert("test");
    return null;
};

export {Test, test, test2};