var ρσ_iterator_symbol = (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") ? Symbol.iterator : "iterator-Symbol-5d0927e5554349048cf0e3762a228256";
var ρσ_kwargs_symbol = (typeof Symbol === "function") ? Symbol("kwargs-object") : "kwargs-object-Symbol-5d0927e5554349048cf0e3762a228256";
var ρσ_cond_temp, ρσ_expr_temp, ρσ_last_exception;
var ρσ_object_counter = 0;
var ρσ_len;
function ρσ_bool(val) {
    return !!val;
};
Object.defineProperties(ρσ_bool, {
    __argnames__ : {value: ["val"]}
});

function ρσ_print() {
    var parts;
    if (typeof console === "object") {
        parts = [];
        for (var i = 0; i < arguments.length; i++) {
            parts.push(ρσ_str(arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i]));
        }
        console.log(parts.join(" "));
    }
};

function ρσ_int(val, base) {
    var ans;
    ans = parseInt(val, base || 10);
    if (isNaN(ans)) {
        throw new ValueError("Invalid literal for int with base " + (base || 10) + ": " + val);
    }
    return ans;
};
Object.defineProperties(ρσ_int, {
    __argnames__ : {value: ["val", "base"]}
});

function ρσ_float() {
    var ans;
    ans = parseFloat.apply(null, arguments);
    if (isNaN(ans)) {
        throw new ValueError("Could not convert string to float: " + arguments[0]);
    }
    return ans;
};

function ρσ_arraylike_creator() {
    var names;
    names = "Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".split(" ");
    if (typeof HTMLCollection === "function") {
        names = names.concat("HTMLCollection NodeList NamedNodeMap".split(" "));
    }
    return (function() {
        var ρσ_anonfunc = function (x) {
            if (Array.isArray(x) || typeof x === "string" || names.indexOf(Object.prototype.toString.call(x).slice(8, -1)) > -1) {
                return true;
            }
            return false;
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["x"]}
        });
        return ρσ_anonfunc;
    })();
};

function options_object(f) {
    return function () {
        if (typeof arguments[arguments.length - 1] === "object") {
            arguments[ρσ_bound_index(arguments.length - 1, arguments)][ρσ_kwargs_symbol] = true;
        }
        return f.apply(this, arguments);
    };
};
Object.defineProperties(options_object, {
    __argnames__ : {value: ["f"]}
});

function ρσ_id(x) {
    return x.ρσ_object_id;
};
Object.defineProperties(ρσ_id, {
    __argnames__ : {value: ["x"]}
});

function ρσ_dir(item) {
    var arr;
    arr = ρσ_list_decorate([]);
    for (var i in item) {
        arr.push(i);
    }
    return arr;
};
Object.defineProperties(ρσ_dir, {
    __argnames__ : {value: ["item"]}
});

function ρσ_ord(x) {
    var ans, second;
    ans = x.charCodeAt(0);
    if (55296 <= ans && ans <= 56319) {
        second = x.charCodeAt(1);
        if (56320 <= second && second <= 57343) {
            return (ans - 55296) * 1024 + second - 56320 + 65536;
        }
        throw new TypeError("string is missing the low surrogate char");
    }
    return ans;
};
Object.defineProperties(ρσ_ord, {
    __argnames__ : {value: ["x"]}
});

function ρσ_chr(code) {
    if (code <= 65535) {
        return String.fromCharCode(code);
    }
    code -= 65536;
    return String.fromCharCode(55296 + (code >> 10), 56320 + (code & 1023));
};
Object.defineProperties(ρσ_chr, {
    __argnames__ : {value: ["code"]}
});

function ρσ_callable(x) {
    return typeof x === "function";
};
Object.defineProperties(ρσ_callable, {
    __argnames__ : {value: ["x"]}
});

function ρσ_bin(x) {
    var ans;
    if (typeof x !== "number" || x % 1 !== 0) {
        throw new TypeError("integer required");
    }
    ans = x.toString(2);
    if (ans[0] === "-") {
        ans = "-" + "0b" + ans.slice(1);
    } else {
        ans = "0b" + ans;
    }
    return ans;
};
Object.defineProperties(ρσ_bin, {
    __argnames__ : {value: ["x"]}
});

function ρσ_hex(x) {
    var ans;
    if (typeof x !== "number" || x % 1 !== 0) {
        throw new TypeError("integer required");
    }
    ans = x.toString(16);
    if (ans[0] === "-") {
        ans = "-" + "0x" + ans.slice(1);
    } else {
        ans = "0x" + ans;
    }
    return ans;
};
Object.defineProperties(ρσ_hex, {
    __argnames__ : {value: ["x"]}
});

function ρσ_enumerate(iterable) {
    var ans, iterator;
    ans = {"_i":-1};
    ans[ρσ_iterator_symbol] = function () {
        return this;
    };
    if (ρσ_arraylike(iterable)) {
        ans["next"] = function () {
            this._i += 1;
            if (this._i < iterable.length) {
                return {'done':false, 'value':[this._i, iterable[this._i]]};
            }
            return {'done':true};
        };
        return ans;
    }
    if (typeof iterable[ρσ_iterator_symbol] === "function") {
        iterator = (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
        ans["_iterator"] = iterator;
        ans["next"] = function () {
            var r;
            r = this._iterator.next();
            if (r.done) {
                return {'done':true};
            }
            this._i += 1;
            return {'done':false, 'value':[this._i, r.value]};
        };
        return ans;
    }
    return ρσ_enumerate(Object.keys(iterable));
};
Object.defineProperties(ρσ_enumerate, {
    __argnames__ : {value: ["iterable"]}
});

function ρσ_reversed(iterable) {
    var ans;
    if (ρσ_arraylike(iterable)) {
        ans = {"_i": iterable.length};
        ans["next"] = function () {
            this._i -= 1;
            if (this._i > -1) {
                return {'done':false, 'value':iterable[this._i]};
            }
            return {'done':true};
        };
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        return ans;
    }
    throw new TypeError("reversed() can only be called on arrays or strings");
};
Object.defineProperties(ρσ_reversed, {
    __argnames__ : {value: ["iterable"]}
});

function ρσ_iter(iterable) {
    var ans;
    if (typeof iterable[ρσ_iterator_symbol] === "function") {
        return (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
    }
    if (ρσ_arraylike(iterable)) {
        ans = {"_i":-1};
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        ans["next"] = function () {
            this._i += 1;
            if (this._i < iterable.length) {
                return {'done':false, 'value':iterable[this._i]};
            }
            return {'done':true};
        };
        return ans;
    }
    return ρσ_iter(Object.keys(iterable));
};
Object.defineProperties(ρσ_iter, {
    __argnames__ : {value: ["iterable"]}
});

function ρσ_range(start, stop, step) {
    var length, ans;
    if (arguments.length <= 1) {
        stop = start || 0;
        start = 0;
    }
    step = arguments[2] || 1;
    length = Math.max(Math.ceil((stop - start) / step), 0);
    ans = {'_i': start - step, '_idx': -1};
    ans[ρσ_iterator_symbol] = function () {
        return this;
    };
    ans["next"] = function () {
        this._i += step;
        this._idx += 1;
        if (this._idx >= length) {
            return {'done':true};
        }
        return {'done':false, 'value':this._i};
    };
    return ans;
};
Object.defineProperties(ρσ_range, {
    __argnames__ : {value: ["start", "stop", "step"]}
});

function ρσ_getattr(obj, name, defval) {
    var ret;
    try {
        ret = obj[(typeof name === "number" && name < 0) ? obj.length + name : name];
    } catch (ρσ_Exception) {
        ρσ_last_exception = ρσ_Exception;
        if (ρσ_Exception instanceof TypeError) {
            if (defval === undefined) {
                throw new AttributeError("The attribute " + name + " is not present");
            }
            return defval;
        } else {
            throw ρσ_Exception;
        }
    }
    if (ret === undefined && !(name in obj)) {
        if (defval === undefined) {
            throw new AttributeError("The attribute " + name + " is not present");
        }
        ret = defval;
    }
    return ret;
};
Object.defineProperties(ρσ_getattr, {
    __argnames__ : {value: ["obj", "name", "defval"]}
});

function ρσ_setattr(obj, name, value) {
    obj[(typeof name === "number" && name < 0) ? obj.length + name : name] = value;
};
Object.defineProperties(ρσ_setattr, {
    __argnames__ : {value: ["obj", "name", "value"]}
});

function ρσ_hasattr(obj, name) {
    return name in obj;
};
Object.defineProperties(ρσ_hasattr, {
    __argnames__ : {value: ["obj", "name"]}
});

ρσ_len = function () {
    function len(obj) {
        if (ρσ_arraylike(obj)) {
            return obj.length;
        }
        if (typeof obj.__len__ === "function") {
            return obj.__len__();
        }
        if (obj instanceof Set || obj instanceof Map) {
            return obj.size;
        }
        return Object.keys(obj).length;
    };
    Object.defineProperties(len, {
        __argnames__ : {value: ["obj"]}
    });

    function len5(obj) {
        if (ρσ_arraylike(obj)) {
            return obj.length;
        }
        if (typeof obj.__len__ === "function") {
            return obj.__len__();
        }
        return Object.keys(obj).length;
    };
    Object.defineProperties(len5, {
        __argnames__ : {value: ["obj"]}
    });

    return (typeof Set === "function" && typeof Map === "function") ? len : len5;
}();
function ρσ_get_module(name) {
    return ρσ_modules[(typeof name === "number" && name < 0) ? ρσ_modules.length + name : name];
};
Object.defineProperties(ρσ_get_module, {
    __argnames__ : {value: ["name"]}
});

var abs = Math.abs, max = Math.max, min = Math.min, bool = ρσ_bool;
var float = ρσ_float, int = ρσ_int, arraylike = ρσ_arraylike_creator(), ρσ_arraylike = arraylike;
var print = ρσ_print, id = ρσ_id, get_module = ρσ_get_module;
var dir = ρσ_dir, ord = ρσ_ord, chr = ρσ_chr, bin = ρσ_bin, hex = ρσ_hex, callable = ρσ_callable;
var enumerate = ρσ_enumerate, iter = ρσ_iter, reversed = ρσ_reversed, len = ρσ_len;
var range = ρσ_range, getattr = ρσ_getattr, setattr = ρσ_setattr, hasattr = ρσ_hasattr;var ρσ_chain_assign_temp;
function ρσ_equals(a, b) {
    var ρσ_unpack, akeys, bkeys, key;
    if (a === b) {
        return true;
    }
    if (a && typeof a.__eq__ === "function") {
        return a.__eq__(b);
    }
    if (b && typeof b.__eq__ === "function") {
        return b.__eq__(a);
    }
    if (ρσ_arraylike(a) && ρσ_arraylike(b)) {
        if ((a.length !== b.length && (typeof a.length !== "object" || ρσ_not_equals(a.length, b.length)))) {
            return false;
        }
        for (var i=0; i < a.length; i++) {
            if (!((a[(typeof i === "number" && i < 0) ? a.length + i : i] === b[(typeof i === "number" && i < 0) ? b.length + i : i] || typeof a[(typeof i === "number" && i < 0) ? a.length + i : i] === "object" && ρσ_equals(a[(typeof i === "number" && i < 0) ? a.length + i : i], b[(typeof i === "number" && i < 0) ? b.length + i : i])))) {
                return false;
            }
        }
        return true;
    }
    if (typeof a === "object" && typeof b === "object" && (a.constructor === Object && b.constructor === Object || Object.getPrototypeOf(a) === null && Object.getPrototypeOf(b) === null)) {
        ρσ_unpack = [Object.keys(a), Object.keys(b)];
        akeys = ρσ_unpack[0];
        bkeys = ρσ_unpack[1];
        if (akeys.length !== bkeys.length) {
            return false;
        }
        for (var j=0; j < akeys.length; j++) {
            key = akeys[(typeof j === "number" && j < 0) ? akeys.length + j : j];
            if (!((a[(typeof key === "number" && key < 0) ? a.length + key : key] === b[(typeof key === "number" && key < 0) ? b.length + key : key] || typeof a[(typeof key === "number" && key < 0) ? a.length + key : key] === "object" && ρσ_equals(a[(typeof key === "number" && key < 0) ? a.length + key : key], b[(typeof key === "number" && key < 0) ? b.length + key : key])))) {
                return false;
            }
        }
        return true;
    }
    return false;
};
Object.defineProperties(ρσ_equals, {
    __argnames__ : {value: ["a", "b"]}
});

function ρσ_not_equals(a, b) {
    if (a === b) {
        return false;
    }
    if (a && typeof a.__ne__ === "function") {
        return a.__ne__(b);
    }
    if (b && typeof b.__ne__ === "function") {
        return b.__ne__(a);
    }
    return !ρσ_equals(a, b);
};
Object.defineProperties(ρσ_not_equals, {
    __argnames__ : {value: ["a", "b"]}
});

var equals = ρσ_equals;
function ρσ_list_extend(iterable) {
    var start, iterator, result;
    if (Array.isArray(iterable) || typeof iterable === "string") {
        start = this.length;
        this.length += iterable.length;
        for (var i = 0; i < iterable.length; i++) {
            (ρσ_expr_temp = this)[ρσ_bound_index(start + i, ρσ_expr_temp)] = iterable[(typeof i === "number" && i < 0) ? iterable.length + i : i];
        }
    } else {
        iterator = (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
        result = iterator.next();
        while (!result.done) {
            this.push(result.value);
            result = iterator.next();
        }
    }
};
Object.defineProperties(ρσ_list_extend, {
    __argnames__ : {value: ["iterable"]}
});

function ρσ_list_index(val, start, stop) {
    var idx;
    start = start || 0;
    if (start < 0) {
        start = this.length + start;
    }
    if (start < 0) {
        throw new ValueError(val + " is not in list");
    }
    if (stop === undefined) {
        idx = this.indexOf(val, start);
        if (idx === -1) {
            throw new ValueError(val + " is not in list");
        }
        return idx;
    }
    if (stop < 0) {
        stop = this.length + stop;
    }
    for (var i = start; i < stop; i++) {
        if (((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === val || typeof (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === "object" && ρσ_equals((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i], val))) {
            return i;
        }
    }
    throw new ValueError(val + " is not in list");
};
Object.defineProperties(ρσ_list_index, {
    __argnames__ : {value: ["val", "start", "stop"]}
});

function ρσ_list_pop(index) {
    var ans;
    if (this.length === 0) {
        throw new IndexError("list is empty");
    }
    ans = this.splice(index, 1);
    if (!ans.length) {
        throw new IndexError("pop index out of range");
    }
    return ans[0];
};
Object.defineProperties(ρσ_list_pop, {
    __argnames__ : {value: ["index"]}
});

function ρσ_list_remove(value) {
    var idx;
    idx = this.indexOf(value);
    if (idx === -1) {
        throw new ValueError(value + " not in list");
    }
    this.splice(idx, 1);
};
Object.defineProperties(ρσ_list_remove, {
    __argnames__ : {value: ["value"]}
});

function ρσ_list_to_string() {
    return "[" + this.join(", ") + "]";
};

function ρσ_list_insert(index, val) {
    if (index < 0) {
        index += this.length;
    }
    index = min(this.length, max(index, 0));
    if (index === 0) {
        this.unshift(val);
        return;
    }
    for (var i = this.length; i > index; i--) {
        (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] = (ρσ_expr_temp = this)[ρσ_bound_index(i - 1, ρσ_expr_temp)];
    }
    (ρσ_expr_temp = this)[(typeof index === "number" && index < 0) ? ρσ_expr_temp.length + index : index] = val;
};
Object.defineProperties(ρσ_list_insert, {
    __argnames__ : {value: ["index", "val"]}
});

function ρσ_list_copy() {
    return ρσ_list_constructor(this);
};

function ρσ_list_clear() {
    this.length = 0;
};

function ρσ_list_as_array() {
    return Array.prototype.slice.call(this);
};

function ρσ_list_count(value) {
    return this.reduce((function() {
        var ρσ_anonfunc = function (n, val) {
            return n + (val === value);
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["n", "val"]}
        });
        return ρσ_anonfunc;
    })(), 0);
};
Object.defineProperties(ρσ_list_count, {
    __argnames__ : {value: ["value"]}
});

function ρσ_list_sort_key(value) {
    var t;
    t = typeof value;
    if (t === "string" || t === "number") {
        return value;
    }
    return value.toString();
};
Object.defineProperties(ρσ_list_sort_key, {
    __argnames__ : {value: ["value"]}
});

function ρσ_list_sort_cmp(a, b) {
    if (a < b) {
        return -1;
    }
    if (a > b) {
        return 1;
    }
    return 0;
};
Object.defineProperties(ρσ_list_sort_cmp, {
    __argnames__ : {value: ["a", "b"]}
});

function ρσ_list_sort(key, reverse) {
    var mult, keymap, k;
    key = key || ρσ_list_sort_key;
    mult = (reverse) ? -1 : 1;
    keymap = dict();
    for (var i=0; i < this.length; i++) {
        k = (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i];
        keymap.set(k, key(k));
    }
    this.sort((function() {
        var ρσ_anonfunc = function (a, b) {
            return mult * ρσ_list_sort_cmp(keymap.get(a), keymap.get(b));
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["a", "b"]}
        });
        return ρσ_anonfunc;
    })());
};
Object.defineProperties(ρσ_list_sort, {
    __argnames__ : {value: ["key", "reverse"]}
});

function ρσ_list_concat() {
    var ans;
    ans = Array.prototype.concat.apply(this, arguments);
    ρσ_list_decorate(ans);
    return ans;
};

function ρσ_list_slice() {
    var ans;
    ans = Array.prototype.slice.apply(this, arguments);
    ρσ_list_decorate(ans);
    return ans;
};

function ρσ_list_iterator(value) {
    var self;
    self = this;
    return (function(){
        var ρσ_d = {};
        ρσ_d["_i"] = -1;
        ρσ_d["_list"] = self;
        ρσ_d["next"] = function () {
            this._i += 1;
            if (this._i >= this._list.length) {
                return (function(){
                    var ρσ_d = {};
                    ρσ_d["done"] = true;
                    return ρσ_d;
                }).call(this);
            }
            return (function(){
                var ρσ_d = {};
                ρσ_d["done"] = false;
                ρσ_d["value"] = (ρσ_expr_temp = this._list)[ρσ_bound_index(this._i, ρσ_expr_temp)];
                return ρσ_d;
            }).call(this);
        };
        return ρσ_d;
    }).call(this);
};
Object.defineProperties(ρσ_list_iterator, {
    __argnames__ : {value: ["value"]}
});

function ρσ_list_len() {
    return this.length;
};

function ρσ_list_contains(val) {
    for (var i = 0; i < this.length; i++) {
        if (((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === val || typeof (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === "object" && ρσ_equals((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i], val))) {
            return true;
        }
    }
    return false;
};
Object.defineProperties(ρσ_list_contains, {
    __argnames__ : {value: ["val"]}
});

function ρσ_list_eq(other) {
    if (!ρσ_arraylike(other)) {
        return false;
    }
    if ((this.length !== other.length && (typeof this.length !== "object" || ρσ_not_equals(this.length, other.length)))) {
        return false;
    }
    for (var i = 0; i < this.length; i++) {
        if (!(((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === other[(typeof i === "number" && i < 0) ? other.length + i : i] || typeof (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] === "object" && ρσ_equals((ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i], other[(typeof i === "number" && i < 0) ? other.length + i : i])))) {
            return false;
        }
    }
    return true;
};
Object.defineProperties(ρσ_list_eq, {
    __argnames__ : {value: ["other"]}
});

function ρσ_list_decorate(ans) {
    ans.append = Array.prototype.push;
    ans.toString = ρσ_list_to_string;
    ans.inspect = ρσ_list_to_string;
    ans.extend = ρσ_list_extend;
    ans.index = ρσ_list_index;
    ans.pypop = ρσ_list_pop;
    ans.remove = ρσ_list_remove;
    ans.insert = ρσ_list_insert;
    ans.copy = ρσ_list_copy;
    ans.clear = ρσ_list_clear;
    ans.count = ρσ_list_count;
    ans.concat = ρσ_list_concat;
    ans.pysort = ρσ_list_sort;
    ans.slice = ρσ_list_slice;
    ans.as_array = ρσ_list_as_array;
    ans.__len__ = ρσ_list_len;
    ans.__contains__ = ρσ_list_contains;
    ans.__eq__ = ρσ_list_eq;
    ans.constructor = ρσ_list_constructor;
    if (typeof ans[ρσ_iterator_symbol] !== "function") {
        ans[ρσ_iterator_symbol] = ρσ_list_iterator;
    }
    return ans;
};
Object.defineProperties(ρσ_list_decorate, {
    __argnames__ : {value: ["ans"]}
});

function ρσ_list_constructor(iterable) {
    var ans, iterator, result;
    if (iterable === undefined) {
        ans = [];
    } else if (ρσ_arraylike(iterable)) {
        ans = new Array(iterable.length);
        for (var i = 0; i < iterable.length; i++) {
            ans[(typeof i === "number" && i < 0) ? ans.length + i : i] = iterable[(typeof i === "number" && i < 0) ? iterable.length + i : i];
        }
    } else if (typeof iterable[ρσ_iterator_symbol] === "function") {
        iterator = (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
        ans = ρσ_list_decorate([]);
        result = iterator.next();
        while (!result.done) {
            ans.push(result.value);
            result = iterator.next();
        }
    } else if (typeof iterable === "number") {
        ans = new Array(iterable);
    } else {
        ans = Object.keys(iterable);
    }
    return ρσ_list_decorate(ans);
};
Object.defineProperties(ρσ_list_constructor, {
    __argnames__ : {value: ["iterable"]}
});

ρσ_list_constructor.__name__ = "list";
var list = ρσ_list_constructor, list_wrap = ρσ_list_decorate;
function sorted() {
    var iterable = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
    var key = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? sorted.__defaults__.key : arguments[1];
    var reverse = (arguments[2] === undefined || ( 2 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? sorted.__defaults__.reverse : arguments[2];
    var ρσ_kwargs_obj = arguments[arguments.length-1];
    if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "key")){
        key = ρσ_kwargs_obj.key;
    }
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "reverse")){
        reverse = ρσ_kwargs_obj.reverse;
    }
    var ans;
    ans = ρσ_list_constructor(iterable);
    ans.pysort(key, reverse);
    return ans;
};
Object.defineProperties(sorted, {
    __defaults__ : {value: {key:null, reverse:false}},
    __handles_kwarg_interpolation__ : {value: true},
    __argnames__ : {value: ["iterable", "key", "reverse"]}
});

var ρσ_global_object_id = 0, ρσ_set_implementation;
function ρσ_set_keyfor(x) {
    var t, ans;
    t = typeof x;
    if (t === "string" || t === "number" || t === "boolean") {
        return "_" + t[0] + x;
    }
    if (x === null) {
        return "__!@#$0";
    }
    ans = x.ρσ_hash_key_prop;
    if (ans === undefined) {
        ans = "_!@#$" + (++ρσ_global_object_id);
        Object.defineProperty(x, "ρσ_hash_key_prop", (function(){
            var ρσ_d = {};
            ρσ_d["value"] = ans;
            return ρσ_d;
        }).call(this));
    }
    return ans;
};
Object.defineProperties(ρσ_set_keyfor, {
    __argnames__ : {value: ["x"]}
});

function ρσ_set_polyfill() {
    this._store = {};
    this.size = 0;
};

ρσ_set_polyfill.prototype.add = (function() {
    var ρσ_anonfunc = function (x) {
        var key;
        key = ρσ_set_keyfor(x);
        if (!Object.prototype.hasOwnProperty.call(this._store, key)) {
            this.size += 1;
            (ρσ_expr_temp = this._store)[(typeof key === "number" && key < 0) ? ρσ_expr_temp.length + key : key] = x;
        }
        return this;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set_polyfill.prototype.clear = (function() {
    var ρσ_anonfunc = function (x) {
        this._store = {};
        this.size = 0;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set_polyfill.prototype.delete = (function() {
    var ρσ_anonfunc = function (x) {
        var key;
        key = ρσ_set_keyfor(x);
        if (Object.prototype.hasOwnProperty.call(this._store, key)) {
            this.size -= 1;
            delete this._store[key];
            return true;
        }
        return false;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set_polyfill.prototype.has = (function() {
    var ρσ_anonfunc = function (x) {
        return Object.prototype.hasOwnProperty.call(this._store, ρσ_set_keyfor(x));
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set_polyfill.prototype.values = (function() {
    var ρσ_anonfunc = function (x) {
        var ans;
        ans = {'_keys': Object.keys(this._store), '_i':-1, '_s':this._store};
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        ans["next"] = function () {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {'done': true};
            }
            return {'done':false, 'value':this._s[this._keys[this._i]]};
        };
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
if (typeof Set !== "function" || typeof Set.prototype.delete !== "function") {
    ρσ_set_implementation = ρσ_set_polyfill;
} else {
    ρσ_set_implementation = Set;
}
function ρσ_set(iterable) {
    var ans, s, iterator, result, keys;
    if (ρσ_instanceof(this, ρσ_set)) {
        this.jsset = new ρσ_set_implementation;
        ans = this;
        if (iterable === undefined) {
            return ans;
        }
        s = ans.jsset;
        if (ρσ_arraylike(iterable)) {
            for (var i = 0; i < iterable.length; i++) {
                s.add(iterable[(typeof i === "number" && i < 0) ? iterable.length + i : i]);
            }
        } else if (typeof iterable[ρσ_iterator_symbol] === "function") {
            iterator = (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
            result = iterator.next();
            while (!result.done) {
                s.add(result.value);
                result = iterator.next();
            }
        } else {
            keys = Object.keys(iterable);
            for (var j=0; j < keys.length; j++) {
                s.add(keys[(typeof j === "number" && j < 0) ? keys.length + j : j]);
            }
        }
        return ans;
    } else {
        return new ρσ_set(iterable);
    }
};
Object.defineProperties(ρσ_set, {
    __argnames__ : {value: ["iterable"]}
});

ρσ_set.prototype.__name__ = "set";
Object.defineProperties(ρσ_set.prototype, (function(){
    var ρσ_d = {};
    ρσ_d["length"] = (function(){
        var ρσ_d = {};
        ρσ_d["get"] = function () {
            return this.jsset.size;
        };
        return ρσ_d;
    }).call(this);
    ρσ_d["size"] = (function(){
        var ρσ_d = {};
        ρσ_d["get"] = function () {
            return this.jsset.size;
        };
        return ρσ_d;
    }).call(this);
    return ρσ_d;
}).call(this));
ρσ_set.prototype.__len__ = function () {
    return this.jsset.size;
};
ρσ_chain_assign_temp = (function() {
    var ρσ_anonfunc = function (x) {
        return this.jsset.has(x);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.has = ρσ_chain_assign_temp;
ρσ_set.prototype.__contains__ = ρσ_chain_assign_temp;
;
ρσ_set.prototype.add = (function() {
    var ρσ_anonfunc = function (x) {
        this.jsset.add(x);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.clear = function () {
    this.jsset.clear();
};
ρσ_set.prototype.copy = function () {
    return ρσ_set(this);
};
ρσ_set.prototype.discard = (function() {
    var ρσ_anonfunc = function (x) {
        this.jsset.delete(x);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype[ρσ_iterator_symbol] = function () {
    return this.jsset.values();
};
ρσ_set.prototype.difference = function () {
    var ans, s, iterator, r, x, has;
    ans = new ρσ_set;
    s = ans.jsset;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        has = false;
        for (var i = 0; i < arguments.length; i++) {
            if (arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i].has(x)) {
                has = true;
                break;
            }
        }
        if (!has) {
            s.add(x);
        }
        r = iterator.next();
    }
    return ans;
};
ρσ_set.prototype.difference_update = function () {
    var s, remove, iterator, r, x;
    s = this.jsset;
    remove = [];
    iterator = s.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        for (var i = 0; i < arguments.length; i++) {
            if (arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i].has(x)) {
                remove.push(x);
                break;
            }
        }
        r = iterator.next();
    }
    for (var j = 0; j < remove.length; j++) {
        s.delete(remove[(typeof j === "number" && j < 0) ? remove.length + j : j]);
    }
};
ρσ_set.prototype.intersection = function () {
    var ans, s, iterator, r, x, has;
    ans = new ρσ_set;
    s = ans.jsset;
    iterator = this.jsset.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        has = true;
        for (var i = 0; i < arguments.length; i++) {
            if (!arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i].has(x)) {
                has = false;
                break;
            }
        }
        if (has) {
            s.add(x);
        }
        r = iterator.next();
    }
    return ans;
};
ρσ_set.prototype.intersection_update = function () {
    var s, remove, iterator, r, x;
    s = this.jsset;
    remove = [];
    iterator = s.values();
    r = iterator.next();
    while (!r.done) {
        x = r.value;
        for (var i = 0; i < arguments.length; i++) {
            if (!arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i].has(x)) {
                remove.push(x);
                break;
            }
        }
        r = iterator.next();
    }
    for (var j = 0; j < remove.length; j++) {
        s.delete(remove[(typeof j === "number" && j < 0) ? remove.length + j : j]);
    }
};
ρσ_set.prototype.isdisjoint = (function() {
    var ρσ_anonfunc = function (other) {
        var iterator, r, x;
        iterator = this.jsset.values();
        r = iterator.next();
        while (!r.done) {
            x = r.value;
            if (other.has(x)) {
                return false;
            }
            r = iterator.next();
        }
        return true;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.issubset = (function() {
    var ρσ_anonfunc = function (other) {
        var iterator, r, x;
        iterator = this.jsset.values();
        r = iterator.next();
        while (!r.done) {
            x = r.value;
            if (!other.has(x)) {
                return false;
            }
            r = iterator.next();
        }
        return true;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.issuperset = (function() {
    var ρσ_anonfunc = function (other) {
        var s, iterator, r, x;
        s = this.jsset;
        iterator = other.jsset.values();
        r = iterator.next();
        while (!r.done) {
            x = r.value;
            if (!s.has(x)) {
                return false;
            }
            r = iterator.next();
        }
        return true;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.pop = function () {
    var iterator, r;
    iterator = this.jsset.values();
    r = iterator.next();
    if (r.done) {
        throw new KeyError("pop from an empty set");
    }
    this.jsset.delete(r.value);
    return r.value;
};
ρσ_set.prototype.remove = (function() {
    var ρσ_anonfunc = function (x) {
        if (!this.jsset.delete(x)) {
            throw new KeyError(x.toString());
        }
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.symmetric_difference = (function() {
    var ρσ_anonfunc = function (other) {
        return this.union(other).difference(this.intersection(other));
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.symmetric_difference_update = (function() {
    var ρσ_anonfunc = function (other) {
        var common;
        common = this.intersection(other);
        this.update(other);
        this.difference_update(common);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_set.prototype.union = function () {
    var ans;
    ans = ρσ_set(this);
    ans.update.apply(ans, arguments);
    return ans;
};
ρσ_set.prototype.update = function () {
    var s, iterator, r;
    s = this.jsset;
    for (var i=0; i < arguments.length; i++) {
        iterator = arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i][ρσ_iterator_symbol]();
        r = iterator.next();
        while (!r.done) {
            s.add(r.value);
            r = iterator.next();
        }
    }
};
ρσ_chain_assign_temp = function () {
    return "{" + list(this).join(", ") + "}";
};
ρσ_set.prototype.toString = ρσ_chain_assign_temp;
ρσ_set.prototype.inspect = ρσ_chain_assign_temp;
;
ρσ_set.prototype.__eq__ = (function() {
    var ρσ_anonfunc = function (other) {
        var iterator, r;
        if (!(ρσ_instanceof(other, this.constructor))) {
            return false;
        }
        if (other.size !== this.size) {
            return false;
        }
        if (other.size === 0) {
            return true;
        }
        iterator = other[ρσ_iterator_symbol]();
        r = iterator.next();
        while (!r.done) {
            if (!this.has(r.value)) {
                return false;
            }
            r = iterator.next();
        }
        return true;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
function ρσ_set_wrap(x) {
    var ans;
    ans = new ρσ_set;
    ans.jsset = x;
    return ans;
};
Object.defineProperties(ρσ_set_wrap, {
    __argnames__ : {value: ["x"]}
});

var set = ρσ_set, set_wrap = ρσ_set_wrap;
var ρσ_dict_implementation;
function ρσ_dict_polyfill() {
    this._store = {};
    this.size = 0;
};

ρσ_dict_polyfill.prototype.set = (function() {
    var ρσ_anonfunc = function (x, value) {
        var key;
        key = ρσ_set_keyfor(x);
        if (!Object.prototype.hasOwnProperty.call(this._store, key)) {
            this.size += 1;
        }
        (ρσ_expr_temp = this._store)[(typeof key === "number" && key < 0) ? ρσ_expr_temp.length + key : key] = [x, value];
        return this;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x", "value"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.clear = (function() {
    var ρσ_anonfunc = function (x) {
        this._store = {};
        this.size = 0;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.delete = (function() {
    var ρσ_anonfunc = function (x) {
        var key;
        key = ρσ_set_keyfor(x);
        if (Object.prototype.hasOwnProperty.call(this._store, key)) {
            this.size -= 1;
            delete this._store[key];
            return true;
        }
        return false;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.has = (function() {
    var ρσ_anonfunc = function (x) {
        return Object.prototype.hasOwnProperty.call(this._store, ρσ_set_keyfor(x));
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.get = (function() {
    var ρσ_anonfunc = function (x) {
        try {
            return (ρσ_expr_temp = this._store)[ρσ_bound_index(ρσ_set_keyfor(x), ρσ_expr_temp)][1];
        } catch (ρσ_Exception) {
            ρσ_last_exception = ρσ_Exception;
            if (ρσ_Exception instanceof TypeError) {
                return undefined;
            } else {
                throw ρσ_Exception;
            }
        }
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.values = (function() {
    var ρσ_anonfunc = function (x) {
        var ans;
        ans = {'_keys': Object.keys(this._store), '_i':-1, '_s':this._store};
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        ans["next"] = function () {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {'done': true};
            }
            return {'done':false, 'value':this._s[this._keys[this._i]][1]};
        };
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.keys = (function() {
    var ρσ_anonfunc = function (x) {
        var ans;
        ans = {'_keys': Object.keys(this._store), '_i':-1, '_s':this._store};
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        ans["next"] = function () {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {'done': true};
            }
            return {'done':false, 'value':this._s[this._keys[this._i]][0]};
        };
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict_polyfill.prototype.entries = (function() {
    var ρσ_anonfunc = function (x) {
        var ans;
        ans = {'_keys': Object.keys(this._store), '_i':-1, '_s':this._store};
        ans[ρσ_iterator_symbol] = function () {
            return this;
        };
        ans["next"] = function () {
            this._i += 1;
            if (this._i >= this._keys.length) {
                return {'done': true};
            }
            return {'done':false, 'value':this._s[this._keys[this._i]]};
        };
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
if (typeof Map !== "function" || typeof Map.prototype.delete !== "function") {
    ρσ_dict_implementation = ρσ_dict_polyfill;
} else {
    ρσ_dict_implementation = Map;
}
function ρσ_dict(iterable) {
    if (ρσ_instanceof(this, ρσ_dict)) {
        this.jsmap = new ρσ_dict_implementation;
        if (iterable !== undefined) {
            this.update(iterable);
        }
        return this;
    } else {
        return new ρσ_dict(iterable);
    }
};
Object.defineProperties(ρσ_dict, {
    __argnames__ : {value: ["iterable"]}
});

ρσ_dict.prototype.__name__ = "dict";
Object.defineProperties(ρσ_dict.prototype, (function(){
    var ρσ_d = {};
    ρσ_d["length"] = (function(){
        var ρσ_d = {};
        ρσ_d["get"] = function () {
            return this.jsmap.size;
        };
        return ρσ_d;
    }).call(this);
    ρσ_d["size"] = (function(){
        var ρσ_d = {};
        ρσ_d["get"] = function () {
            return this.jsmap.size;
        };
        return ρσ_d;
    }).call(this);
    return ρσ_d;
}).call(this));
ρσ_dict.prototype.__len__ = function () {
    return this.jsmap.size;
};
ρσ_chain_assign_temp = (function() {
    var ρσ_anonfunc = function (x) {
        return this.jsmap.has(x);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["x"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.has = ρσ_chain_assign_temp;
ρσ_dict.prototype.__contains__ = ρσ_chain_assign_temp;
;
ρσ_chain_assign_temp = (function() {
    var ρσ_anonfunc = function (key, value) {
        this.jsmap.set(key, value);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key", "value"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.set = ρσ_chain_assign_temp;
ρσ_dict.prototype.__setitem__ = ρσ_chain_assign_temp;
;
ρσ_dict.prototype.__delitem__ = (function() {
    var ρσ_anonfunc = function (key) {
        this.jsmap.delete(key);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.clear = function () {
    this.jsmap.clear();
};
ρσ_dict.prototype.copy = function () {
    return ρσ_dict(this);
};
ρσ_dict.prototype.keys = function () {
    return this.jsmap.keys();
};
ρσ_dict.prototype.values = function () {
    return this.jsmap.values();
};
ρσ_chain_assign_temp = function () {
    return this.jsmap.entries();
};
ρσ_dict.prototype.items = ρσ_chain_assign_temp;
ρσ_dict.prototype.entries = ρσ_chain_assign_temp;
;
ρσ_dict.prototype[ρσ_iterator_symbol] = function () {
    return this.jsmap.keys();
};
ρσ_dict.prototype.__getitem__ = (function() {
    var ρσ_anonfunc = function (key) {
        var ans;
        ans = this.jsmap.get(key);
        if (ans === undefined && !this.jsmap.has(key)) {
            throw new KeyError(key + "");
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.get = (function() {
    var ρσ_anonfunc = function (key, defval) {
        var ans;
        ans = this.jsmap.get(key);
        if (ans === undefined && !this.jsmap.has(key)) {
            return (defval === undefined) ? null : defval;
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key", "defval"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.set_default = (function() {
    var ρσ_anonfunc = function (key, defval) {
        var j;
        j = this.jsmap;
        if (!j.has(key)) {
            j.set(key, defval);
            return defval;
        }
        return j.get(key);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key", "defval"]}
    });
    return ρσ_anonfunc;
})();
ρσ_chain_assign_temp = (function() {
    var ρσ_anonfunc = function () {
        var iterable = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
        var value = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? ρσ_anonfunc.__defaults__.value : arguments[1];
        var ρσ_kwargs_obj = arguments[arguments.length-1];
        if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
        if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "value")){
            value = ρσ_kwargs_obj.value;
        }
        var ans, iterator, r;
        ans = ρσ_dict();
        iterator = iter(iterable);
        r = iterator.next();
        while (!r.done) {
            ans.set(r.value, value);
            r = iterator.next();
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __defaults__ : {value: {value:null}},
        __handles_kwarg_interpolation__ : {value: true},
        __argnames__ : {value: ["iterable", "value"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.fromkeys = ρσ_chain_assign_temp;
ρσ_dict.prototype.fromkeys = ρσ_chain_assign_temp;
;
ρσ_dict.prototype.pop = (function() {
    var ρσ_anonfunc = function (key, defval) {
        var ans;
        ans = this.jsmap.get(key);
        if (ans === undefined && !this.jsmap.has(key)) {
            if (defval === undefined) {
                throw new KeyError(key);
            }
            return defval;
        }
        this.jsmap.delete(key);
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["key", "defval"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.popitem = function () {
    var r;
    r = this.jsmap.entries().next();
    if (r.done) {
        throw new KeyError("dict is empty");
    }
    this.jsmap.delete(r.value[0]);
    return r.value;
};
ρσ_dict.prototype.update = function () {
    var m, iterable, iterator, result, keys;
    if (arguments.length === 0) {
        return;
    }
    m = this.jsmap;
    iterable = arguments[0];
    if (Array.isArray(iterable)) {
        for (var i = 0; i < iterable.length; i++) {
            m.set(iterable[(typeof i === "number" && i < 0) ? iterable.length + i : i][0], iterable[(typeof i === "number" && i < 0) ? iterable.length + i : i][1]);
        }
    } else if (ρσ_instanceof(iterable, ρσ_dict)) {
        iterator = iterable.items();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else if (typeof Map === "function" && ρσ_instanceof(iterable, Map)) {
        iterator = iterable.entries();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else if (typeof iterable[ρσ_iterator_symbol] === "function") {
        iterator = iterable[ρσ_iterator_symbol]();
        result = iterator.next();
        while (!result.done) {
            m.set(result.value[0], result.value[1]);
            result = iterator.next();
        }
    } else {
        keys = Object.keys(iterable);
        for (var j=0; j < keys.length; j++) {
            if (keys[(typeof j === "number" && j < 0) ? keys.length + j : j] !== ρσ_iterator_symbol) {
                m.set(keys[(typeof j === "number" && j < 0) ? keys.length + j : j], iterable[ρσ_bound_index(keys[(typeof j === "number" && j < 0) ? keys.length + j : j], iterable)]);
            }
        }
    }
    if (arguments.length > 1) {
        ρσ_dict.prototype.update.call(this, arguments[1]);
    }
};
ρσ_chain_assign_temp = function () {
    var entries, iterator, r;
    entries = [];
    iterator = this.jsmap.entries();
    r = iterator.next();
    while (!r.done) {
        entries.push(r.value[0] + ": " + r.value[1]);
        r = iterator.next();
    }
    return "{" + entries.join(", ") + "}";
};
ρσ_dict.prototype.toString = ρσ_chain_assign_temp;
ρσ_dict.prototype.inspect = ρσ_chain_assign_temp;
;
ρσ_dict.prototype.__eq__ = (function() {
    var ρσ_anonfunc = function (other) {
        var iterator, r, x;
        if (!(ρσ_instanceof(other, this.constructor))) {
            return false;
        }
        if (other.size !== this.size) {
            return false;
        }
        if (other.size === 0) {
            return true;
        }
        iterator = other.items();
        r = iterator.next();
        while (!r.done) {
            x = this.jsmap.get(r.value[0]);
            if (x === undefined && !this.jsmap.has(r.value[0]) || x !== r.value[1]) {
                return false;
            }
            r = iterator.next();
        }
        return true;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
ρσ_dict.prototype.as_object = (function() {
    var ρσ_anonfunc = function (other) {
        var ans, iterator, r;
        ans = {};
        iterator = this.jsmap.entries();
        r = iterator.next();
        while (!r.done) {
            ans[ρσ_bound_index(r.value[0], ans)] = r.value[1];
            r = iterator.next();
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["other"]}
    });
    return ρσ_anonfunc;
})();
function ρσ_dict_wrap(x) {
    var ans;
    ans = new ρσ_dict;
    ans.jsmap = x;
    return ans;
};
Object.defineProperties(ρσ_dict_wrap, {
    __argnames__ : {value: ["x"]}
});

var dict = ρσ_dict, dict_wrap = ρσ_dict_wrap;var NameError;
NameError = ReferenceError;
function Exception() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    Exception.prototype.__init__.apply(this, arguments);
}
ρσ_extends(Exception, Error);
Exception.prototype.__init__ = function __init__(message) {
    var self = this;
    self.message = message;
    self.stack = (new Error).stack;
    self.name = self.constructor.name;
};
Object.defineProperties(Exception.prototype.__init__, {
    __argnames__ : {value: ["message"]}
});
Exception.__argnames__ = Exception.prototype.__init__.__argnames__;
Exception.__handles_kwarg_interpolation__ = Exception.prototype.__init__.__handles_kwarg_interpolation__;
Exception.prototype.__repr__ = function __repr__() {
    var self = this;
    return self.name + ": " + self.message;
};
Object.defineProperties(Exception.prototype.__repr__, {
    __argnames__ : {value: []}
});
Exception.prototype.__str__ = function __str__ () {
    if(Error.prototype.__str__) return Error.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(Exception.prototype, "__bases__", {value: [Error]});

function AttributeError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    AttributeError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(AttributeError, Exception);
AttributeError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
AttributeError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
AttributeError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(AttributeError.prototype, "__bases__", {value: [Exception]});


function IndexError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    IndexError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(IndexError, Exception);
IndexError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
IndexError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
IndexError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(IndexError.prototype, "__bases__", {value: [Exception]});


function KeyError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    KeyError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(KeyError, Exception);
KeyError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
KeyError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
KeyError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(KeyError.prototype, "__bases__", {value: [Exception]});


function ValueError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    ValueError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(ValueError, Exception);
ValueError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
ValueError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
ValueError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(ValueError.prototype, "__bases__", {value: [Exception]});


function UnicodeDecodeError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    UnicodeDecodeError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(UnicodeDecodeError, Exception);
UnicodeDecodeError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
UnicodeDecodeError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
UnicodeDecodeError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(UnicodeDecodeError.prototype, "__bases__", {value: [Exception]});


function AssertionError() {
    if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
    AssertionError.prototype.__init__.apply(this, arguments);
}
ρσ_extends(AssertionError, Exception);
AssertionError.prototype.__init__ = function __init__ () {
    Exception.prototype.__init__ && Exception.prototype.__init__.apply(this, arguments);
};
AssertionError.prototype.__repr__ = function __repr__ () {
    if(Exception.prototype.__repr__) return Exception.prototype.__repr__.call(this);
    return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
};
AssertionError.prototype.__str__ = function __str__ () {
    if(Exception.prototype.__str__) return Exception.prototype.__str__.call(this);
return this.__repr__();
};
Object.defineProperty(AssertionError.prototype, "__bases__", {value: [Exception]});

var ρσ_in, ρσ_desugar_kwargs, ρσ_exists;
function ρσ_eslice(arr, step, start, end) {
    var is_string;
    if (typeof arr === "string" || ρσ_instanceof(arr, String)) {
        is_string = true;
        arr = arr.split("");
    }
    if (step < 0) {
        step = -step;
        arr = arr.slice().reverse();
        if (typeof start !== "undefined") {
            start = arr.length - start - 1;
        }
        if (typeof end !== "undefined") {
            end = arr.length - end - 1;
        }
    }
    if (typeof start === "undefined") {
        start = 0;
    }
    if (typeof end === "undefined") {
        end = arr.length;
    }
    arr = arr.slice(start, end).filter((function() {
        var ρσ_anonfunc = function (e, i) {
            return i % step === 0;
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["e", "i"]}
        });
        return ρσ_anonfunc;
    })());
    if (is_string) {
        arr = arr.join("");
    }
    return arr;
};
Object.defineProperties(ρσ_eslice, {
    __argnames__ : {value: ["arr", "step", "start", "end"]}
});

function ρσ_delslice(arr, step, start, end) {
    var is_string, ρσ_unpack, indices;
    if (typeof arr === "string" || ρσ_instanceof(arr, String)) {
        is_string = true;
        arr = arr.split("");
    }
    if (step < 0) {
        if (typeof start === "undefined") {
            start = arr.length;
        }
        if (typeof end === "undefined") {
            end = 0;
        }
        ρσ_unpack = [end, start, -step];
        start = ρσ_unpack[0];
        end = ρσ_unpack[1];
        step = ρσ_unpack[2];
    }
    if (typeof start === "undefined") {
        start = 0;
    }
    if (typeof end === "undefined") {
        end = arr.length;
    }
    if (step === 1) {
        arr.splice(start, end - start);
    } else {
        if (end > start) {
            indices = [];
            for (var i = start; i < end; i += step) {
                indices.push(i);
            }
            for (var i = indices.length - 1; i >= 0; i--) {
                arr.splice(indices[(typeof i === "number" && i < 0) ? indices.length + i : i], 1);
            }
        }
    }
    if (is_string) {
        arr = arr.join("");
    }
    return arr;
};
Object.defineProperties(ρσ_delslice, {
    __argnames__ : {value: ["arr", "step", "start", "end"]}
});

function ρσ_flatten(arr) {
    var ans, value;
    ans = ρσ_list_decorate([]);
    for (var i=0; i < arr.length; i++) {
        value = arr[(typeof i === "number" && i < 0) ? arr.length + i : i];
        if (Array.isArray(value)) {
            ans = ans.concat(ρσ_flatten(value));
        } else {
            ans.push(value);
        }
    }
    return ans;
};
Object.defineProperties(ρσ_flatten, {
    __argnames__ : {value: ["arr"]}
});

function ρσ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.constructor = child;
};
Object.defineProperties(ρσ_extends, {
    __argnames__ : {value: ["child", "parent"]}
});

ρσ_in = function () {
    if (typeof Map === "function" && typeof Set === "function") {
        return (function() {
            var ρσ_anonfunc = function (val, arr) {
                if (typeof arr === "string") {
                    return arr.indexOf(val) !== -1;
                }
                if (typeof arr.__contains__ === "function") {
                    return arr.__contains__(val);
                }
                if (ρσ_instanceof.apply(null, [arr, Map, Set])) {
                    return arr.has(val);
                }
                if (ρσ_arraylike(arr)) {
                    return ρσ_list_contains.call(arr, val);
                }
                return Object.prototype.hasOwnProperty.call(arr, val);
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["val", "arr"]}
            });
            return ρσ_anonfunc;
        })();
    }
    return (function() {
        var ρσ_anonfunc = function (val, arr) {
            if (typeof arr === "string") {
                return arr.indexOf(val) !== -1;
            }
            if (typeof arr.__contains__ === "function") {
                return arr.__contains__(val);
            }
            if (ρσ_arraylike(arr)) {
                return ρσ_list_contains.call(arr, val);
            }
            return Object.prototype.hasOwnProperty.call(arr, val);
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["val", "arr"]}
        });
        return ρσ_anonfunc;
    })();
}();
function ρσ_Iterable(iterable) {
    var iterator, ans, result;
    if (ρσ_arraylike(iterable)) {
        return iterable;
    }
    if (typeof iterable[ρσ_iterator_symbol] === "function") {
        iterator = (typeof Map === "function" && ρσ_instanceof(iterable, Map)) ? iterable.keys() : iterable[ρσ_iterator_symbol]();
        ans = ρσ_list_decorate([]);
        result = iterator.next();
        while (!result.done) {
            ans.push(result.value);
            result = iterator.next();
        }
        return ans;
    }
    return Object.keys(iterable);
};
Object.defineProperties(ρσ_Iterable, {
    __argnames__ : {value: ["iterable"]}
});

ρσ_desugar_kwargs = function () {
    if (typeof Object.assign === "function") {
        return function () {
            var ans;
            ans = Object.create(null);
            ans[ρσ_kwargs_symbol] = true;
            for (var i = 0; i < arguments.length; i++) {
                Object.assign(ans, arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i]);
            }
            return ans;
        };
    }
    return function () {
        var ans, keys;
        ans = Object.create(null);
        ans[ρσ_kwargs_symbol] = true;
        for (var i = 0; i < arguments.length; i++) {
            keys = Object.keys(arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i]);
            for (var j = 0; j < keys.length; j++) {
                ans[ρσ_bound_index(keys[(typeof j === "number" && j < 0) ? keys.length + j : j], ans)] = (ρσ_expr_temp = arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i])[ρσ_bound_index(keys[(typeof j === "number" && j < 0) ? keys.length + j : j], ρσ_expr_temp)];
            }
        }
        return ans;
    };
}();
function ρσ_interpolate_kwargs(f, supplied_args) {
    var has_prop, kwobj, args, prop;
    if (!f.__argnames__) {
        return f.apply(this, supplied_args);
    }
    has_prop = Object.prototype.hasOwnProperty;
    kwobj = supplied_args.pop();
    if (f.__handles_kwarg_interpolation__) {
        args = new Array(Math.max(supplied_args.length, f.__argnames__.length) + 1);
        args[args.length-1] = kwobj;
        for (var i = 0; i < args.length - 1; i++) {
            if (i < f.__argnames__.length) {
                prop = (ρσ_expr_temp = f.__argnames__)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i];
                if (has_prop.call(kwobj, prop)) {
                    args[(typeof i === "number" && i < 0) ? args.length + i : i] = kwobj[(typeof prop === "number" && prop < 0) ? kwobj.length + prop : prop];
                    delete kwobj[prop];
                } else if (i < supplied_args.length) {
                    args[(typeof i === "number" && i < 0) ? args.length + i : i] = supplied_args[(typeof i === "number" && i < 0) ? supplied_args.length + i : i];
                }
            } else {
                args[(typeof i === "number" && i < 0) ? args.length + i : i] = supplied_args[(typeof i === "number" && i < 0) ? supplied_args.length + i : i];
            }
        }
        return f.apply(this, args);
    }
    for (var i = 0; i < f.__argnames__.length; i++) {
        prop = (ρσ_expr_temp = f.__argnames__)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i];
        if (has_prop.call(kwobj, prop)) {
            supplied_args[(typeof i === "number" && i < 0) ? supplied_args.length + i : i] = kwobj[(typeof prop === "number" && prop < 0) ? kwobj.length + prop : prop];
        }
    }
    return f.apply(this, supplied_args);
};
Object.defineProperties(ρσ_interpolate_kwargs, {
    __argnames__ : {value: ["f", "supplied_args"]}
});

function ρσ_interpolate_kwargs_constructor(apply, f, supplied_args) {
    if (apply) {
        f.apply(this, supplied_args);
    } else {
        ρσ_interpolate_kwargs.call(this, f, supplied_args);
    }
    return this;
};
Object.defineProperties(ρσ_interpolate_kwargs_constructor, {
    __argnames__ : {value: ["apply", "f", "supplied_args"]}
});

function ρσ_getitem(obj, key) {
    if (obj.__getitem__) {
        return obj.__getitem__(key);
    }
    if (typeof key === "number" && key < 0) {
        key += obj.length;
    }
    return obj[(typeof key === "number" && key < 0) ? obj.length + key : key];
};
Object.defineProperties(ρσ_getitem, {
    __argnames__ : {value: ["obj", "key"]}
});

function ρσ_setitem(obj, key, val) {
    if (obj.__setitem__) {
        obj.__setitem__(key, val);
    } else {
        if (typeof key === "number" && key < 0) {
            key += obj.length;
        }
        obj[(typeof key === "number" && key < 0) ? obj.length + key : key] = val;
    }
};
Object.defineProperties(ρσ_setitem, {
    __argnames__ : {value: ["obj", "key", "val"]}
});

function ρσ_delitem(obj, key) {
    if (obj.__delitem__) {
        obj.__delitem__(key);
    } else if (typeof obj.splice === "function") {
        obj.splice(key, 1);
    } else {
        if (typeof key === "number" && key < 0) {
            key += obj.length;
        }
        delete obj[key];
    }
};
Object.defineProperties(ρσ_delitem, {
    __argnames__ : {value: ["obj", "key"]}
});

function ρσ_bound_index(idx, arr) {
    if (typeof idx === "number" && idx < 0) {
        idx += arr.length;
    }
    return idx;
};
Object.defineProperties(ρσ_bound_index, {
    __argnames__ : {value: ["idx", "arr"]}
});

ρσ_exists = (function(){
    var ρσ_d = {};
    ρσ_d["n"] = (function() {
        var ρσ_anonfunc = function (expr) {
            return expr !== undefined && expr !== null;
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["expr"]}
        });
        return ρσ_anonfunc;
    })();
    ρσ_d["d"] = (function() {
        var ρσ_anonfunc = function (expr) {
            if (expr === undefined || expr === null) {
                return Object.create(null);
            }
            return expr;
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["expr"]}
        });
        return ρσ_anonfunc;
    })();
    ρσ_d["c"] = (function() {
        var ρσ_anonfunc = function (expr) {
            if (typeof expr === "function") {
                return expr;
            }
            return function () {
                return undefined;
            };
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["expr"]}
        });
        return ρσ_anonfunc;
    })();
    ρσ_d["g"] = (function() {
        var ρσ_anonfunc = function (expr) {
            if (expr === undefined || expr === null || typeof expr.__getitem__ !== "function") {
                return (function(){
                    var ρσ_d = {};
                    ρσ_d["__getitem__"] = function () {
                        return undefined;
                    };
                    return ρσ_d;
                }).call(this);
            }
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["expr"]}
        });
        return ρσ_anonfunc;
    })();
    ρσ_d["e"] = (function() {
        var ρσ_anonfunc = function (expr, alt) {
            return (expr === undefined || expr === null) ? alt : expr;
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["expr", "alt"]}
        });
        return ρσ_anonfunc;
    })();
    return ρσ_d;
}).call(this);
function ρσ_mixin() {
    var seen, ρσ_chain_assign_temp, resolved_props, p, target, props, name;
    seen = Object.create(null);
    ρσ_chain_assign_temp = true;
    seen.__argnames__ = ρσ_chain_assign_temp;
    seen.__handles_kwarg_interpolation__ = ρσ_chain_assign_temp;
    seen.__init__ = ρσ_chain_assign_temp;
    seen.__annotations__ = ρσ_chain_assign_temp;
    seen.__doc__ = ρσ_chain_assign_temp;
    seen.__bind_methods__ = ρσ_chain_assign_temp;
    seen.__bases__ = ρσ_chain_assign_temp;
    seen.constructor = ρσ_chain_assign_temp;
    seen.__class__ = ρσ_chain_assign_temp;
;
    resolved_props = {};
    ρσ_chain_assign_temp = arguments[0].prototype;
    p = ρσ_chain_assign_temp;
    target = ρσ_chain_assign_temp;
;
    while (p && p !== Object.prototype) {
        props = Object.getOwnPropertyNames(p);
        for (var i = 0; i < props.length; i++) {
            seen[ρσ_bound_index(props[(typeof i === "number" && i < 0) ? props.length + i : i], seen)] = true;
        }
        p = Object.getPrototypeOf(p);
    }
    for (var c = 1; c < arguments.length; c++) {
        p = arguments[(typeof c === "number" && c < 0) ? arguments.length + c : c].prototype;
        while (p && p !== Object.prototype) {
            props = Object.getOwnPropertyNames(p);
            for (var i = 0; i < props.length; i++) {
                name = props[(typeof i === "number" && i < 0) ? props.length + i : i];
                if (seen[(typeof name === "number" && name < 0) ? seen.length + name : name]) {
                    continue;
                }
                seen[(typeof name === "number" && name < 0) ? seen.length + name : name] = true;
                resolved_props[(typeof name === "number" && name < 0) ? resolved_props.length + name : name] = Object.getOwnPropertyDescriptor(p, name);
            }
            p = Object.getPrototypeOf(p);
        }
    }
    Object.defineProperties(target, resolved_props);
};

function ρσ_instanceof() {
    var obj, bases, q, cls, p;
    obj = arguments[0];
    bases = "";
    if (obj && obj.constructor && obj.constructor.prototype) {
        bases = obj.constructor.prototype.__bases__ || "";
    }
    for (var i = 1; i < arguments.length; i++) {
        q = arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i];
        if (obj instanceof q) {
            return true;
        }
        if ((q === Array || q === ρσ_list_constructor) && Array.isArray(obj)) {
            return true;
        }
        if (q === ρσ_str && (typeof obj === "string" || obj instanceof String)) {
            return true;
        }
        if (bases.length > 1) {
            for (var c = 1; c < bases.length; c++) {
                cls = bases[(typeof c === "number" && c < 0) ? bases.length + c : c];
                while (cls) {
                    if (q === cls) {
                        return true;
                    }
                    p = Object.getPrototypeOf(cls.prototype);
                    if (!p) {
                        break;
                    }
                    cls = p.constructor;
                }
            }
        }
    }
    return false;
};
function sum(iterable, start) {
    var ans, iterator, r;
    if (Array.isArray(iterable)) {
        return iterable.reduce((function() {
            var ρσ_anonfunc = function (prev, cur) {
                return prev + cur;
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["prev", "cur"]}
            });
            return ρσ_anonfunc;
        })(), start || 0);
    }
    ans = start || 0;
    iterator = iter(iterable);
    r = iterator.next();
    while (!r.done) {
        ans += r.value;
        r = iterator.next();
    }
    return ans;
};
Object.defineProperties(sum, {
    __argnames__ : {value: ["iterable", "start"]}
});

function map() {
    var iterators, func, args, ans;
    iterators = new Array(arguments.length - 1);
    func = arguments[0];
    args = new Array(arguments.length - 1);
    for (var i = 1; i < arguments.length; i++) {
        iterators[ρσ_bound_index(i - 1, iterators)] = iter(arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i]);
    }
    ans = {'_func':func, '_iterators':iterators, '_args':args};
    ans[ρσ_iterator_symbol] = function () {
        return this;
    };
    ans["next"] = function () {
        var r;
        for (var i = 0; i < this._iterators.length; i++) {
            r = (ρσ_expr_temp = this._iterators)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i].next();
            if (r.done) {
                return {'done':true};
            }
            (ρσ_expr_temp = this._args)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i] = r.value;
        }
        return {'done':false, 'value':this._func.apply(undefined, this._args)};
    };
    return ans;
};

function filter(func_or_none, iterable) {
    var func, ans;
    func = (func_or_none === null) ? ρσ_bool : func_or_none;
    ans = {'_func':func, '_iterator':ρσ_iter(iterable)};
    ans[ρσ_iterator_symbol] = function () {
        return this;
    };
    ans["next"] = function () {
        var r;
        r = this._iterator.next();
        while (!r.done) {
            if (this._func(r.value)) {
                return r;
            }
            r = this._iterator.next();
        }
        return {'done':true};
    };
    return ans;
};
Object.defineProperties(filter, {
    __argnames__ : {value: ["func_or_none", "iterable"]}
});

function zip() {
    var iterators, ans;
    iterators = new Array(arguments.length);
    for (var i = 0; i < arguments.length; i++) {
        iterators[(typeof i === "number" && i < 0) ? iterators.length + i : i] = iter(arguments[(typeof i === "number" && i < 0) ? arguments.length + i : i]);
    }
    ans = {'_iterators':iterators};
    ans[ρσ_iterator_symbol] = function () {
        return this;
    };
    ans["next"] = function () {
        var args, r;
        args = new Array(this._iterators.length);
        for (var i = 0; i < this._iterators.length; i++) {
            r = (ρσ_expr_temp = this._iterators)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i].next();
            if (r.done) {
                return {'done':true};
            }
            args[(typeof i === "number" && i < 0) ? args.length + i : i] = r.value;
        }
        return {'done':false, 'value':args};
    };
    return ans;
};

function any(iterable) {
    var i;
    var ρσ_Iter0 = ρσ_Iterable(iterable);
    for (var ρσ_Index0 = 0; ρσ_Index0 < ρσ_Iter0.length; ρσ_Index0++) {
        i = ρσ_Iter0[ρσ_Index0];
        if (i) {
            return true;
        }
    }
    return false;
};
Object.defineProperties(any, {
    __argnames__ : {value: ["iterable"]}
});

function all(iterable) {
    var i;
    var ρσ_Iter1 = ρσ_Iterable(iterable);
    for (var ρσ_Index1 = 0; ρσ_Index1 < ρσ_Iter1.length; ρσ_Index1++) {
        i = ρσ_Iter1[ρσ_Index1];
        if (!i) {
            return false;
        }
    }
    return true;
};
Object.defineProperties(all, {
    __argnames__ : {value: ["iterable"]}
});
var define_str_func, ρσ_unpack, ρσ_orig_split, ρσ_orig_replace;
function ρσ_repr_js_builtin(x, as_array) {
    var ans, b, keys, key;
    ans = [];
    b = "{}";
    if (as_array) {
        b = "[]";
        for (var i = 0; i < x.length; i++) {
            ans.push(ρσ_repr(x[(typeof i === "number" && i < 0) ? x.length + i : i]));
        }
    } else {
        keys = Object.keys(x);
        for (var k = 0; k < keys.length; k++) {
            key = keys[(typeof k === "number" && k < 0) ? keys.length + k : k];
            ans.push(JSON.stringify(key) + ":" + ρσ_repr(x[(typeof key === "number" && key < 0) ? x.length + key : key]));
        }
    }
    return b[0] + ans.join(", ") + b[1];
};
Object.defineProperties(ρσ_repr_js_builtin, {
    __argnames__ : {value: ["x", "as_array"]}
});

function ρσ_repr(x) {
    var ans, name;
    if (x === null) {
        return "None";
    }
    if (x === undefined) {
        return "undefined";
    }
    ans = x;
    if (typeof x.__repr__ === "function") {
        ans = x.__repr__();
    } else if (x === true || x === false) {
        ans = (x) ? "True" : "False";
    } else if (Array.isArray(x)) {
        ans = ρσ_repr_js_builtin(x, true);
    } else if (typeof x === "function") {
        ans = x.toString();
    } else if (typeof x === "object" && !x.toString) {
        ans = ρσ_repr_js_builtin(x);
    } else {
        name = Object.prototype.toString.call(x).slice(8, -1);
        if (ρσ_not_equals("Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".indexOf(name), -1)) {
            return name + "([" + x.map((function() {
                var ρσ_anonfunc = function (i) {
                    return str.format("0x{:02x}", i);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["i"]}
                });
                return ρσ_anonfunc;
            })()).join(", ") + "])";
        }
        ans = (typeof x.toString === "function") ? x.toString() : x;
        if (ans === "[object Object]") {
            return ρσ_repr_js_builtin(x);
        }
        try {
            ans = JSON.stringify(x);
        } catch (ρσ_Exception) {
            ρσ_last_exception = ρσ_Exception;
            {
            } 
        }
    }
    return ans + "";
};
Object.defineProperties(ρσ_repr, {
    __argnames__ : {value: ["x"]}
});

function ρσ_str(x) {
    var ans, name;
    if (x === null) {
        return "None";
    }
    if (x === undefined) {
        return "undefined";
    }
    ans = x;
    if (typeof x.__str__ === "function") {
        ans = x.__str__();
    } else if (typeof x.__repr__ === "function") {
        ans = x.__repr__();
    } else if (x === true || x === false) {
        ans = (x) ? "True" : "False";
    } else if (Array.isArray(x)) {
        ans = ρσ_repr_js_builtin(x, true);
    } else if (typeof x.toString === "function") {
        name = Object.prototype.toString.call(x).slice(8, -1);
        if (ρσ_not_equals("Int8Array Uint8Array Uint8ClampedArray Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array".indexOf(name), -1)) {
            return name + "([" + x.map((function() {
                var ρσ_anonfunc = function (i) {
                    return str.format("0x{:02x}", i);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["i"]}
                });
                return ρσ_anonfunc;
            })()).join(", ") + "])";
        }
        ans = x.toString();
        if (ans === "[object Object]") {
            ans = ρσ_repr_js_builtin(x);
        }
    } else if (typeof x === "object" && !x.toString) {
        ans = ρσ_repr_js_builtin(x);
    }
    return ans + "";
};
Object.defineProperties(ρσ_str, {
    __argnames__ : {value: ["x"]}
});

define_str_func = (function() {
    var ρσ_anonfunc = function (name, func) {
        var f, ρσ_chain_assign_temp;
        (ρσ_expr_temp = ρσ_str.prototype)[(typeof name === "number" && name < 0) ? ρσ_expr_temp.length + name : name] = func;
        ρσ_chain_assign_temp = func.call.bind(func);
        ρσ_str[(typeof name === "number" && name < 0) ? ρσ_str.length + name : name] = ρσ_chain_assign_temp;
        f = ρσ_chain_assign_temp;
;
        if (func.__argnames__) {
            Object.defineProperty(f, "__argnames__", (function(){
                var ρσ_d = {};
                ρσ_d["value"] = ['string'].concat(func.__argnames__);
                return ρσ_d;
            }).call(this));
        }
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["name", "func"]}
    });
    return ρσ_anonfunc;
})();
ρσ_unpack = [String.prototype.split.call.bind(String.prototype.split), String.prototype.replace.call.bind(String.prototype.replace)];
ρσ_orig_split = ρσ_unpack[0];
ρσ_orig_replace = ρσ_unpack[1];
define_str_func("format", function () {
    var template, args, kwargs, explicit, implicit, ρσ_chain_assign_temp, idx, split, ans, pos, in_brace, markup, ch;
    template = this;
    if (template === undefined) {
        throw new TypeError("Template is required");
    }
    args = Array.prototype.slice.call(arguments);
    kwargs = {};
    if (args[args.length-1] && args[args.length-1][ρσ_kwargs_symbol] !== undefined) {
        kwargs = args[args.length-1];
        args = args.slice(0, -1);
    }
    ρσ_chain_assign_temp = false;
    explicit = ρσ_chain_assign_temp;
    implicit = ρσ_chain_assign_temp;
;
    idx = 0;
    split = ρσ_orig_split;
    if (ρσ_str.format._template_resolve_pat === undefined) {
        ρσ_str.format._template_resolve_pat = /[.\[]/;
    }
    function resolve(arg, object) {
        var ρσ_unpack, first, key, rest, ans;
        if (!arg) {
            return object;
        }
        ρσ_unpack = [arg[0], arg.slice(1)];
        first = ρσ_unpack[0];
        arg = ρσ_unpack[1];
        key = split(arg, ρσ_str.format._template_resolve_pat, 1)[0];
        rest = arg.slice(key.length);
        ans = (first === "[") ? object[ρσ_bound_index(key.slice(0, -1), object)] : getattr(object, key);
        if (ans === undefined) {
            throw new KeyError((first === "[") ? key.slice(0, -1) : key);
        }
        return resolve(rest, ans);
    };
    Object.defineProperties(resolve, {
        __argnames__ : {value: ["arg", "object"]}
    });

    function resolve_format_spec(format_spec) {
        if (ρσ_str.format._template_resolve_fs_pat === undefined) {
            ρσ_str.format._template_resolve_fs_pat = /[{]([a-zA-Z0-9_]+)[}]/g;
        }
        return format_spec.replace(ρσ_str.format._template_resolve_fs_pat, (function() {
            var ρσ_anonfunc = function (match, key) {
                if (!Object.prototype.hasOwnProperty.call(kwargs, key)) {
                    return "";
                }
                return "" + kwargs[(typeof key === "number" && key < 0) ? kwargs.length + key : key];
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["match", "key"]}
            });
            return ρσ_anonfunc;
        })());
    };
    Object.defineProperties(resolve_format_spec, {
        __argnames__ : {value: ["format_spec"]}
    });

    function apply_formatting(value, format_spec) {
        var ρσ_unpack, fill, align, sign, fhash, zeropad, width, comma, precision, ftype, is_numeric, is_int, lftype, code, exp, nval, is_positive, left, right;
        if (format_spec.indexOf("{") !== -1) {
            format_spec = resolve_format_spec(format_spec);
        }
        if (ρσ_str.format._template_format_pat === undefined) {
            ρσ_str.format._template_format_pat = /([^{}](?=[<>=^]))?([<>=^])?([-+\x20])?(\#)?(0)?(\d+)?(,)?(?:\.(\d+))?([bcdeEfFgGnosxX%])?/;
        }
        try {
            ρσ_unpack = format_spec.match(ρσ_str.format._template_format_pat).slice(1);
            fill = ρσ_unpack[0];
            align = ρσ_unpack[1];
            sign = ρσ_unpack[2];
            fhash = ρσ_unpack[3];
            zeropad = ρσ_unpack[4];
            width = ρσ_unpack[5];
            comma = ρσ_unpack[6];
            precision = ρσ_unpack[7];
            ftype = ρσ_unpack[8];
        } catch (ρσ_Exception) {
            ρσ_last_exception = ρσ_Exception;
            if (ρσ_Exception instanceof TypeError) {
                return value;
            } else {
                throw ρσ_Exception;
            }
        }
        if (zeropad) {
            fill = fill || "0";
            align = align || "=";
        } else {
            fill = fill || " ";
            align = align || ">";
        }
        is_numeric = Number(value) === value;
        is_int = is_numeric && value % 1 === 0;
        precision = parseInt(precision, 10);
        lftype = (ftype || "").toLowerCase();
        if (ftype === "n") {
            is_numeric = true;
            if (is_int) {
                if (comma) {
                    throw new ValueError("Cannot specify ',' with 'n'");
                }
                value = parseInt(value, 10).toLocaleString();
            } else {
                value = parseFloat(value).toLocaleString();
            }
        } else if (['b', 'c', 'd', 'o', 'x'].indexOf(lftype) !== -1) {
            value = parseInt(value, 10);
            is_numeric = true;
            if (!isNaN(value)) {
                if (ftype === "b") {
                    value = (value >>> 0).toString(2);
                    if (fhash) {
                        value = "0b" + value;
                    }
                } else if (ftype === "c") {
                    if (value > 65535) {
                        code = value - 65536;
                        value = String.fromCharCode(55296 + (code >> 10), 56320 + (code & 1023));
                    } else {
                        value = String.fromCharCode(value);
                    }
                } else if (ftype === "d") {
                    if (comma) {
                        value = value.toLocaleString("en-US");
                    } else {
                        value = value.toString(10);
                    }
                } else if (ftype === "o") {
                    value = value.toString(8);
                    if (fhash) {
                        value = "0o" + value;
                    }
                } else if (lftype === "x") {
                    value = value.toString(16);
                    value = (ftype === "x") ? value.toLowerCase() : value.toUpperCase();
                    if (fhash) {
                        value = "0x" + value;
                    }
                }
            }
        } else if (['e','f','g','%'].indexOf(lftype) !== -1) {
            is_numeric = true;
            value = parseFloat(value);
            if (lftype === "e") {
                value = value.toExponential((isNaN(precision)) ? 6 : precision);
                value = (ftype === "E") ? value.toUpperCase() : value.toLowerCase();
            } else if (lftype === "f") {
                value = value.toFixed((isNaN(precision)) ? 6 : precision);
                value = (ftype === "F") ? value.toUpperCase() : value.toLowerCase();
            } else if (ftype === "%") {
                value *= 100;
                value = value.toFixed((isNaN(precision)) ? 6 : precision) + "%";
            } else if (lftype === "g") {
                if (isNaN(precision)) {
                    precision = 6;
                }
                precision = max(1, precision);
                exp = parseInt(split(value.toExponential(precision - 1).toLowerCase(), "e")[1], 10);
                if (-4 <= exp && exp < precision) {
                    value = value.toFixed(precision - 1 - exp);
                } else {
                    value = value.toExponential(precision - 1);
                }
                value = value.replace(/0+$/g, "");
                if (value[value.length-1] === ".") {
                    value = value.slice(0, -1);
                }
                if (ftype === "G") {
                    value = value.toUpperCase();
                }
            }
        } else {
            value += "";
            if (!isNaN(precision)) {
                value = value.slice(0, precision);
            }
        }
        value += "";
        if (is_numeric && sign) {
            nval = Number(value);
            is_positive = !isNaN(nval) && nval >= 0;
            if (is_positive && (sign === " " || sign === "+")) {
                value = sign + value;
            }
        }
        function repeat(char, num) {
            return (new Array(num+1)).join(char);
        };
        Object.defineProperties(repeat, {
            __argnames__ : {value: ["char", "num"]}
        });

        if (is_numeric && width && width[0] === "0") {
            width = width.slice(1);
            ρσ_unpack = ["0", "="];
            fill = ρσ_unpack[0];
            align = ρσ_unpack[1];
        }
        width = parseInt(width || "-1", 10);
        if (isNaN(width)) {
            throw new ValueError("Invalid width specification: " + width);
        }
        if (fill && value.length < width) {
            if (align === "<") {
                value = value + repeat(fill, width - value.length);
            } else if (align === ">") {
                value = repeat(fill, width - value.length) + value;
            } else if (align === "^") {
                left = Math.floor((width - value.length) / 2);
                right = width - left - value.length;
                value = repeat(fill, left) + value + repeat(fill, right);
            } else if (align === "=") {
                if (ρσ_in(value[0], "+- ")) {
                    value = value[0] + repeat(fill, width - value.length) + value.slice(1);
                } else {
                    value = repeat(fill, width - value.length) + value;
                }
            } else {
                throw new ValueError("Unrecognized alignment: " + align);
            }
        }
        return value;
    };
    Object.defineProperties(apply_formatting, {
        __argnames__ : {value: ["value", "format_spec"]}
    });

    function parse_markup(markup) {
        var key, transformer, format_spec, ρσ_chain_assign_temp, pos, state, ch;
        ρσ_chain_assign_temp = "";
        key = ρσ_chain_assign_temp;
        transformer = ρσ_chain_assign_temp;
        format_spec = ρσ_chain_assign_temp;
;
        pos = 0;
        state = 0;
        while (pos < markup.length) {
            ch = markup[(typeof pos === "number" && pos < 0) ? markup.length + pos : pos];
            if (state === 0) {
                if (ch === "!") {
                    state = 1;
                } else if (ch === ":") {
                    state = 2;
                } else {
                    key += ch;
                }
            } else if (state === 1) {
                if (ch === ":") {
                    state = 2;
                } else {
                    transformer += ch;
                }
            } else {
                format_spec += ch;
            }
            pos += 1;
        }
        return [key, transformer, format_spec];
    };
    Object.defineProperties(parse_markup, {
        __argnames__ : {value: ["markup"]}
    });

    function render_markup(markup) {
        var ρσ_unpack, key, transformer, format_spec, lkey, nvalue, object, ans;
        ρσ_unpack = parse_markup(markup);
        key = ρσ_unpack[0];
        transformer = ρσ_unpack[1];
        format_spec = ρσ_unpack[2];
        if (transformer && ['a', 'r', 's'].indexOf(transformer) === -1) {
            throw new ValueError("Unknown conversion specifier: " + transformer);
        }
        lkey = key.length && split(key, /[.\[]/, 1)[0];
        if (lkey) {
            explicit = true;
            if (implicit) {
                throw new ValueError("cannot switch from automatic field numbering to manual field specification");
            }
            nvalue = parseInt(lkey);
            object = (isNaN(nvalue)) ? kwargs[(typeof lkey === "number" && lkey < 0) ? kwargs.length + lkey : lkey] : args[(typeof nvalue === "number" && nvalue < 0) ? args.length + nvalue : nvalue];
            if (object === undefined) {
                if (isNaN(nvalue)) {
                    throw new KeyError(lkey);
                }
                throw new IndexError(lkey);
            }
            object = resolve(key.slice(lkey.length), object);
        } else {
            implicit = true;
            if (explicit) {
                throw new ValueError("cannot switch from manual field specification to automatic field numbering");
            }
            if (idx >= args.length) {
                throw new IndexError("Not enough arguments to match template: " + template);
            }
            object = args[(typeof idx === "number" && idx < 0) ? args.length + idx : idx];
            idx += 1;
        }
        if (typeof object === "function") {
            object = object();
        }
        ans = "" + object;
        if (format_spec) {
            ans = apply_formatting(ans, format_spec);
        }
        return ans;
    };
    Object.defineProperties(render_markup, {
        __argnames__ : {value: ["markup"]}
    });

    ans = "";
    pos = 0;
    in_brace = 0;
    markup = "";
    while (pos < template.length) {
        ch = template[(typeof pos === "number" && pos < 0) ? template.length + pos : pos];
        if (in_brace) {
            if (ch === "{") {
                in_brace += 1;
                markup += "{";
            } else if (ch === "}") {
                in_brace -= 1;
                if (in_brace > 0) {
                    markup += "}";
                } else {
                    ans += render_markup(markup);
                }
            } else {
                markup += ch;
            }
        } else {
            if (ch === "{") {
                if (template[ρσ_bound_index(pos + 1, template)] === "{") {
                    pos += 1;
                    ans += "{";
                } else {
                    in_brace = 1;
                    markup = "";
                }
            } else {
                ans += ch;
            }
        }
        pos += 1;
    }
    if (in_brace) {
        throw new ValueError("expected '}' before end of string");
    }
    return ans;
});
define_str_func("capitalize", function () {
    var string;
    string = this;
    if (string) {
        string = string[0].toUpperCase() + string.slice(1).toLowerCase();
    }
    return string;
});
define_str_func("center", (function() {
    var ρσ_anonfunc = function (width, fill) {
        var left, right;
        left = Math.floor((width - this.length) / 2);
        right = width - left - this.length;
        fill = fill || " ";
        return new Array(left+1).join(fill) + this + new Array(right+1).join(fill);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["width", "fill"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("count", (function() {
    var ρσ_anonfunc = function (needle, start, end) {
        var string, ρσ_unpack, pos, step, ans;
        string = this;
        start = start || 0;
        end = end || string.length;
        if (start < 0 || end < 0) {
            string = string.slice(start, end);
            ρσ_unpack = [0, string.length];
            start = ρσ_unpack[0];
            end = ρσ_unpack[1];
        }
        pos = start;
        step = needle.length;
        if (!step) {
            return 0;
        }
        ans = 0;
        while (pos !== -1) {
            pos = string.indexOf(needle, pos);
            if (pos !== -1) {
                ans += 1;
                pos += step;
            }
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["needle", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("endswith", (function() {
    var ρσ_anonfunc = function (suffixes, start, end) {
        var string, q;
        string = this;
        start = start || 0;
        if (typeof suffixes === "string") {
            suffixes = [suffixes];
        }
        if (end !== undefined) {
            string = string.slice(0, end);
        }
        for (var i = 0; i < suffixes.length; i++) {
            q = suffixes[(typeof i === "number" && i < 0) ? suffixes.length + i : i];
            if (string.indexOf(q, Math.max(start, string.length - q.length)) !== -1) {
                return true;
            }
        }
        return false;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["suffixes", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("startswith", (function() {
    var ρσ_anonfunc = function (prefixes, start, end) {
        var prefix;
        start = start || 0;
        if (typeof prefixes === "string") {
            prefixes = [prefixes];
        }
        for (var i = 0; i < prefixes.length; i++) {
            prefix = prefixes[(typeof i === "number" && i < 0) ? prefixes.length + i : i];
            end = (end === undefined) ? this.length : end;
            if (end - start >= prefix.length && prefix === this.slice(start, start + prefix.length)) {
                return true;
            }
        }
        return false;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["prefixes", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("find", (function() {
    var ρσ_anonfunc = function (needle, start, end) {
        var ans;
        while (start < 0) {
            start += this.length;
        }
        ans = this.indexOf(needle, start);
        if (end !== undefined && ans !== -1) {
            while (end < 0) {
                end += this.length;
            }
            if (ans >= end - needle.length) {
                return -1;
            }
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["needle", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rfind", (function() {
    var ρσ_anonfunc = function (needle, start, end) {
        var ans;
        while (end < 0) {
            end += this.length;
        }
        ans = this.lastIndexOf(needle, end - 1);
        if (start !== undefined && ans !== -1) {
            while (start < 0) {
                start += this.length;
            }
            if (ans < start) {
                return -1;
            }
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["needle", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("index", (function() {
    var ρσ_anonfunc = function (needle, start, end) {
        var ans;
        ans = ρσ_str.prototype.find.apply(this, arguments);
        if (ans === -1) {
            throw new ValueError("substring not found");
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["needle", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rindex", (function() {
    var ρσ_anonfunc = function (needle, start, end) {
        var ans;
        ans = ρσ_str.prototype.rfind.apply(this, arguments);
        if (ans === -1) {
            throw new ValueError("substring not found");
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["needle", "start", "end"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("islower", function () {
    return this.length > 0 && this.toUpperCase() !== this;
});
define_str_func("isupper", function () {
    return this.length > 0 && this.toLowerCase() !== this;
});
define_str_func("isspace", function () {
    return this.length > 0 && /^\s+$/.test(this);
});
define_str_func("join", (function() {
    var ρσ_anonfunc = function (iterable) {
        var ans, r;
        if (Array.isArray(iterable)) {
            return iterable.join(this);
        }
        ans = "";
        r = iterable.next();
        while (!r.done) {
            if (ans) {
                ans += this;
            }
            ans += r.value;
            r = iterable.next();
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["iterable"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("ljust", (function() {
    var ρσ_anonfunc = function (width, fill) {
        var string;
        string = this;
        if (width > string.length) {
            fill = fill || " ";
            string += new Array(width - string.length + 1).join(fill);
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["width", "fill"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rjust", (function() {
    var ρσ_anonfunc = function (width, fill) {
        var string;
        string = this;
        if (width > string.length) {
            fill = fill || " ";
            string = new Array(width - string.length + 1).join(fill) + string;
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["width", "fill"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("lower", function () {
    return this.toLowerCase();
});
define_str_func("upper", function () {
    return this.toUpperCase();
});
define_str_func("lstrip", (function() {
    var ρσ_anonfunc = function (chars) {
        var string, pos;
        string = this;
        pos = 0;
        chars = chars || ρσ_str.whitespace;
        while (chars.indexOf(string[(typeof pos === "number" && pos < 0) ? string.length + pos : pos]) !== -1) {
            pos += 1;
        }
        if (pos) {
            string = string.slice(pos);
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["chars"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rstrip", (function() {
    var ρσ_anonfunc = function (chars) {
        var string, pos;
        string = this;
        pos = string.length - 1;
        chars = chars || ρσ_str.whitespace;
        while (chars.indexOf(string[(typeof pos === "number" && pos < 0) ? string.length + pos : pos]) !== -1) {
            pos -= 1;
        }
        if (pos < string.length - 1) {
            string = string.slice(0, pos + 1);
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["chars"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("strip", (function() {
    var ρσ_anonfunc = function (chars) {
        return ρσ_str.prototype.lstrip.call(ρσ_str.prototype.rstrip.call(this, chars), chars);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["chars"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("partition", (function() {
    var ρσ_anonfunc = function (sep) {
        var idx;
        idx = this.indexOf(sep);
        if (idx === -1) {
            return [this, "", ""];
        }
        return [this.slice(0, idx), sep, this.slice(idx + sep.length)];
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["sep"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rpartition", (function() {
    var ρσ_anonfunc = function (sep) {
        var idx;
        idx = this.lastIndexOf(sep);
        if (idx === -1) {
            return ["", "", this];
        }
        return [this.slice(0, idx), sep, this.slice(idx + sep.length)];
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["sep"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("replace", (function() {
    var ρσ_anonfunc = function (old, repl, count) {
        var string, pos, idx;
        string = this;
        if (count === 1) {
            return ρσ_orig_replace(string, old, repl);
        }
        if (count < 1) {
            return string;
        }
        count = count || Number.MAX_VALUE;
        pos = 0;
        while (count > 0) {
            count -= 1;
            idx = string.indexOf(old, pos);
            if (idx === -1) {
                break;
            }
            pos = idx + repl.length;
            string = string.slice(0, idx) + repl + string.slice(idx + old.length);
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["old", "repl", "count"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("split", (function() {
    var ρσ_anonfunc = function (sep, maxsplit) {
        var split, ans, extra, parts;
        if (maxsplit === 0) {
            return ρσ_list_decorate([ this ]);
        }
        split = ρσ_orig_split;
        if (sep === undefined || sep === null) {
            if (maxsplit > 0) {
                ans = split(this, /(\s+)/);
                extra = "";
                parts = [];
                for (var i = 0; i < ans.length; i++) {
                    if (parts.length >= maxsplit + 1) {
                        extra += ans[(typeof i === "number" && i < 0) ? ans.length + i : i];
                    } else if (i % 2 === 0) {
                        parts.push(ans[(typeof i === "number" && i < 0) ? ans.length + i : i]);
                    }
                }
                parts[parts.length-1] += extra;
                ans = parts;
            } else {
                ans = split(this, /\s+/);
            }
        } else {
            if (sep === "") {
                throw new ValueError("empty separator");
            }
            ans = split(this, sep);
            if (maxsplit > 0 && ans.length > maxsplit) {
                extra = ans.slice(maxsplit).join(sep);
                ans = ans.slice(0, maxsplit);
                ans.push(extra);
            }
        }
        return ρσ_list_decorate(ans);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["sep", "maxsplit"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("rsplit", (function() {
    var ρσ_anonfunc = function (sep, maxsplit) {
        var split, ans, is_space, pos, current, spc, ch, end, ρσ_chain_assign_temp, idx;
        if (!maxsplit) {
            return ρσ_str.prototype.split.call(this, sep);
        }
        split = ρσ_orig_split;
        if (sep === undefined || sep === null) {
            if (maxsplit > 0) {
                ans = [];
                is_space = /\s/;
                pos = this.length - 1;
                current = "";
                while (pos > -1 && maxsplit > 0) {
                    spc = false;
                    ch = (ρσ_expr_temp = this)[(typeof pos === "number" && pos < 0) ? ρσ_expr_temp.length + pos : pos];
                    while (pos > -1 && is_space.test(ch)) {
                        spc = true;
                        ch = this[--pos];
                    }
                    if (spc) {
                        if (current) {
                            ans.push(current);
                            maxsplit -= 1;
                        }
                        current = ch;
                    } else {
                        current += ch;
                    }
                    pos -= 1;
                }
                ans.push(this.slice(0, pos + 1) + current);
                ans.reverse();
            } else {
                ans = split(this, /\s+/);
            }
        } else {
            if (sep === "") {
                throw new ValueError("empty separator");
            }
            ans = [];
            ρσ_chain_assign_temp = this.length;
            pos = ρσ_chain_assign_temp;
            end = ρσ_chain_assign_temp;
;
            while (pos > -1 && maxsplit > 0) {
                maxsplit -= 1;
                idx = this.lastIndexOf(sep, pos);
                if (idx === -1) {
                    break;
                }
                ans.push(this.slice(idx + sep.length, end));
                pos = idx - 1;
                end = idx;
            }
            ans.push(this.slice(0, end));
            ans.reverse();
        }
        return ρσ_list_decorate(ans);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["sep", "maxsplit"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("splitlines", (function() {
    var ρσ_anonfunc = function (keepends) {
        var split, parts, ans;
        split = ρσ_orig_split;
        if (keepends) {
            parts = split(this, /((?:\r?\n)|\r)/);
            ans = [];
            for (var i = 0; i < parts.length; i++) {
                if (i % 2 === 0) {
                    ans.push(parts[(typeof i === "number" && i < 0) ? parts.length + i : i]);
                } else {
                    ans[ans.length-1] += parts[(typeof i === "number" && i < 0) ? parts.length + i : i];
                }
            }
        } else {
            ans = split(this, /(?:\r?\n)|\r/);
        }
        return ρσ_list_decorate(ans);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["keepends"]}
    });
    return ρσ_anonfunc;
})());
define_str_func("swapcase", function () {
    var ans, a, b;
    ans = new Array(this.length);
    for (var i = 0; i < ans.length; i++) {
        a = (ρσ_expr_temp = this)[(typeof i === "number" && i < 0) ? ρσ_expr_temp.length + i : i];
        b = a.toLowerCase();
        if (a === b) {
            b = a.toUpperCase();
        }
        ans[(typeof i === "number" && i < 0) ? ans.length + i : i] = b;
    }
    return ans.join("");
});
define_str_func("zfill", (function() {
    var ρσ_anonfunc = function (width) {
        var string;
        string = this;
        if (width > string.length) {
            string = new Array(width - string.length + 1).join("0") + string;
        }
        return string;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["width"]}
    });
    return ρσ_anonfunc;
})());
ρσ_str.uchrs = (function() {
    var ρσ_anonfunc = function (string, with_positions) {
        return (function(){
            var ρσ_d = {};
            ρσ_d["_string"] = string;
            ρσ_d["_pos"] = 0;
            ρσ_d[ρσ_iterator_symbol] = function () {
                return this;
            };
            ρσ_d["next"] = function () {
                var length, pos, value, ans, extra;
                length = this._string.length;
                if (this._pos >= length) {
                    return (function(){
                        var ρσ_d = {};
                        ρσ_d["done"] = true;
                        return ρσ_d;
                    }).call(this);
                }
                pos = this._pos;
                value = this._string.charCodeAt(this._pos++);
                ans = "\ufffd";
                if (55296 <= value && value <= 56319) {
                    if (this._pos < length) {
                        extra = this._string.charCodeAt(this._pos++);
                        if ((extra & 56320) === 56320) {
                            ans = String.fromCharCode(value, extra);
                        }
                    }
                } else if ((value & 56320) !== 56320) {
                    ans = String.fromCharCode(value);
                }
                if (with_positions) {
                    return (function(){
                        var ρσ_d = {};
                        ρσ_d["done"] = false;
                        ρσ_d["value"] = ρσ_list_decorate([ pos, ans ]);
                        return ρσ_d;
                    }).call(this);
                } else {
                    return (function(){
                        var ρσ_d = {};
                        ρσ_d["done"] = false;
                        ρσ_d["value"] = ans;
                        return ρσ_d;
                    }).call(this);
                }
            };
            return ρσ_d;
        }).call(this);
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["string", "with_positions"]}
    });
    return ρσ_anonfunc;
})();
ρσ_str.uslice = (function() {
    var ρσ_anonfunc = function (string, start, end) {
        var items, iterator, r;
        items = [];
        iterator = ρσ_str.uchrs(string);
        r = iterator.next();
        while (!r.done) {
            items.push(r.value);
            r = iterator.next();
        }
        return items.slice(start || 0, (end === undefined) ? items.length : end).join("");
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["string", "start", "end"]}
    });
    return ρσ_anonfunc;
})();
ρσ_str.ulen = (function() {
    var ρσ_anonfunc = function (string) {
        var iterator, r, ans;
        iterator = ρσ_str.uchrs(string);
        r = iterator.next();
        ans = 0;
        while (!r.done) {
            r = iterator.next();
            ans += 1;
        }
        return ans;
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["string"]}
    });
    return ρσ_anonfunc;
})();
ρσ_str.ascii_lowercase = "abcdefghijklmnopqrstuvwxyz";
ρσ_str.ascii_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
ρσ_str.ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
ρσ_str.digits = "0123456789";
ρσ_str.punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
ρσ_str.printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\u000b\f";
ρσ_str.whitespace = " \t\n\r\u000b\f";
define_str_func = undefined;
var str = ρσ_str, repr = ρσ_repr;;
var ρσ_modules = {};
ρσ_modules.glob = {};
ρσ_modules.page = {};
ρσ_modules.tabmenuitem = {};
ρσ_modules.scrolltbl = {};
ρσ_modules.tools = {};
ρσ_modules.tbl = {};
ρσ_modules.tabmenu = {};
ρσ_modules.popup = {};

(function(){
    var __name__ = "glob";
    var ACTIVE_PAGE;
    ACTIVE_PAGE = null;
    ρσ_modules.glob.ACTIVE_PAGE = ACTIVE_PAGE;
})();

(function(){
    var __name__ = "page";
    function Page() {
        if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
        Page.prototype.__init__.apply(this, arguments);
    }
    Page.prototype.__init__ = function __init__(id, page) {
        var self = this;
        self.id = id;
        self.page = page;
    };
    Object.defineProperties(Page.prototype.__init__, {
        __argnames__ : {value: ["id", "page"]}
    });
    Page.__argnames__ = Page.prototype.__init__.__argnames__;
    Page.__handles_kwarg_interpolation__ = Page.prototype.__init__.__handles_kwarg_interpolation__;
    Page.prototype.set_href = function set_href(href) {
        var self = this;
        self.page.attr("_href", href);
    };
    Object.defineProperties(Page.prototype.set_href, {
        __argnames__ : {value: ["href"]}
    });
    Page.prototype.get_href = function get_href() {
        var self = this;
        return self.page.attr("_href");
    };
    Object.defineProperties(Page.prototype.get_href, {
        __argnames__ : {value: []}
    });
    Page.prototype.__repr__ = function __repr__ () {
                return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
    };
    Page.prototype.__str__ = function __str__ () {
        return this.__repr__();
    };
    Object.defineProperty(Page.prototype, "__bases__", {value: []});

    ρσ_modules.page.Page = Page;
})();

(function(){
    var __name__ = "tabmenuitem";
    function TabMenuItem() {
        if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
        TabMenuItem.prototype.__init__.apply(this, arguments);
    }
    TabMenuItem.prototype.__init__ = function __init__() {
        var self = this;
        var id = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
        var title = ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[1];
        var url = ( 2 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[2];
        var data = (arguments[3] === undefined || ( 3 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? __init__.__defaults__.data : arguments[3];
        var ρσ_kwargs_obj = arguments[arguments.length-1];
        if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
        if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "data")){
            data = ρσ_kwargs_obj.data;
        }
        self.id = id;
        self.title = jQuery.trim(title);
        self.url = url;
        self.data = data;
    };
    Object.defineProperties(TabMenuItem.prototype.__init__, {
        __defaults__ : {value: {data:null}},
        __handles_kwarg_interpolation__ : {value: true},
        __argnames__ : {value: ["id", "title", "url", "data"]}
    });
    TabMenuItem.__argnames__ = TabMenuItem.prototype.__init__.__argnames__;
    TabMenuItem.__handles_kwarg_interpolation__ = TabMenuItem.prototype.__init__.__handles_kwarg_interpolation__;
    TabMenuItem.prototype.__repr__ = function __repr__ () {
                return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
    };
    TabMenuItem.prototype.__str__ = function __str__ () {
        return this.__repr__();
    };
    Object.defineProperty(TabMenuItem.prototype, "__bases__", {value: []});

    ρσ_modules.tabmenuitem.TabMenuItem = TabMenuItem;
})();

(function(){
    var __name__ = "scrolltbl";
    var glob = ρσ_modules.glob;

    function stick_resize() {
        var tbl, dy_table, dy_win, ρσ_chain_assign_temp, dy;
        tbl = glob.ACTIVE_PAGE.page.find(".tbl_scroll");
        if (tbl.length > 0) {
            dy_table = tbl.offset().top;
            ρσ_chain_assign_temp = jQuery(window).height();
            dy_win = ρσ_chain_assign_temp;
            dy_win = ρσ_chain_assign_temp;
;
            dy = dy_win - dy_table;
            if (dy < 100) dy = 100;
            tbl.height(dy - 35);
        }
    };

    function resize_win() {
        var tab2, tab_width;
        stick_resize();
        tab2 = ρσ_list_decorate([]);
        tab_width = glob.ACTIVE_PAGE.page.find("table[name='tabsort']").width();
        glob.ACTIVE_PAGE.page.find(".tbl_header").width(tab_width);
        glob.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function () {
            tab2.push(jQuery(this).width());
        });
        tab2 = tab2.reverse();
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function () {
            jQuery(this).width(tab2.pop());
        });
    };

    function stick_header() {
        var tab, tab2, table;
        tab = ρσ_list_decorate([]);
        tab2 = ρσ_list_decorate([]);
        glob.ACTIVE_PAGE.page.find("table.tabsort th").each(function () {
            tab.push(jQuery(this).width());
        });
        table = jQuery("<table class=\"tabsort tbl_header\" style=\"overflow-x: hidden;\"></table>");
        table.append(glob.ACTIVE_PAGE.page.find("table.tabsort thead"));
        glob.ACTIVE_PAGE.page.find(".tbl_scroll").before(table);
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function () {
            tab2.push(jQuery(this).width());
        });
        tab2 = tab2.reverse();
        glob.ACTIVE_PAGE.page.find("table[name='tabsort'] tr:first td").each(function () {
            var x;
            x = tab2.pop();
            if (x > jQuery(this).width()) {
                jQuery(this).css("min-width", x);
            }
        });
        tab = tab.reverse();
        glob.ACTIVE_PAGE.page.find(".tbl_header th").each(function () {
            jQuery(this).width(tab.pop());
        });
        jQuery(window).resize(resize_win);
        resize_win();
    };

    ρσ_modules.scrolltbl.stick_resize = stick_resize;
    ρσ_modules.scrolltbl.resize_win = resize_win;
    ρσ_modules.scrolltbl.stick_header = stick_header;
})();

(function(){
    var __name__ = "tools";
    var LOADED_FILES;
    LOADED_FILES = {};
    function download_binary_file(buf, content_disposition) {
        var l, buffer, view, i, mimetype, blob, blobURL;
        l = buf.length;
        buffer = new ArrayBuffer(l);
        view = new Uint8Array(buffer);
        for (var ρσ_Index0 = 0; ρσ_Index0 < l; ρσ_Index0++) {
            i = ρσ_Index0;
            view[(typeof i === "number" && i < 0) ? view.length + i : i] = buf.charCodeAt(i);
        }
        mimetype = "text/html";
        if (ρσ_in("odf", content_disposition) || ρσ_in("ods", content_disposition)) {
            mimetype = "application/vnd.oasis.opendocument.formula";
        } else if (ρσ_in("pdf", content_disposition)) {
            mimetype = "application/pdf";
        } else if (ρσ_in("zip", content_disposition)) {
            mimetype = "application/x-compressed";
        } else if (ρσ_in("xls", content_disposition)) {
            mimetype = "application/excel";
        }
        blob = new Blob(ρσ_list_decorate([ view ]), (function(){
            var ρσ_d = {};
            ρσ_d["type"] = mimetype;
            return ρσ_d;
        }).call(this));
        blobURL = window.URL.createObjectURL(blob);
        window.open(blobURL);
    };
    Object.defineProperties(download_binary_file, {
        __argnames__ : {value: ["buf", "content_disposition"]}
    });

    function ajax_get(url, complete) {
        var req;
        req = new XMLHttpRequest;
        function _onload() {
            var disp;
            disp = req.getResponseHeader("Content-Disposition");
            if (disp && ρσ_in("attachment", disp)) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                complete(req.responseText);
            }
        };

        req.onload = _onload;
        req.open("GET", url, true);
        req.send();
    };
    Object.defineProperties(ajax_get, {
        __argnames__ : {value: ["url", "complete"]}
    });

    function ajax_load(elem, url, complete) {
        function _onload(responseText) {
            elem.html(responseText);
            complete(responseText);
        };
        Object.defineProperties(_onload, {
            __argnames__ : {value: ["responseText"]}
        });

        ajax_get(url, _onload);
    };
    Object.defineProperties(ajax_load, {
        __argnames__ : {value: ["elem", "url", "complete"]}
    });

    function _req_post(req, url, data, complete) {
        function _onload() {
            var disp;
            disp = req.getResponseHeader("Content-Disposition");
            if (disp && ρσ_in("attachment", disp)) {
                download_binary_file(req.response, disp);
                complete(null);
            } else {
                complete(req.responseText);
            }
        };

        req.onload = _onload;
        req.open("POST", url, true);
        req.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
        if (data.length) {
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.setRequestHeader("Content-length", data.length);
            req.setRequestHeader("Connection", "close");
        }
        req.send(data);
    };
    Object.defineProperties(_req_post, {
        __argnames__ : {value: ["req", "url", "data", "complete"]}
    });

    function ajax_post(url, data, complete) {
        var req;
        req = new XMLHttpRequest;
        _req_post(req, url, data, complete);
    };
    Object.defineProperties(ajax_post, {
        __argnames__ : {value: ["url", "data", "complete"]}
    });

    function ajax_submit(form, complete) {
        var req, data;
        req = new XMLHttpRequest;
        if (form.find("[type='file']").length > 0) {
            form.attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
            data = new FormData(form[0]);
            form.closest("div").append("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
            function _progressHandlingFunction(e) {
                if (e.lengthComputable) {
                    jQuery("#progress").width("" + parseInt(100 * e.loaded / e.total) + "%");
                }
            };
            Object.defineProperties(_progressHandlingFunction, {
                __argnames__ : {value: ["e"]}
            });

            req.upload.addEventListener("progress", _progressHandlingFunction, false);
        } else {
            data = form.serialize();
        }
        _req_post(req, corect_href(form.attr("action")), data, complete);
    };
    Object.defineProperties(ajax_submit, {
        __argnames__ : {value: ["form", "complete"]}
    });

    function get_page(elem) {
        if (elem.hasClass(".tab-pane")) {
            return elem;
        } else {
            return elem.closest(".tab-pane");
        }
    };
    Object.defineProperties(get_page, {
        __argnames__ : {value: ["elem"]}
    });

    function get_table_type(elem) {
        var tabsort, ret;
        tabsort = elem.find(".tabsort");
        if ((tabsort.length === 0 || typeof tabsort.length === "object" && ρσ_equals(tabsort.length, 0))) {
            tabsort = get_page(elem).find(".tabsort");
        }
        if (tabsort.length > 0) {
            ret = tabsort.attr("table_type");
            if (ret) {
                return ret;
            } else {
                return "scrolled";
            }
        } else {
            return "";
        }
    };
    Object.defineProperties(get_table_type, {
        __argnames__ : {value: ["elem"]}
    });

    function can_popup() {
        if (jQuery("div.dialog-form").hasClass("in") || jQuery("div.dialog-form-delete").hasClass("in") || jQuery("div.dialog-form-info").hasClass("in")) {
            return false;
        } else {
            return true;
        }
    };

    function corect_href(href) {
        if (ρσ_in("only_content", href)) {
            return href;
        } else {
            if (ρσ_in("?", href)) {
                return href + "&only_content=1";
            } else {
                return href + "?only_content=1";
            }
        }
    };
    Object.defineProperties(corect_href, {
        __argnames__ : {value: ["href"]}
    });

    function handle_class_click(fragment_obj, obj_class, fun) {
        fragment_obj.on("click", "." + obj_class, (function() {
            var ρσ_anonfunc = function (e) {
                var src_obj;
                src_obj = jQuery(this);
                e.preventDefault();
                fun(this);
                return false;
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["e"]}
            });
            return ρσ_anonfunc;
        })());
    };
    Object.defineProperties(handle_class_click, {
        __argnames__ : {value: ["fragment_obj", "obj_class", "fun"]}
    });

    function load_css(path) {
        var req;
        if (!(LOADED_FILES && ρσ_in(path, LOADED_FILES))) {
            LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path] = null;
            req = new XMLHttpRequest;
            function _onload() {
                jQuery("<style type=\"text/css\"></style>").html(req.responseText).appendTo("head");
            };

            req.onload = _onload;
            req.open("GET", path, true);
            req.send("");
        }
    };
    Object.defineProperties(load_css, {
        __argnames__ : {value: ["path"]}
    });

    function on_load_js(path) {
        var functions, fun;
        if (LOADED_FILES && ρσ_in(path, LOADED_FILES)) {
            functions = LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path];
            if (functions) {
                var ρσ_Iter1 = ρσ_Iterable(functions);
                for (var ρσ_Index1 = 0; ρσ_Index1 < ρσ_Iter1.length; ρσ_Index1++) {
                    fun = ρσ_Iter1[ρσ_Index1];
                    fun();
                }
            }
            LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path] = null;
        }
    };
    Object.defineProperties(on_load_js, {
        __argnames__ : {value: ["path"]}
    });

    function load_js(path, fun) {
        var req;
        if (LOADED_FILES && ρσ_in(path, LOADED_FILES)) {
            if (LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path]) {
                LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path].push(fun);
            } else {
                fun();
            }
        } else {
            LOADED_FILES[(typeof path === "number" && path < 0) ? LOADED_FILES.length + path : path] = ρσ_list_decorate([ fun ]);
            req = new XMLHttpRequest;
            function _onload() {
                jQuery.globalEval(req.responseText);
                on_load_js(path);
            };

            req.onload = _onload;
            req.open("GET", path, true);
            req.send("");
        }
    };
    Object.defineProperties(load_js, {
        __argnames__ : {value: ["path", "fun"]}
    });

    function load_many_js(paths, fun) {
        var counter, path;
        counter = 0;
        function _fun() {
            counter = counter - 1;
            if ((counter === 0 || typeof counter === "object" && ρσ_equals(counter, 0))) {
                fun();
            }
        };

        var ρσ_Iter2 = ρσ_Iterable(paths.split(paths, ";"));
        for (var ρσ_Index2 = 0; ρσ_Index2 < ρσ_Iter2.length; ρσ_Index2++) {
            path = ρσ_Iter2[ρσ_Index2];
            if (path.lenght() > 0) {
                counter = counter + 1;
                load_js(path, _fun);
                {}
            }
        }
    };
    Object.defineProperties(load_many_js, {
        __argnames__ : {value: ["paths", "fun"]}
    });

    ρσ_modules.tools.LOADED_FILES = LOADED_FILES;
    ρσ_modules.tools.download_binary_file = download_binary_file;
    ρσ_modules.tools.ajax_get = ajax_get;
    ρσ_modules.tools.ajax_load = ajax_load;
    ρσ_modules.tools._req_post = _req_post;
    ρσ_modules.tools.ajax_post = ajax_post;
    ρσ_modules.tools.ajax_submit = ajax_submit;
    ρσ_modules.tools.get_page = get_page;
    ρσ_modules.tools.get_table_type = get_table_type;
    ρσ_modules.tools.can_popup = can_popup;
    ρσ_modules.tools.corect_href = corect_href;
    ρσ_modules.tools.handle_class_click = handle_class_click;
    ρσ_modules.tools.load_css = load_css;
    ρσ_modules.tools.on_load_js = on_load_js;
    ρσ_modules.tools.load_js = load_js;
    ρσ_modules.tools.load_many_js = load_many_js;
})();

(function(){
    var __name__ = "tbl";
    var glob = ρσ_modules.glob;

    var stick_header = ρσ_modules.scrolltbl.stick_header;

    var ajax_post = ρσ_modules.tools.ajax_post;
    var ajax_post = ρσ_modules.tools.ajax_post;

    function datetable_set_height() {
        var elem, dy_table, dy_win, dy_body1, dy_body2, dy_body, dy;
        if (jQuery(this).hasClass("table_get")) {
            return;
        }
        if (!jQuery(this).is(":visible")) {
            return;
        }
        elem = jQuery(this).closest(".tabsort_panel");
        dy_table = elem.height();
        dy_win = jQuery(window).height();
        dy_body1 = 0;
        jQuery(".win-header").each(function () {
            dy_body1 += jQuery(this).height();
        });
        dy_body2 = jQuery(".win-content").height();
        dy_body = dy_body1 + dy_body2;
        dy = dy_table + (dy_win - dy_body);
        if (dy < 200) {
            dy = 200;
        }
        jQuery(this).bootstrapTable("resetView", (function(){
            var ρσ_d = {};
            ρσ_d["height"] = dy - 10;
            return ρσ_d;
        }).call(this));
    };

    function datatable_refresh(table) {
        table.bootstrapTable("refresh");
    };
    Object.defineProperties(datatable_refresh, {
        __argnames__ : {value: ["table"]}
    });

    function _rowStyle(value, row, index) {
        var x, c;
        x = jQuery("<div>" + value["cid"] + "</div>").find("div.td_information");
        if (x.length > 0) {
            c = x.attr("class").replace("td_information", "");
            if (c.length > 0) {
                return (function(){
                    var ρσ_d = {};
                    ρσ_d["classes"] = c;
                    return ρσ_d;
                }).call(this);
            }
        }
        return {};
    };
    Object.defineProperties(_rowStyle, {
        __argnames__ : {value: ["value", "row", "index"]}
    });

    function prepare_datatable(table) {
        table.find("div.second_row").each((function() {
            var ρσ_anonfunc = function (index) {
                var td, tr, l;
                td = jQuery(this).parent();
                tr = td.parent();
                l = tr.find("td").length;
                tr.find("td:gt(0)").remove();
                td.attr("colspan", l);
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["index"]}
            });
            return ρσ_anonfunc;
        })());
    };
    Object.defineProperties(prepare_datatable, {
        __argnames__ : {value: ["table"]}
    });

    function datatable_ajax(params) {
        var url, success, form, d;
        url = params["url"];
        success = params["success"];
        if (ρσ_in("form", params["data"])) {
            form = params["data"]["form"];
            ρσ_delitem(params["data"], "form");
            d = jQuery.param(params["data"]);
            url += "?" + d;
            ajax_post(url, form, (function() {
                var ρσ_anonfunc = function (data) {
                    var d2;
                    d2 = JSON.parse(data);
                    success(d2);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["data"]}
                });
                return ρσ_anonfunc;
            })());
        } else {
            d = jQuery.param(params["data"]);
            url += "?" + d;
            ajax_get(url, (function() {
                var ρσ_anonfunc = function (data) {
                    var d2;
                    d2 = JSON.parse(data);
                    success(d2);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["data"]}
                });
                return ρσ_anonfunc;
            })());
        }
    };
    Object.defineProperties(datatable_ajax, {
        __argnames__ : {value: ["params"]}
    });

    function init_table(table, table_type) {
        if ((table_type === "scrolled" || typeof table_type === "object" && ρσ_equals(table_type, "scrolled"))) {
            stick_header();
        }
        if ((table_type === "datatable" || typeof table_type === "object" && ρσ_equals(table_type, "datatable"))) {
            function onLoadSuccess(data) {
                prepare_datatable(table);
                datatable_onresize();
                return false;
            };
            Object.defineProperties(onLoadSuccess, {
                __argnames__ : {value: ["data"]}
            });

            function queryParams(p) {
                var refr_block, src;
                refr_block = jQuery(table).closest(".refr_object");
                src = refr_block.find(".refr_source");
                if (src.length > 0 && ρσ_equals(src.prop("tagName"), "FORM")) {
                    p["form"] = src.serialize();
                }
                return p;
            };
            Object.defineProperties(queryParams, {
                __argnames__ : {value: ["p"]}
            });

            if (table.hasClass("table_get")) {
                table.bootstrapTable((function(){
                    var ρσ_d = {};
                    ρσ_d["onLoadSuccess"] = onLoadSuccess;
                    ρσ_d["height"] = 350;
                    ρσ_d["rowStyle"] = _rowStyle;
                    ρσ_d["queryParams"] = queryParams;
                    ρσ_d["ajax"] = datatable_ajax;
                    return ρσ_d;
                }).call(this));
            } else {
                table.bootstrapTable((function(){
                    var ρσ_d = {};
                    ρσ_d["onLoadSuccess"] = onLoadSuccess;
                    ρσ_d["rowStyle"] = _rowStyle;
                    ρσ_d["queryParams"] = queryParams;
                    ρσ_d["ajax"] = datatable_ajax;
                    return ρσ_d;
                }).call(this));
            }
        }
    };
    Object.defineProperties(init_table, {
        __argnames__ : {value: ["table", "table_type"]}
    });

    function datatable_onresize() {
        jQuery(".datatable:not(.table_get)").each(datetable_set_height);
    };

    ρσ_modules.tbl.datetable_set_height = datetable_set_height;
    ρσ_modules.tbl.datatable_refresh = datatable_refresh;
    ρσ_modules.tbl._rowStyle = _rowStyle;
    ρσ_modules.tbl.prepare_datatable = prepare_datatable;
    ρσ_modules.tbl.datatable_ajax = datatable_ajax;
    ρσ_modules.tbl.init_table = init_table;
    ρσ_modules.tbl.datatable_onresize = datatable_onresize;
})();

(function(){
    var __name__ = "tabmenu";
    var glob = ρσ_modules.glob;

    var Page = ρσ_modules.page.Page;

    var TabMenuItem = ρσ_modules.tabmenuitem.TabMenuItem;

    var datatable_onresize = ρσ_modules.tbl.datatable_onresize;

    function TabMenu() {
        if (this.ρσ_object_id === undefined) Object.defineProperty(this, "ρσ_object_id", {"value":++ρσ_object_counter});
        TabMenu.prototype.__init__.apply(this, arguments);
    }
    TabMenu.prototype.__init__ = function __init__() {
        var self = this;
        self.id = 0;
        self.titles = {};
        self.active_item = null;
    };
    Object.defineProperties(TabMenu.prototype.__init__, {
        __argnames__ : {value: []}
    });
    TabMenu.__argnames__ = TabMenu.prototype.__init__.__argnames__;
    TabMenu.__handles_kwarg_interpolation__ = TabMenu.prototype.__init__.__handles_kwarg_interpolation__;
    TabMenu.prototype.get_active_item = function get_active_item() {
        var self = this;
        return self.active_item;
    };
    Object.defineProperties(TabMenu.prototype.get_active_item, {
        __argnames__ : {value: []}
    });
    TabMenu.prototype.is_open = function is_open(title) {
        var self = this;
        if (self.titles && ρσ_in(title, self.titles) && (ρσ_expr_temp = self.titles)[(typeof title === "number" && title < 0) ? ρσ_expr_temp.length + title : title]) {
            return true;
        } else {
            return false;
        }
    };
    Object.defineProperties(TabMenu.prototype.is_open, {
        __argnames__ : {value: ["title"]}
    });
    TabMenu.prototype.activate = function activate() {
        var self = this;
        var title = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
        var push_state = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? activate.__defaults__.push_state : arguments[1];
        var ρσ_kwargs_obj = arguments[arguments.length-1];
        if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
        if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "push_state")){
            push_state = ρσ_kwargs_obj.push_state;
        }
        var menu_item;
        menu_item = (ρσ_expr_temp = self.titles)[(typeof title === "number" && title < 0) ? ρσ_expr_temp.length + title : title];
        jQuery(sprintf("#li_%s a", menu_item.id)).tab("show");
        if (push_state && PUSH_STATE) {
            history_push_state(menu_item.title, menu_item.url);
        }
        datatable_onresize();
    };
    Object.defineProperties(TabMenu.prototype.activate, {
        __defaults__ : {value: {push_state:true}},
        __handles_kwarg_interpolation__ : {value: true},
        __argnames__ : {value: ["title", "push_state"]}
    });
    TabMenu.prototype.new_page = function new_page(title, data, href, riot_init) {
        var self = this;
        var _id, title2, menu_item, scripts;
        _id = "tab" + self.id;
        title2 = jQuery.trim(title);
        menu_item = new TabMenuItem(_id, title2, href, data);
        (ρσ_expr_temp = self.titles)[(typeof title2 === "number" && title2 < 0) ? ρσ_expr_temp.length + title2 : title2] = menu_item;
        jQuery("#tabs2").append(vsprintf("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-raised btn-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", ρσ_list_decorate([ _id, _id, title2, _id ])));
        jQuery("#tabs2_content").append(sprintf("<div class='tab-pane' id='%s'></div>", _id));
        glob.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id));
        self.active_item = menu_item;
        jQuery("#" + _id).html(data);
        if (PUSH_STATE) {
            history_push_state(title2, href);
        }
        jQuery("#tabs2 a:last").on("shown.bs.tab", (function() {
            var ρσ_anonfunc = function (e) {
                var menu;
                glob.ACTIVE_PAGE = new Page(_id, jQuery("#" + _id), menu_item);
                menu = get_menu();
                menu_item = (ρσ_expr_temp = menu.titles)[ρσ_bound_index(jQuery.trim(e.target.text), ρσ_expr_temp)];
                self.active_item = menu_item;
                if (PUSH_STATE) {
                    history_push_state(menu_item.title, menu_item.url);
                }
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["e"]}
            });
            return ρσ_anonfunc;
        })());
        jQuery("#tabs2 a:last").tab("show");
        page_init(_id, false);
        jQuery(sprintf("#button_%s", _id)).click((function() {
            var ρσ_anonfunc = function (event) {
                get_menu().remove_page(jQuery(this).attr("id").replace("button_", ""));
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["event"]}
            });
            return ρσ_anonfunc;
        })());
        scripts = jQuery("#" + _id + " script");
        scripts.each((function() {
            var ρσ_anonfunc = function (index, element) {
                eval(this.innerHTML);
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["index", "element"]}
            });
            return ρσ_anonfunc;
        })());
        self.id += 1;
        return _id;
    };
    Object.defineProperties(TabMenu.prototype.new_page, {
        __argnames__ : {value: ["title", "data", "href", "riot_init"]}
    });
    TabMenu.prototype.remove_page = function remove_page(id) {
        var self = this;
        jQuery.each(self.titles, (function() {
            var ρσ_anonfunc = function (index, value) {
                if (value && (value.id === id || typeof value.id === "object" && ρσ_equals(value.id, id))) {
                    (ρσ_expr_temp = self.titles)[(typeof index === "number" && index < 0) ? ρσ_expr_temp.length + index : index] = null;
                }
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["index", "value"]}
            });
            return ρσ_anonfunc;
        })());
        jQuery(sprintf("#li_%s", id)).remove();
        jQuery(sprintf("#%s", id)).remove();
        jQuery("#tabs2 a:last").tab("show");
    };
    Object.defineProperties(TabMenu.prototype.remove_page, {
        __argnames__ : {value: ["id"]}
    });
    TabMenu.prototype.__repr__ = function __repr__ () {
                return "<" + __name__ + "." + this.constructor.name + " #" + this.ρσ_object_id + ">";
    };
    TabMenu.prototype.__str__ = function __str__ () {
        return this.__repr__();
    };
    Object.defineProperty(TabMenu.prototype, "__bases__", {value: []});

    function get_menu() {
        if (!MENU) {
            MENU = new TabMenu;
        }
        return MENU;
    };

    ρσ_modules.tabmenu.TabMenu = TabMenu;
    ρσ_modules.tabmenu.get_menu = get_menu;
})();

(function(){
    var __name__ = "popup";
    var can_popup = ρσ_modules.tools.can_popup;
    var corect_href = ρσ_modules.tools.corect_href;
    var ajax_load = ρσ_modules.tools.ajax_load;
    var ajax_get = ρσ_modules.tools.ajax_get;
    var ajax_post = ρσ_modules.tools.ajax_post;

    var datatable_refresh = ρσ_modules.tbl.datatable_refresh;

    function refresh_fragment() {
        var data_item_to_refresh = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
        var fun = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? refresh_fragment.__defaults__.fun : arguments[1];
        var only_table = (arguments[2] === undefined || ( 2 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? refresh_fragment.__defaults__.only_table : arguments[2];
        var ρσ_kwargs_obj = arguments[arguments.length-1];
        if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
        if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "fun")){
            fun = ρσ_kwargs_obj.fun;
        }
        if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "only_table")){
            only_table = ρσ_kwargs_obj.only_table;
        }
        var refr_block, target, datatable, src, href;
        refr_block = data_item_to_refresh.closest(".refr_object");
        if (refr_block.hasClass("refr_target")) {
            target = refr_block;
        } else {
            target = refr_block.find(".refr_target");
        }
        if (only_table) {
            datatable = target.find("table[name=tabsort].datatable");
            if (datatable.length > 0) {
                datatable_refresh(datatable);
                if (fun) {
                    fun();
                }
                return true;
            }
            return false;
        }
        src = refr_block.find(".refr_source");
        if (src.length > 0) {
            href = src.attr("href");
            if (ρσ_equals(src.prop("tagName"), "FORM")) {
                function _refr2(data) {
                    target.html(data);
                    fragment_init(target);
                    if (fun) {
                        fun();
                    }
                };
                Object.defineProperties(_refr2, {
                    __argnames__ : {value: ["data"]}
                });

                ajax_post(corect_href(href), src.serialize(), _refr2);
            } else {
                ajax_load(target, corect_href(href), (function() {
                    var ρσ_anonfunc = function (responseText) {
                    };
                    Object.defineProperties(ρσ_anonfunc, {
                        __argnames__ : {value: ["responseText"]}
                    });
                    return ρσ_anonfunc;
                })());
            }
        }
        return true;
    };
    Object.defineProperties(refresh_fragment, {
        __defaults__ : {value: {fun:null, only_table:false}},
        __handles_kwarg_interpolation__ : {value: true},
        __argnames__ : {value: ["data_item_to_refresh", "fun", "only_table"]}
    });

    function on_popup_inline(elem) {
        var id, href2, new_fragment, elem2;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (WAIT_ICON) {
            WAIT_ICON.start();
        }
        jQuery(elem).closest("table").find(".inline_dialog").remove();
        COUNTER = COUNTER + 1;
        id = COUNTER;
        href2 = corect_href(jQuery(elem).attr("href"));
        new_fragment = jQuery("<tr class='refr_source inline_dialog hide' id='IDIAL_" + id + "' href='" + href2 + "'><td colspan='20'>" + INLINE_TABLE_HTML + "</td></tr>");
        new_fragment.insertAfter(jQuery(elem).closest("tr"));
        elem2 = new_fragment.find(".refr_target");
        ajax_load(elem2, href2, (function() {
            var ρσ_anonfunc = function (responseText, status, response) {
                jQuery("#IDIAL_" + id).hide();
                jQuery("#IDIAL_" + id).removeClass("hide");
                jQuery("#IDIAL_" + id).show("slow");
                if ((status !== "error" && (typeof status !== "object" || ρσ_not_equals(status, "error")))) {
                    _dialog_loaded(false, elem2);
                    on_dialog_load();
                }
                if (WAIT_ICON) {
                    WAIT_ICON.stop();
                    WAIT_ICON = null;
                }
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["responseText", "status", "response"]}
            });
            return ρσ_anonfunc;
        })());
        return false;
    };
    Object.defineProperties(on_popup_inline, {
        __argnames__ : {value: ["elem"]}
    });

    function on_popup_in_form(elem) {
        var id, href2, new_fragment, elem2;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (WAIT_ICON) {
            WAIT_ICON.start();
        }
        jQuery(elem).closest("div.Dialog").find(".inline_dialog").remove();
        COUNTER = COUNTER + 1;
        id = COUNTER;
        href2 = corect_href(jQuery(elem).attr("href"));
        new_fragment = jQuery("<div class='refr_source inline_dialog hide' id='IDIAL_" + id + "' href='" + href2 + "'>" + INLINE_TABLE_HTML + "</div>");
        new_fragment.insertAfter(jQuery(elem).closest("div.form-group"));
        elem2 = new_fragment.find(".refr_target");
        ajax_load(elem2, href2, (function() {
            var ρσ_anonfunc = function (responseText, status, response) {
                var table_type, tbl;
                jQuery("#IDIAL_" + id).hide();
                jQuery("#IDIAL_" + id).removeClass("hide");
                jQuery("#IDIAL_" + id).show("slow");
                if ((status !== "error" && (typeof status !== "object" || ρσ_not_equals(status, "error")))) {
                    _dialog_loaded(false, elem2);
                    table_type = get_table_type(elem2);
                    tbl = elem2.find(".tabsort");
                    if (tbl.length > 0) {
                        init_table(tbl, table_type);
                    }
                    on_dialog_load();
                }
                if (WAIT_ICON) {
                    WAIT_ICON.stop();
                    WAIT_ICON = null;
                }
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["responseText", "status", "response"]}
            });
            return ρσ_anonfunc;
        })());
        return false;
    };
    Object.defineProperties(on_popup_in_form, {
        __argnames__ : {value: ["elem"]}
    });

    function on_popup_edit_new(elem) {
        var elem2, test, elem3;
        jQuery(elem).attr("data-style", "zoom-out");
        jQuery(elem).attr("data-spinner-color", "#FF0000");
        WAIT_ICON = Ladda.create(elem);
        if (can_popup() && !jQuery(elem).hasClass("inline") && !(jQuery(elem).attr("name") && ρσ_in("_inline", jQuery(elem).attr("name")))) {
            elem2 = jQuery("div.dialog-data");
            elem2.closest(".refr_object").attr("related-object", jQuery(elem).uid());
            ajax_load(elem2, jQuery(elem).attr("href"), (function() {
                var ρσ_anonfunc = function (responseText, status, response) {
                    _dialog_loaded(true, elem2);
                    on_dialog_load();
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["responseText", "status", "response"]}
                });
                return ρσ_anonfunc;
            })());
        } else {
            if (WAIT_ICON) {
                WAIT_ICON.start();
            }
            if (jQuery(elem).hasClass("new-row")) {
                elem2 = jQuery("<div class='refr_source inline_dialog tr hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>");
                elem2.insertAfter(jQuery(elem).closest("div.tr"));
            } else {
                test = jQuery(elem).closest("form");
                if (test.length > 0) {
                    elem2 = jQuery("<div class='refr_source inline_dialog hide'>" + INLINE_DIALOG_UPDATE_HTML + "</div>");
                    elem2.insertAfter(jQuery(elem).closest("div.form-group"));
                } else {
                    elem2 = jQuery("<tr class='inline_dialog hide'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML + "</td></tr>");
                    elem2.insertAfter(jQuery(elem).closest("tr"));
                }
            }
            elem2.find(".modal-title").html(jQuery(elem).attr("title"));
            elem2.find(".refr_object").attr("related-object", jQuery(elem).uid());
            elem3 = elem2.find("div.dialog-data-inner");
            ajax_load(elem3, jQuery(elem).attr("href"), (function() {
                var ρσ_anonfunc = function (responseText, status, response) {
                    var table_type;
                    elem2.hide();
                    elem2.removeClass("hide");
                    elem2.show("slow");
                    if ((status !== "error" && (typeof status !== "object" || ρσ_not_equals(status, "error")))) {
                        _dialog_loaded(false, elem3);
                        table_type = get_table_type(elem3);
                        init_table(elem3, table_type);
                        on_dialog_load();
                    }
                    if (WAIT_ICON) {
                        WAIT_ICON.stop();
                        WAIT_ICON = null;
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["responseText", "status", "response"]}
                });
                return ρσ_anonfunc;
            })());
        }
        return false;
    };
    Object.defineProperties(on_popup_edit_new, {
        __argnames__ : {value: ["elem"]}
    });

    function on_popup_info(elem) {
        if (can_popup()) {
            ajax_load(jQuery("div.dialog-data-info"), jQuery(elem).attr("href"), (function() {
                var ρσ_anonfunc = function (responseText, status, response) {
                    jQuery("div.dialog-form-info").modal();
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["responseText", "status", "response"]}
                });
                return ρσ_anonfunc;
            })());
        } else {
            jQuery(".inline_dialog").remove();
            jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML + "</td></tr>").insertAfter(jQuery(elem).parents("tr"));
            ajax_load(jQuery("div.dialog-data-inner"), jQuery(elem).attr("href"), (function() {
                var ρσ_anonfunc = function (responseText, status, response) {
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["responseText", "status", "response"]}
                });
                return ρσ_anonfunc;
            })());
        }
        return false;
    };
    Object.defineProperties(on_popup_info, {
        __argnames__ : {value: ["elem"]}
    });

    function on_popup_delete(elem) {
        var elem2;
        if (can_popup()) {
            jQuery("div.dialog-data-delete").closest(".refr_object").attr("related-object", jQuery(elem).uid());
            ajax_load(jQuery("div.dialog-data-delete"), jQuery(elem).attr("href"), (function() {
                var ρσ_anonfunc = function (responseText, status, response) {
                    jQuery("div.dialog-form-delete").modal();
                    jQuery("div.dialog-form-delete").fadeTo("fast", 1);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["responseText", "status", "response"]}
                });
                return ρσ_anonfunc;
            })());
        } else {
            jQuery(".inline_dialog").remove();
            elem2 = jQuery("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML + "</td></tr>");
            elem2.insertAfter(jQuery(elem).parents("tr"));
            elem2.find(".refr_object").attr("related-object", jQuery(elem).uid());
            ajax_load(jQuery("div.dialog-data-inner"), jQuery(elem).attr("href"), function () {
            });
        }
        return false;
    };
    Object.defineProperties(on_popup_delete, {
        __argnames__ : {value: ["elem"]}
    });

    function on_dialog_load() {
    };

    function _dialog_loaded(is_modal, elem) {
        fragment_init(elem);
        if (is_modal) {
            jQuery("div.dialog-form").fadeTo("fast", 1);
            if (jQuery("div.dialog-form").find("div.form2columns").length > 0) {
                jQuery("div.dialog-form").find(".modal-dialog").addClass("modal-lg");
            } else {
                jQuery("div.dialog-form").find(".modal-dialog").removeClass("modal-lg");
            }
            jQuery("div.dialog-form").modal();
            jQuery("div.dialog-form").drags((function(){
                var ρσ_d = {};
                ρσ_d["handle"] = ".modal-header";
                return ρσ_d;
            }).call(this));
        }
    };
    Object.defineProperties(_dialog_loaded, {
        __argnames__ : {value: ["is_modal", "elem"]}
    });

    function _refresh_win(responseText, ok_button) {
        var popup_activator, dialog;
        popup_activator = jQuery("#" + jQuery(ok_button).closest(".refr_object").attr("related-object"));
        if (responseText && ρσ_in("RETURN_OK", responseText)) {
            if (!can_popup()) {
                if (jQuery("div.dialog-form").hasClass("in")) {
                    dialog = "div.dialog-form";
                } else {
                    if (jQuery("div.dialog-form-delete").hasClass("in")) {
                        dialog = "div.dialog-form-delete";
                    } else {
                        dialog = "div.dialog-form-info";
                    }
                }
                function hide_dialog_form() {
                    jQuery(dialog).modal("hide");
                };

                jQuery(dialog).fadeTo("slow", .5);
                if (!refresh_fragment(popup_activator, hide_dialog_form, true)) {
                    refresh_fragment(popup_activator, hide_dialog_form, false);
                }
            } else {
                if (!refresh_fragment(popup_activator, null, true)) {
                    return refresh_fragment(popup_activator, null, true);
                }
            }
        } else {
            if (!can_popup()) {
                jQuery("div.dialog-data").html(responseText);
            } else {
                ok_button.closest(".refr_target").html(responseText);
            }
        }
    };
    Object.defineProperties(_refresh_win, {
        __argnames__ : {value: ["responseText", "ok_button"]}
    });

    function _refresh_win_and_ret(responseText, ok_button) {
        var related_object, popup_activator, RET_CONTROL, EDIT_RET_FUNCTION, q;
        if (responseText && ρσ_in("RETURN_OK", responseText)) {
            related_object = jQuery(ok_button).closest(".refr_object").attr("related-object");
            popup_activator = jQuery("#" + related_object);
            if (jQuery(ok_button).closest(".refr_object").hasClass("in")) {
                jQuery("div.dialog-form").modal("hide");
            } else {
                jQuery(ok_button).closest(".refr_object").remove();
            }
            if (popup_activator && popup_activator.data("edit_ret_function")) {
                RET_CONTROL = popup_activator.data("ret_control");
                EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function");
                q = jQuery(responseText);
                eval(q[1].text);
            }
        } else {
            jQuery("div.dialog-data").html(responseText);
        }
    };
    Object.defineProperties(_refresh_win_and_ret, {
        __argnames__ : {value: ["responseText", "ok_button"]}
    });

    function _refresh_win_after_ok(responseText, ok_button) {
        var related_object, popup_activator;
        related_object = jQuery(ok_button).closest(".refr_object").attr("related-object");
        popup_activator = jQuery("#" + related_object);
        if (popup_activator && popup_activator.data("edit_ret_function")) {
            EDIT_RET_FUNCTION = popup_activator.data("edit_ret_function");
            EDIT_RET_FUNCTION(responseText, ok_button);
            EDIT_RET_FUNCTION = false;
        } else {
            _refresh_win(responseText, ok_button);
        }
    };
    Object.defineProperties(_refresh_win_after_ok, {
        __argnames__ : {value: ["responseText", "ok_button"]}
    });

    function on_edit_ok(form) {
        function _fun(data) {
            _refresh_win_after_ok(data, form);
        };
        Object.defineProperties(_fun, {
            __argnames__ : {value: ["data"]}
        });

        ajax_submit(form, _fun);
        return false;
    };
    Object.defineProperties(on_edit_ok, {
        __argnames__ : {value: ["form"]}
    });

    function on_delete_ok(form) {
        ajax_post(corect_href(form.attr("action")), form.serialize(), (function() {
            var ρσ_anonfunc = function (data) {
                _refresh_win(data, form);
            };
            Object.defineProperties(ρσ_anonfunc, {
                __argnames__ : {value: ["data"]}
            });
            return ρσ_anonfunc;
        })());
        return false;
    };
    Object.defineProperties(on_delete_ok, {
        __argnames__ : {value: ["form"]}
    });

    function on_cancel_inline(elem) {
        jQuery(elem).closest(".inline_dialog").remove();
    };
    Object.defineProperties(on_cancel_inline, {
        __argnames__ : {value: ["elem"]}
    });

    function ret_ok(id, title) {
        RET_CONTROL.select2("data", (function(){
            var ρσ_d = {};
            ρσ_d[id] = id;
            ρσ_d[text] = title;
            return ρσ_d;
        }).call(this)).trigger("change");
        RET_CONTROL.val(id.toString());
        RET_CONTROL[0].defaultValue = id.toString();
    };
    Object.defineProperties(ret_ok, {
        __argnames__ : {value: ["id", "title"]}
    });

    function on_get_tbl_value(elem) {
        on_popup_in_form(elem);
    };
    Object.defineProperties(on_get_tbl_value, {
        __argnames__ : {value: ["elem"]}
    });

    function on_new_tbl_value(elem) {
        EDIT_RET_FUNCTION = _refresh_win_and_ret;
        RET_CONTROL = jQuery(elem).closest(".input-group").find(".django-select2");
        jQuery(elem).data("edit_ret_function", EDIT_RET_FUNCTION);
        jQuery(elem).data("ret_control", RET_CONTROL);
        return on_popup_edit_new(elem);
    };
    Object.defineProperties(on_new_tbl_value, {
        __argnames__ : {value: ["elem"]}
    });

    function on_get_row(elem) {
        var id, text, ret_control;
        id = jQuery(elem).attr("data-id");
        text = jQuery(elem).attr("data-text");
        ret_control = jQuery(elem).closest(".refr_source").prev(".form-group").find(".django-select2");
        if ((ret_control.find("option[value='" + id + "']").length === 0 || typeof ret_control.find("option[value='" + id + "']").length === "object" && ρσ_equals(ret_control.find("option[value='" + id + "']").length, 0))) {
            ret_control.append(jQuery("<option>", (function(){
                var ρσ_d = {};
                ρσ_d["value"] = id;
                ρσ_d["text"] = text;
                return ρσ_d;
            }).call(this)));
        }
        ret_control.val(id.toString());
        ret_control.trigger("change");
        jQuery(elem).closest(".refr_source").remove();
    };
    Object.defineProperties(on_get_row, {
        __argnames__ : {value: ["elem"]}
    });

    ρσ_modules.popup.refresh_fragment = refresh_fragment;
    ρσ_modules.popup.on_popup_inline = on_popup_inline;
    ρσ_modules.popup.on_popup_in_form = on_popup_in_form;
    ρσ_modules.popup.on_popup_edit_new = on_popup_edit_new;
    ρσ_modules.popup.on_popup_info = on_popup_info;
    ρσ_modules.popup.on_popup_delete = on_popup_delete;
    ρσ_modules.popup.on_dialog_load = on_dialog_load;
    ρσ_modules.popup._dialog_loaded = _dialog_loaded;
    ρσ_modules.popup._refresh_win = _refresh_win;
    ρσ_modules.popup._refresh_win_and_ret = _refresh_win_and_ret;
    ρσ_modules.popup._refresh_win_after_ok = _refresh_win_after_ok;
    ρσ_modules.popup.on_edit_ok = on_edit_ok;
    ρσ_modules.popup.on_delete_ok = on_delete_ok;
    ρσ_modules.popup.on_cancel_inline = on_cancel_inline;
    ρσ_modules.popup.ret_ok = ret_ok;
    ρσ_modules.popup.on_get_tbl_value = on_get_tbl_value;
    ρσ_modules.popup.on_new_tbl_value = on_new_tbl_value;
    ρσ_modules.popup.on_get_row = on_get_row;
})();

var __name__ = "__main__";

var APPLICATION_TEMPLATE, RET_BUFOR, RET_OBJ, LANG, MENU, PUSH_STATE, BASE_PATH, WAIT_ICON, WAIT_ICON2, MENU_ID, BASE_FRAGMENT_INIT, COUNTER, EDIT_RET_FUNCTION, RET_CONTROL, RIOT_INIT;
APPLICATION_TEMPLATE = "standard";
RET_BUFOR = null;
RET_OBJ = null;
LANG = "en";
MENU = null;
PUSH_STATE = true;
BASE_PATH = null;
WAIT_ICON = null;
WAIT_ICON2 = false;
MENU_ID = 0;
BASE_FRAGMENT_INIT = null;
COUNTER = 1;
EDIT_RET_FUNCTION = null;
RET_CONTROL = null;
RIOT_INIT = null;
var glob = ρσ_modules.glob;

var Page = ρσ_modules.page.Page;

var TabMenuItem = ρσ_modules.tabmenuitem.TabMenuItem;

var get_menu = ρσ_modules.tabmenu.get_menu;

var on_get_tbl_value = ρσ_modules.popup.on_get_tbl_value;
var on_new_tbl_value = ρσ_modules.popup.on_new_tbl_value;
var on_get_row = ρσ_modules.popup.on_get_row;
var on_popup_edit_new = ρσ_modules.popup.on_popup_edit_new;
var on_popup_inline = ρσ_modules.popup.on_popup_inline;
var on_popup_info = ρσ_modules.popup.on_popup_info;
var on_popup_delete = ρσ_modules.popup.on_popup_delete;
var on_cancel_inline = ρσ_modules.popup.on_cancel_inline;
var refresh_fragment = ρσ_modules.popup.refresh_fragment;
var on_edit_ok = ρσ_modules.popup.on_edit_ok;
var on_delete_ok = ρσ_modules.popup.on_delete_ok;
var ret_ok = ρσ_modules.popup.ret_ok;

var init_table = ρσ_modules.tbl.init_table;
var datatable_onresize = ρσ_modules.tbl.datatable_onresize;

var can_popup = ρσ_modules.tools.can_popup;
var corect_href = ρσ_modules.tools.corect_href;
var get_table_type = ρσ_modules.tools.get_table_type;
var handle_class_click = ρσ_modules.tools.handle_class_click;
var ajax_get = ρσ_modules.tools.ajax_get;
var ajax_post = ρσ_modules.tools.ajax_post;
var ajax_load = ρσ_modules.tools.ajax_load;
var ajax_submit = ρσ_modules.tools.ajax_submit;
var load_css = ρσ_modules.tools.load_css;
var load_js = ρσ_modules.tools.load_js;
var load_many_js = ρσ_modules.tools.load_many_js;

function init_pagintor(pg) {
    var paginate, totalPages, page_number, options, form, url;
    if (pg.length > 0) {
        paginate = true;
        totalPages = pg.attr("totalPages");
        page_number = pg.attr("start_page");
        options = (function(){
            var ρσ_d = {};
            ρσ_d["totalPages"] = +totalPages;
            ρσ_d["startPage"] = +page_number;
            ρσ_d["visiblePages"] = 3;
            ρσ_d["first"] = "<<";
            ρσ_d["prev"] = "<";
            ρσ_d["next"] = ">";
            ρσ_d["last"] = ">>";
            ρσ_d["onPageClick"] = (function() {
                var ρσ_anonfunc = function (event, page) {
                    var form, url, active_button, WAIT_ICON2;
                    form = pg.closest(".refr_object").find("form.refr_source");
                    if (form) {
                        function _on_new_page(data) {
                            pg.closest(".content").find(".tabsort tbody").html(jQuery(jQuery.parseHTML(data)).find(".tabsort tbody").html());
                            fragment_init(pg.closest(".content").find(".tabsort tbody"));
                            if (WAIT_ICON2) {
                                jQuery("#loading-indicator").hide();
                                WAIT_ICON2 = false;
                            }
                        };
                        Object.defineProperties(_on_new_page, {
                            __argnames__ : {value: ["data"]}
                        });

                        url = pg.attr("href").replace("[[page]]", page) + "&only_content=1";
                        form.attr("action", url);
                        form.attr("href", url);
                        active_button = pg.find(".page active");
                        WAIT_ICON2 = true;
                        jQuery("#loading-indicator").show();
                        ajax_post(url, form.serialize(), _on_new_page);
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["event", "page"]}
                });
                return ρσ_anonfunc;
            })();
            return ρσ_d;
        }).call(this);
        pg.twbsPagination(options);
        if ((+page_number !== 1 && (typeof +page_number !== "object" || ρσ_not_equals(+page_number, 1)))) {
            form = pg.closest(".refr_object").find("form.refr_source");
            url = pg.attr("href").replace("[[page]]", page_number) + "&only_content=1";
            form.attr("action", url);
            form.attr("href", url);
        }
    } else {
        paginate = false;
    }
    return paginate;
};
Object.defineProperties(init_pagintor, {
    __argnames__ : {value: ["pg"]}
});

function fragment_init() {
    var elem = (arguments[0] === undefined || ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? fragment_init.__defaults__.elem : arguments[0];
    var ρσ_kwargs_obj = arguments[arguments.length-1];
    if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "elem")){
        elem = ρσ_kwargs_obj.elem;
    }
    var elem2, d, _id, x, pos;
    if (elem) {
        elem2 = elem;
    } else {
        elem2 = glob.ACTIVE_PAGE.page;
    }
    handle_class_click(elem, "get_tbl_value", on_get_tbl_value);
    handle_class_click(elem, "new_tbl_value", on_new_tbl_value);
    handle_class_click(elem, "get_row", on_get_row);
    d = elem2.find(".dateinput");
    d.wrap("<div class='input-group date'></div>");
    d.after("<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span>");
    d.parent().datetimepicker((function(){
        var ρσ_d = {};
        ρσ_d["format"] = "YYYY-MM-DD";
        ρσ_d["locale"] = "pl";
        ρσ_d["showTodayButton"] = true;
        return ρσ_d;
    }).call(this));
    d = elem2.find(".datetimeinput");
    d.wrap("<div class='input-group date datetime'></div>");
    d.after("<span class='input-group-addon'><span class='glyphicon glyphicon-time'></span></span>");
    d.parent().datetimepicker((function(){
        var ρσ_d = {};
        ρσ_d["format"] = "YYYY-MM-DD hh:mm";
        ρσ_d["locale"] = "pl";
        ρσ_d["showTodayButton"] = true;
        return ρσ_d;
    }).call(this));
    elem2.find(".win-content").bind("resize", datatable_onresize);
    jQuery(".selectpicker").selectpicker();
    if (RIOT_INIT) {
        _id = jQuery(elem).uid();
        var ρσ_Iter0 = ρσ_Iterable(RIOT_INIT);
        for (var ρσ_Index0 = 0; ρσ_Index0 < ρσ_Iter0.length; ρσ_Index0++) {
            pos = ρσ_Iter0[ρσ_Index0];
            x = sprintf("riot.mount('#%s')", _id + " " + pos);
            eval(x);
        }
    }
    if (BASE_FRAGMENT_INIT) {
        BASE_FRAGMENT_INIT();
    }
    datatable_onresize();
};
Object.defineProperties(fragment_init, {
    __defaults__ : {value: {elem:null}},
    __handles_kwarg_interpolation__ : {value: true},
    __argnames__ : {value: ["elem"]}
});

function page_init() {
    var id = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
    var first_time = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? page_init.__defaults__.first_time : arguments[1];
    var ρσ_kwargs_obj = arguments[arguments.length-1];
    if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "first_time")){
        first_time = ρσ_kwargs_obj.first_time;
    }
    var table_type, pg, paginate, elem2;
    table_type = get_table_type(jQuery("#" + id));
    if ((table_type !== "datatable" && (typeof table_type !== "object" || ρσ_not_equals(table_type, "datatable")))) {
        if (glob.ACTIVE_PAGE) {
            pg = glob.ACTIVE_PAGE.page.find(".pagination");
            paginate = init_pagintor(pg);
        }
    }
    init_table(jQuery("#" + id + " .tabsort"), table_type);
    if (first_time) {
        elem2 = jQuery("body");
    }
    jQuery("#" + id).on("click", "a", (function() {
        var ρσ_anonfunc = function (e) {
            var target, src_obj, pos, href, title, href2;
            target = jQuery(e.currentTarget).attr("target");
            src_obj = jQuery(this);
            if ((target === "_blank" || typeof target === "object" && ρσ_equals(target, "_blank"))) {
                return;
            }
            var ρσ_Iter1 = ρσ_Iterable(ρσ_list_decorate([ "get_tbl_value", "new_tbl_value", "get_row" ]));
            for (var ρσ_Index1 = 0; ρσ_Index1 < ρσ_Iter1.length; ρσ_Index1++) {
                pos = ρσ_Iter1[ρσ_Index1];
                if (jQuery(this).hasClass(pos)) {
                    return true;
                }
            }
            var ρσ_Iter2 = ρσ_Iterable(ρσ_list_decorate([ ["popup", on_popup_edit_new], ["popup_inline", 
            on_popup_inline], ["popup_info", on_popup_info], ["popup_delete", on_popup_delete] ]));
            for (var ρσ_Index2 = 0; ρσ_Index2 < ρσ_Iter2.length; ρσ_Index2++) {
                pos = ρσ_Iter2[ρσ_Index2];
                if (jQuery(this).hasClass(pos[0])) {
                    e.preventDefault();
                    pos[1](this);
                    return true;
                }
            }
            href = jQuery(this).attr("href");
            if (href && ρσ_in("#", href)) {
                return true;
            }
            e.preventDefault();
            if (ρσ_in(jQuery(e.currentTarget).attr("target"), ["_top", "_top2"])) {
                title = jQuery(e.currentTarget).attr("title");
                if (!title) {
                    if (len(href) > 16) {
                        title = "..." + href.slice(-13);
                    } else {
                        title = href;
                    }
                }
                return _on_menu_href(this, title);
            }
            href2 = corect_href(href);
            ajax_get(href2, (function() {
                var ρσ_anonfunc = function (data) {
                    if (data && ρσ_in("_parent_refr", data) || ρσ_in(target, ["refresh_obj", "refresh_page"])) {
                        if ((target === "refresh_obj" || typeof target === "object" && ρσ_equals(target, "refresh_obj"))) {
                            if (!refresh_fragment(src_obj, null, true)) {
                                refresh_fragment(src_obj);
                            }
                        } else {
                            refresh_fragment(src_obj);
                        }
                    } else {
                        if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern"))) {
                            glob.ACTIVE_PAGE.page.html(data);
                            glob.ACTIVE_PAGE.set_href(href);
                            page_init(glob.ACTIVE_PAGE.id, false);
                        } else {
                            jQuery("#body_body").html(data);
                            page_init("body_body", false);
                        }
                        glob.ACTIVE_PAGE.set_href(href);
                        get_menu().get_active_item().url = href;
                        if (PUSH_STATE) {
                            history_push_state("title", href);
                        }
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["data"]}
                });
                return ρσ_anonfunc;
            })());
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["e"]}
        });
        return ρσ_anonfunc;
    })());
    glob.ACTIVE_PAGE.page.find("form").submit((function() {
        var ρσ_anonfunc = function (e) {
            var data, submit_button, href;
            if (ρσ_equals(jQuery(this).attr("target"), "_blank")) {
                jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
                return true;
            }
            if (ρσ_equals(jQuery(this).attr("target"), "refresh_obj")) {
                if (refresh_fragment(jQuery(this), null, true)) {
                    return false;
                }
            }
            data = jQuery(this).serialize();
            if (data && ρσ_in("pdf=on", data)) {
                jQuery(this).attr("target", "_blank");
                jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
                return true;
            }
            if (data && ρσ_in("odf=on", data)) {
                jQuery(this).attr("target", "_blank");
                jQuery(this).attr("enctype", "multipart/form-data").attr("encoding", "multipart/form-data");
                return true;
            }
            e.preventDefault();
            submit_button = jQuery(this).find("button[type=\"submit\"]");
            if (submit_button.length > 0) {
                submit_button.attr("data-style", "zoom-out");
                submit_button.attr("data-spinner-color", "#FF0000");
                WAIT_ICON = Ladda.create(submit_button[0]);
                WAIT_ICON.start();
            } else {
                WAIT_ICON2 = true;
                jQuery("#loading-indicator").show();
            }
            href = jQuery(this).attr("action");
            if (href) {
                jQuery(this).attr("action", corect_href(href));
            }
            ajax_submit(jQuery(this), (function() {
                var ρσ_anonfunc = function (data) {
                    glob.ACTIVE_PAGE.page.html(data);
                    page_init(id, false);
                    if (WAIT_ICON) {
                        WAIT_ICON.stop();
                    }
                    if (WAIT_ICON2) {
                        jQuery("#loading-indicator").hide();
                        WAIT_ICON2 = false;
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["data"]}
                });
                return ρσ_anonfunc;
            })());
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["e"]}
        });
        return ρσ_anonfunc;
    })());
    fragment_init(glob.ACTIVE_PAGE.page);
};
Object.defineProperties(page_init, {
    __defaults__ : {value: {first_time:true}},
    __handles_kwarg_interpolation__ : {value: true},
    __argnames__ : {value: ["id", "first_time"]}
});

function app_init(application_template, menu_id, lang, base_path, base_fragment_init, riot_init) {
    var SUBWIN;
    APPLICATION_TEMPLATE = application_template;
    LANG = lang;
    BASE_PATH = base_path;
    BASE_FRAGMENT_INIT = base_fragment_init;
    RIOT_INIT = riot_init;
    if (can_popup()) {
        SUBWIN = false;
        jQuery(function () {
            var pos, elem, id;
            jQuery("#tabs").tabdrop();
            jQuery("#tabs2").tabdrop();
            if ((APPLICATION_TEMPLATE !== "traditional" && (typeof APPLICATION_TEMPLATE !== "object" || ρσ_not_equals(APPLICATION_TEMPLATE, "traditional")))) {
                pos = jQuery(".menu-href.btn-warning");
                if (pos.length > 0) {
                    elem = jQuery("#a_" + pos.closest("div.tab-pane").attr("id"));
                    elem.tab("show");
                } else {
                    elem = jQuery(".first_pos");
                    elem.tab("show");
                }
            } else {
                id = int(menu_id) + 1;
                elem = jQuery("#tabs a:eq(" + id + ")");
                elem.tab("show");
            }
            jQuery(elem.prop("hash")).perfectScrollbar();
            jQuery("body").on("click", "a.menu-href", (function() {
                var ρσ_anonfunc = function (e) {
                    if ((APPLICATION_TEMPLATE !== "traditional" && (typeof APPLICATION_TEMPLATE !== "object" || ρσ_not_equals(APPLICATION_TEMPLATE, "traditional")))) {
                        e.preventDefault();
                        _on_menu_href(this);
                    }
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            jQuery("body").on("submit", "form.DialogForm", (function() {
                var ρσ_anonfunc = function (e) {
                    e.preventDefault();
                    on_edit_ok(jQuery(this));
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            jQuery("#logout").on("click", function () {
                window.location = jQuery(this).attr("action");
            });
            jQuery(".system_menu").on("click", function () {
                window.location = jQuery(this).attr("action");
            });
            jQuery("#tabs a").click((function() {
                var ρσ_anonfunc = function (e) {
                    e.preventDefault();
                    jQuery(this).tab("show");
                    jQuery(jQuery(this).prop("hash")).perfectScrollbar();
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            jQuery("#tabs2").on("shown.bs.tab", (function() {
                var ρσ_anonfunc = function (e) {
                    datatable_onresize();
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            jQuery("body").on("expanded.pushMenu collapsed.pushMenu", (function() {
                var ρσ_anonfunc = function (e) {
                    window.setTimeout(datatable_onresize, 300);
                };
                Object.defineProperties(ρσ_anonfunc, {
                    __argnames__ : {value: ["e"]}
                });
                return ρσ_anonfunc;
            })());
            jQuery(window).resize(datatable_onresize);
        });
    } else {
        SUBWIN = true;
    }
};
Object.defineProperties(app_init, {
    __argnames__ : {value: ["application_template", "menu_id", "lang", "base_path", "base_fragment_init", "riot_init"]}
});

function _on_menu_href() {
    var elem = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
    var title = (arguments[1] === undefined || ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? _on_menu_href.__defaults__.title : arguments[1];
    var ρσ_kwargs_obj = arguments[arguments.length-1];
    if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "title")){
        title = ρσ_kwargs_obj.title;
    }
    var menu, classname, href, href2;
    if ((APPLICATION_TEMPLATE !== "traditional" && (typeof APPLICATION_TEMPLATE !== "object" || ρσ_not_equals(APPLICATION_TEMPLATE, "traditional")))) {
        if (!title) {
            title = jQuery.trim(jQuery(elem).text());
        }
        menu = get_menu();
        classname = jQuery(elem).attr("class");
        if (classname && ρσ_in("btn", classname)) {
            if (WAIT_ICON) {
                WAIT_ICON.stop();
            }
            jQuery(elem).attr("data-style", "zoom-out");
            jQuery(elem).attr("data-spinner-color", "#FF0000");
            WAIT_ICON = Ladda.create(elem);
        } else {
            WAIT_ICON = null;
        }
        if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern")) && menu.is_open(title)) {
            menu.activate(title);
        } else {
            href = jQuery(elem).attr("href");
            href2 = corect_href(href);
            function _on_new_win(data) {
                var id;
                if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern"))) {
                    id = menu.new_page(title, data, href2, RIOT_INIT);
                } else {
                    jQuery("#body_body").html(data);
                    glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
                    glob.ACTIVE_PAGE.set_href(href2);
                    page_init("body_body", false);
                    if (PUSH_STATE) {
                        id = jQuery(elem).attr("id");
                        if (!id) {
                            id = "menu_id_" + MENU_ID;
                            MENU_ID = MENU_ID + 1;
                            jQuery(elem).attr("id", id);
                        }
                        history_push_state(title, href, ρσ_list_decorate([ data, id ]));
                    }
                }
                if (WAIT_ICON) {
                    WAIT_ICON.stop();
                    WAIT_ICON = null;
                }
                if (WAIT_ICON2) {
                    jQuery("#loading-indicator").hide();
                    WAIT_ICON2 = false;
                }
            };
            Object.defineProperties(_on_new_win, {
                __argnames__ : {value: ["data"]}
            });

            if ((APPLICATION_TEMPLATE === "standard" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "standard")) && classname && ρσ_in("btn", classname)) {
                jQuery("a.menu-href").removeClass("btn-warning");
                jQuery(elem).addClass("btn-warning");
            }
            if (WAIT_ICON) {
                WAIT_ICON.start();
            } else {
                WAIT_ICON2 = true;
                jQuery("#loading-indicator").show();
            }
            ajax_get(href2, _on_new_win);
            jQuery(".navbar-ex1-collapse").collapse("hide");
        }
        return false;
    }
};
Object.defineProperties(_on_menu_href, {
    __defaults__ : {value: {title:null}},
    __handles_kwarg_interpolation__ : {value: true},
    __argnames__ : {value: ["elem", "title"]}
});

function _on_error(request, settings) {
    var start, end;
    if (WAIT_ICON) {
        WAIT_ICON.stop();
        WAIT_ICON = null;
    }
    if (WAIT_ICON2) {
        jQuery("#loading-indicator").hide();
        WAIT_ICON2 = false;
    }
    if ((settings.status === 200 || typeof settings.status === "object" && ρσ_equals(settings.status, 200))) {
        return;
    }
    if (settings.responseText) {
        start = settings.responseText.indexOf("<body>");
        end = settings.responseText.lastIndexOf("</body>");
        if (start > 0 && end > 0) {
            jQuery("#dialog-data-error").html(settings.responseText.substring(start + 6, end - 1));
            jQuery("#dialog-form-error").modal();
        } else {
            jQuery("#dialog-data-error").html(settings.responseText);
            jQuery("#dialog-form-error").modal();
        }
    }
};
Object.defineProperties(_on_error, {
    __argnames__ : {value: ["request", "settings"]}
});

function jquery_ready() {
    var txt, txt2, menu;
    jQuery(document).ajaxError(_on_error);
    jQuery("div.dialog-form").on("hide.bs.modal", (function() {
        var ρσ_anonfunc = function (e) {
            IS_POPUP = false;
            jQuery(this).find("div.dialog-data").html("<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
        };
        Object.defineProperties(ρσ_anonfunc, {
            __argnames__ : {value: ["e"]}
        });
        return ρσ_anonfunc;
    })());
    jQuery(".navbar-ex1-collapse").on("hidden.bs.collapse", function () {
        console.log("collapsed");
    });
    if ((APPLICATION_TEMPLATE === "traditional" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "traditional"))) {
        glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
        page_init("body_body");
    } else {
        if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern"))) {
            txt = jQuery(".page").text();
            txt2 = jQuery.trim(txt);
            if (txt2) {
                txt = jQuery.trim(jQuery(".page")[0].outerHTML);
                jQuery(".page").remove();
                menu = get_menu();
                menu.new_page(jQuery("title").text(), txt, window.location.href, RIOT_INIT);
            }
        } else {
            glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
            page_init("body_body");
        }
    }
};

window.addEventListener("popstate", (function() {
    var ρσ_anonfunc = function (e) {
        var menu, x;
        if (e.state) {
            PUSH_STATE = false;
            if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern"))) {
                menu = get_menu().activate(e.state, false);
            } else {
                x = e.state;
                jQuery("#body_body").html(LZString.decompress(x[0]));
                glob.ACTIVE_PAGE = new Page(0, jQuery("#body_body"));
                glob.ACTIVE_PAGE.set_href(document.location);
                if ((APPLICATION_TEMPLATE === "standard" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "standard"))) {
                    jQuery("a.menu-href").removeClass("btn-warning");
                    jQuery("#" + x[1]).addClass("btn-warning");
                }
            }
            PUSH_STATE = true;
        } else {
            if ((APPLICATION_TEMPLATE === "modern" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "modern"))) {
            } else {
                jQuery("#body_body").html("");
                glob.ACTIVE_PAGE = null;
                if ((APPLICATION_TEMPLATE === "standard" || typeof APPLICATION_TEMPLATE === "object" && ρσ_equals(APPLICATION_TEMPLATE, "standard"))) {
                    jQuery("a.menu-href").removeClass("btn-warning");
                }
            }
        }
    };
    Object.defineProperties(ρσ_anonfunc, {
        __argnames__ : {value: ["e"]}
    });
    return ρσ_anonfunc;
})(), false);
function history_push_state() {
    var title = ( 0 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[0];
    var url = ( 1 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true) ? undefined : arguments[1];
    var data = (arguments[2] === undefined || ( 2 === arguments.length-1 && arguments[arguments.length-1] !== null && typeof arguments[arguments.length-1] === "object" && arguments[arguments.length-1] [ρσ_kwargs_symbol] === true)) ? history_push_state.__defaults__.data : arguments[2];
    var ρσ_kwargs_obj = arguments[arguments.length-1];
    if (ρσ_kwargs_obj === null || typeof ρσ_kwargs_obj !== "object" || ρσ_kwargs_obj [ρσ_kwargs_symbol] !== true) ρσ_kwargs_obj = {};
    if (Object.prototype.hasOwnProperty.call(ρσ_kwargs_obj, "data")){
        data = ρσ_kwargs_obj.data;
    }
    var url2, data2;
    url2 = url.split("?")[0];
    if (data) {
        data2 = ρσ_list_decorate([ LZString.compress(data[0]), data[1] ]);
    } else {
        data2 = title;
    }
    window.history.pushState(data2, title, url2);
};
Object.defineProperties(history_push_state, {
    __defaults__ : {value: {data:null}},
    __handles_kwarg_interpolation__ : {value: true},
    __argnames__ : {value: ["title", "url", "data"]}
});
