var Test;
Test = function () {
    _pyfunc_op_instantiate(this, arguments);
}
Test.prototype._base_class = Object;
Test.prototype.__name__ = "Test";

Test.prototype.__init__ = function () {
    this.value = 0;
    return null;
};

Test.prototype.get_value = function () {
    return this.value;
};


export {Test};