
var __name__ = "__main__";

function Test() {
    Test.prototype.__init__.apply(this, arguments);
}
Test.prototype.__init__ = function __init__(){
    var self = this;
    self.value = 0;
};
Test.prototype.get_value = function get_value(){
    var self = this;
    return self.value;
};
