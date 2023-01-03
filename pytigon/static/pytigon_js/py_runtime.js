var _pyfunc_abs = Math.abs;
var _pyfunc_all = function (x) { // nargs: 1
    for (var i=0; i<x.length; i++) {
        if (!_pyfunc_truthy(x[i])){return false;}
    } return true;
};
var _pyfunc_any = function (x) { // nargs: 1
    for (var i=0; i<x.length; i++) {
        if (_pyfunc_truthy(x[i])){return true;}
    } return false;
};
var _pyfunc_bool = function (x) { // nargs: 1
    return Boolean(_pyfunc_truthy(x));
};
var _pyfunc_create_dict = function () {
    var d = {};
    for (var i=0; i<arguments.length; i+=2) { d[arguments[i]] = arguments[i+1]; }
    return d;
};
var _pyfunc_delattr = function (ob, name) {  // nargs: 2
    delete ob[name];
};
var _pyfunc_dict = function (x) {
    var t, i, keys, r={};
    if (Array.isArray(x)) {
        for (i=0; i<x.length; i++) {
            t=x[i]; r[t[0]] = t[1];
        }
    } else {
        keys = Object.keys(x);
        for (i=0; i<keys.length; i++) {
            t=keys[i]; r[t] = x[t];
        }
    }
    return r;
};
var _pyfunc_divmod = function (x, y) { // nargs: 2
    var m = x % y; return [(x-m)/y, m];
};
var _pyfunc_enumerate = function (iter) { // nargs: 1
    var i, res=[];
    if ((typeof iter==="object") && (!Array.isArray(iter))) {iter = Object.keys(iter);}
    for (i=0; i<iter.length; i++) {res.push([i, iter[i]]);}
    return res;
};
var _pyfunc_filter = function (func, iter) { // nargs: 2
    if (typeof func === "undefined" || func === null) {func = function(x) {return x;}}
    if ((typeof iter==="object") && (!Array.isArray(iter))) {iter = Object.keys(iter);}
    return iter.filter(func);
};
var _pyfunc_float = Number;
var _pyfunc_format = function (v, fmt) {  // nargs: 2
    fmt = fmt.toLowerCase();
    var s = String(v);
    if (fmt.indexOf('!r') >= 0) {
        try { s = JSON.stringify(v); } catch (e) { s = undefined; }
        if (typeof s === 'undefined') { s = v._IS_COMPONENT ? v.id : String(v); }
    }
    var fmt_type = '';
    if (fmt.slice(-1) == 'i' || fmt.slice(-1) == 'f' ||
        fmt.slice(-1) == 'e' || fmt.slice(-1) == 'g') {
            fmt_type = fmt[fmt.length-1]; fmt = fmt.slice(0, fmt.length-1);
    }
    var i0 = fmt.indexOf(':');
    var i1 = fmt.indexOf('.');
    var spec1 = '', spec2 = '';  // before and after dot
    if (i0 >= 0) {
        if (i1 > i0) { spec1 = fmt.slice(i0+1, i1); spec2 = fmt.slice(i1+1); }
        else { spec1 = fmt.slice(i0+1); }
    }
    // Format numbers
    if (fmt_type == '') {
    } else if (fmt_type == 'i') { // integer formatting, for %i
        s = parseInt(v).toFixed(0);
    } else if (fmt_type == 'f') {  // float formatting
        v = parseFloat(v);
        var decimals = spec2 ? Number(spec2) : 6;
        s = v.toFixed(decimals);
    } else if (fmt_type == 'e') {  // exp formatting
        v = parseFloat(v);
        var precision = (spec2 ? Number(spec2) : 6) || 1;
        s = v.toExponential(precision);
    } else if (fmt_type == 'g') {  // "general" formatting
        v = parseFloat(v);
        var precision = (spec2 ? Number(spec2) : 6) || 1;
        // Exp or decimal?
        s = v.toExponential(precision-1);
        var s1 = s.slice(0, s.indexOf('e')), s2 = s.slice(s.indexOf('e'));
        if (s2.length == 3) { s2 = 'e' + s2[1] + '0' + s2[2]; }
        var exp = Number(s2.slice(1));
        if (exp >= -4 && exp < precision) { s1=v.toPrecision(precision); s2=''; }
        // Skip trailing zeros and dot
        var j = s1.length-1;
        while (j>0 && s1[j] == '0') { j-=1; }
        s1 = s1.slice(0, j+1);
        if (s1.slice(-1) == '.') { s1 = s1.slice(0, s1.length-1); }
        s = s1 + s2;
    }
    // prefix/padding
    var prefix = '';
    if (spec1) {
        if (spec1[0] == '+' && v > 0) { prefix = '+'; spec1 = spec1.slice(1); }
        else if (spec1[0] == ' ' && v > 0) { prefix = ' '; spec1 = spec1.slice(1); }
    }
    if (spec1 && spec1[0] == '0') {
        var padding = Number(spec1.slice(1)) - (s.length + prefix.length);
        s = '0'.repeat(Math.max(0, padding)) + s;
    }
    return prefix + s;
};
var _pyfunc_getattr = function (ob, name, deflt) { // nargs: 2 3
    var has_attr = ob !== undefined && ob !== null && ob[name] !== undefined;
    if (has_attr) {return ob[name];}
    else if (arguments.length == 3) {return deflt;}
    else {var e = Error(name); e.name='AttributeError'; throw e;}
};
var _pyfunc_hasattr = function (ob, name) { // nargs: 2
    return (ob !== undefined) && (ob !== null) && (ob[name] !== undefined);
};
var _pyfunc_int = function (x, base) { // nargs: 1 2
    if(base !== undefined) return parseInt(x, base);
    return x<0 ? Math.ceil(x): Math.floor(x);
};
var _pyfunc_list = function (x) {
    var r=[];
    if (typeof x==="object" && !Array.isArray(x)) {x = Object.keys(x)}
    for (var i=0; i<x.length; i++) {
        r.push(x[i]);
    }
    return r;
};
var _pyfunc_map = function (func, iter) { // nargs: 2
    if (typeof func === "undefined" || func === null) {func = function(x) {return x;}}
    if ((typeof iter==="object") && (!Array.isArray(iter))) {iter = Object.keys(iter);}
    return iter.map(func);
};
var _pyfunc_merge_dicts = function () {
    var res = {};
    for (var i=0; i<arguments.length; i++) {
        var d = arguments[i];
        var key, keys = Object.keys(d);
        for (var j=0; j<keys.length; j++) { key = keys[j]; res[key] = d[key]; }
    }
    return res;
};
var _pyfunc_op_add = function (a, b) { // nargs: 2
    if (Array.isArray(a) && Array.isArray(b)) {
        return a.concat(b);
    } return a + b;
};
var _pyfunc_op_contains = function op_contains (a, b) { // nargs: 2
    if (b == null) {
    } else if (Array.isArray(b)) {
        for (var i=0; i<b.length; i++) {if (_pyfunc_op_equals(a, b[i]))
                                           return true;}
        return false;
    } else if (b.constructor === Object) {
        for (var k in b) {if (a == k) return true;}
        return false;
    } else if (b.constructor == String) {
        return b.indexOf(a) >= 0;
    } var e = Error('Not a container: ' + b); e.name='TypeError'; throw e;
};
var _pyfunc_op_equals = function op_equals (a, b) { // nargs: 2
    var a_type = typeof a;
    // If a (or b actually) is of type string, number or boolean, we don't need
    // to do all the other type checking below.
    if (a_type === "string" || a_type === "boolean" || a_type === "number") {
        return a == b;
    }

    if (a == null || b == null) {
    } else if (Array.isArray(a) && Array.isArray(b)) {
        var i = 0, iseq = a.length == b.length;
        while (iseq && i < a.length) {iseq = op_equals(a[i], b[i]); i+=1;}
        return iseq;
    } else if (a.constructor === Object && b.constructor === Object) {
        var akeys = Object.keys(a), bkeys = Object.keys(b);
        akeys.sort(); bkeys.sort();
        var i=0, k, iseq = op_equals(akeys, bkeys);
        while (iseq && i < akeys.length)
            {k=akeys[i]; iseq = op_equals(a[k], b[k]); i+=1;}
        return iseq;
    } return a == b;
};
var _pyfunc_op_error = function (etype, msg) { // nargs: 2
    var e = new Error(etype + ': ' + msg);
    e.name = etype
    return e;
};
var _pyfunc_op_instantiate = function (ob, args) { // nargs: 2
    if ((typeof ob === "undefined") ||
            (typeof window !== "undefined" && window === ob) ||
            (typeof global !== "undefined" && global === ob))
            {throw "Class constructor is called as a function.";}
    for (var name in ob) {
        if (Object[name] === undefined &&
            typeof ob[name] === 'function' && !ob[name].nobind) {
            ob[name] = ob[name].bind(ob);
            ob[name].__name__ = name;
        }
    }
    if (ob.__init__) {
        ob.__init__.apply(ob, args);
    }
};
var _pyfunc_op_mult = function (a, b) { // nargs: 2
    if ((typeof a === 'number') + (typeof b === 'number') === 1) {
        if (a.constructor === String) return _pymeth_repeat.call(a, b);
        if (b.constructor === String) return _pymeth_repeat.call(b, a);
        if (Array.isArray(b)) {var t=a; a=b; b=t;}
        if (Array.isArray(a)) {
            var res = []; for (var i=0; i<b; i++) res = res.concat(a);
            return res;
        }
    } return a * b;
};
var _pyfunc_op_parse_kwargs = function (arg_names, arg_values, kwargs, strict) { // nargs: 3
    for (var i=0; i<arg_values.length; i++) {
        var name = arg_names[i];
        if (kwargs[name] !== undefined) {
            arg_values[i] = kwargs[name];
            delete kwargs[name];
        }
    }
    if (strict && Object.keys(kwargs).length > 0) {
        throw _pyfunc_op_error('TypeError',
            'Function ' + strict + ' does not accept **kwargs.');
    }
    return kwargs;
};
var _pyfunc_perf_counter = function() { // nargs: 0
    if (typeof(process) === "undefined"){return performance.now()*1e-3;}
    else {var t = process.hrtime(); return t[0] + t[1]*1e-9;}
};
var _pyfunc_pow = Math.pow;
var _pyfunc_range = function (start, end, step) {
    var i, res = [];
    var val = start;
    var n = (end - start) / step;
    for (i=0; i<n; i++) {
        res.push(val);
        val += step;
    }
    return res;
};
var _pyfunc_repr = function (x) { // nargs: 1
    var res; try { res = JSON.stringify(x); } catch (e) { res = undefined; }
    if (typeof res === 'undefined') { res = x._IS_COMPONENT ? x.id : String(x); }
    return res;
};
var _pyfunc_reversed = function (iter) { // nargs: 1
    if ((typeof iter==="object") && (!Array.isArray(iter))) {iter = Object.keys(iter);}
    return iter.slice().reverse();
};
var _pyfunc_round = Math.round;
var _pyfunc_setattr = function (ob, name, value) {  // nargs: 3
    ob[name] = value;
};
var _pyfunc_sorted = function (iter, key, reverse) { // nargs: 1 2 3
    if ((typeof iter==="object") && (!Array.isArray(iter))) {iter = Object.keys(iter);}
    var comp = function (a, b) {a = key(a); b = key(b);
        if (a<b) {return -1;} if (a>b) {return 1;} return 0;};
    comp = Boolean(key) ? comp : undefined;
    iter = iter.slice().sort(comp);
    if (reverse) iter.reverse();
    return iter;
};
var _pyfunc_str = String;
var _pyfunc_sum = function (x) {  // nargs: 1
    return x.reduce(function(a, b) {return a + b;});
};
var _pyfunc_time = function () {return Date.now() / 1000;};
var _pyfunc_truthy = function (v) {
    if (v === null || typeof v !== "object") {return v;}
    else if (v.length !== undefined) {return v.length ? v : false;}
    else if (v.byteLength !== undefined) {return v.byteLength ? v : false;}
    else if (v.constructor !== Object) {return true;}
    else {return Object.getOwnPropertyNames(v).length ? v : false;}
};
var _pyfunc_zip = function () { // nargs: 2 3 4 5 6 7 8 9
    var i, j, tup, arg, args = [], res = [], len = 1e20;
    for (i=0; i<arguments.length; i++) {
        arg = arguments[i];
        if ((typeof arg==="object") && (!Array.isArray(arg))) {arg = Object.keys(arg);}
        args.push(arg);
        len = Math.min(len, arg.length);
    }
    for (j=0; j<len; j++) {
        tup = []
        for (i=0; i<args.length; i++) {tup.push(args[i][j]);}
        res.push(tup);
    }
    return res;
};
var _pymeth_append = function (x) { // nargs: 1
    if (!Array.isArray(this)) return this.append.apply(this, arguments);
    this.push(x);
};
var _pymeth_capitalize = function () { // nargs: 0
    if (this.constructor !== String) return this.capitalize.apply(this, arguments);
    return this.slice(0, 1).toUpperCase() + this.slice(1).toLowerCase();
};
var _pymeth_casefold = function () { // nargs: 0
    if (this.constructor !== String) return this.casefold.apply(this, arguments);
    return this.toLowerCase();
};
var _pymeth_center = function (w, fill) { // nargs: 1 2
    if (this.constructor !== String) return this.center.apply(this, arguments);
    fill = (fill === undefined) ? ' ' : fill;
    var tofill = Math.max(0, w - this.length);
    var left = Math.ceil(tofill / 2);
    var right = tofill - left;
    return _pymeth_repeat.call(fill, left) + this + _pymeth_repeat.call(fill, right);
};
var _pymeth_clear = function () { // nargs: 0
    if (Array.isArray(this)) {
        this.splice(0, this.length);
    } else if (this.constructor === Object) {
        var keys = Object.keys(this);
        for (var i=0; i<keys.length; i++) delete this[keys[i]];
    } else return this.clear.apply(this, arguments);
};
var _pymeth_copy = function () { // nargs: 0
    if (Array.isArray(this)) {
        return this.slice(0);
    } else if (this.constructor === Object) {
        var key, keys = Object.keys(this), res = {};
        for (var i=0; i<keys.length; i++) {key = keys[i]; res[key] = this[key];}
        return res;
    } else return this.copy.apply(this, arguments);
};
var _pymeth_count = function (x, start, stop) { // nargs: 1 2 3
    start = (start === undefined) ? 0 : start;
    stop = (stop === undefined) ? this.length : stop;
    start = Math.max(0, ((start < 0) ? this.length + start : start));
    stop = Math.min(this.length, ((stop < 0) ? this.length + stop : stop));
    if (Array.isArray(this)) {
        var count = 0;
        for (var i=0; i<this.length; i++) {
            if (_pyfunc_op_equals(this[i], x)) {count+=1;}
        } return count;
    } else if (this.constructor == String) {
        var count = 0, i = start;
        while (i >= 0 && i < stop) {
            i = this.indexOf(x, i);
            if (i < 0) break;
            count += 1;
            i += Math.max(1, x.length);
        } return count;
    } else return this.count.apply(this, arguments);
};
var _pymeth_endswith = function (x) { // nargs: 1
    if (this.constructor !== String) return this.endswith.apply(this, arguments);
    var last_index = this.lastIndexOf(x);
    return last_index == this.length - x.length && last_index >= 0;
};
var _pymeth_expandtabs = function (tabsize) { // nargs: 0 1
    if (this.constructor !== String) return this.expandtabs.apply(this, arguments);
    tabsize = (tabsize === undefined) ? 8 : tabsize;
    return this.replace(/\t/g, _pymeth_repeat.call(' ', tabsize));
};
var _pymeth_extend = function (x) { // nargs: 1
    if (!Array.isArray(this)) return this.extend.apply(this, arguments);
    this.push.apply(this, x);
};
var _pymeth_find = function (x, start, stop) { // nargs: 1 2 3
    if (this.constructor !== String) return this.find.apply(this, arguments);
    start = (start === undefined) ? 0 : start;
    stop = (stop === undefined) ? this.length : stop;
    start = Math.max(0, ((start < 0) ? this.length + start : start));
    stop = Math.min(this.length, ((stop < 0) ? this.length + stop : stop));
    var i = this.slice(start, stop).indexOf(x);
    if (i >= 0) return i + start;
    return -1;
};
var _pymeth_format = function () {
    if (this.constructor !== String) return this.format.apply(this, arguments);
    var parts = [], i = 0, i1, i2;
    var itemnr = -1;
    while (i < this.length) {
        // find opening
        i1 = this.indexOf('{', i);
        if (i1 < 0 || i1 == this.length-1) { break; }
        if (this[i1+1] == '{') {parts.push(this.slice(i, i1+1)); i = i1 + 2; continue;}
        // find closing
        i2 = this.indexOf('}', i1);
        if (i2 < 0) { break; }
        // parse
        itemnr += 1;
        var fmt = this.slice(i1+1, i2);
        var index = fmt.split(':')[0].split('!')[0];
        index = index? Number(index) : itemnr
        var s = _pyfunc_format(arguments[index], fmt);
        parts.push(this.slice(i, i1), s);
        i = i2 + 1;
    }
    parts.push(this.slice(i));
    return parts.join('');
};
var _pymeth_get = function (key, d) { // nargs: 1 2
    if (this.constructor !== Object) return this.get.apply(this, arguments);
    if (this[key] !== undefined) {return this[key];}
    else if (d !== undefined) {return d;}
    else {return null;}
};
var _pymeth_index = function (x, start, stop) { // nargs: 1 2 3
    start = (start === undefined) ? 0 : start;
    stop = (stop === undefined) ? this.length : stop;
    start = Math.max(0, ((start < 0) ? this.length + start : start));
    stop = Math.min(this.length, ((stop < 0) ? this.length + stop : stop));
    if (Array.isArray(this)) {
        for (var i=start; i<stop; i++) {
            if (_pyfunc_op_equals(this[i], x)) {return i;} // indexOf cant
        }
    } else if (this.constructor === String) {
        var i = this.slice(start, stop).indexOf(x);
        if (i >= 0) return i + start;
    } else return this.index.apply(this, arguments);
    var e = Error(x); e.name='ValueError'; throw e;
};
var _pymeth_insert = function (i, x) { // nargs: 2
    if (!Array.isArray(this)) return this.insert.apply(this, arguments);
    i = (i < 0) ? this.length + i : i;
    this.splice(i, 0, x);
};
var _pymeth_isalnum = function () { // nargs: 0
    if (this.constructor !== String) return this.isalnum.apply(this, arguments);
    return Boolean(/^[A-Za-z0-9]+$/.test(this));
};
var _pymeth_isalpha = function () { // nargs: 0
    if (this.constructor !== String) return this.isalpha.apply(this, arguments);
    return Boolean(/^[A-Za-z]+$/.test(this));
};
var _pymeth_isdecimal = function () { // nargs: 0
    if (this.constructor !== String) return this.isdecimal.apply(this, arguments);
    return Boolean(/^[0-9]+$/.test(this));
};
var _pymeth_isdigit = function () { // nargs: 0
    if (this.constructor !== String) return this.isdigit.apply(this, arguments);
    return Boolean(/^[0-9]+$/.test(this));
};
var _pymeth_isidentifier = function () { // nargs: 0
    if (this.constructor !== String) return this.isidentifier.apply(this, arguments);
    return Boolean(/^[A-Za-z_][A-Za-z0-9_]*$/.test(this));
};
var _pymeth_islower = function () { // nargs: 0
    if (this.constructor !== String) return this.islower.apply(this, arguments);
    var low = this.toLowerCase(), high = this.toUpperCase();
    return low != high && low == this;
};
var _pymeth_isnumeric = function () { // nargs: 0
    if (this.constructor !== String) return this.isnumeric.apply(this, arguments);
    return Boolean(/^[0-9]+$/.test(this));
};
var _pymeth_isspace = function () { // nargs: 0
    if (this.constructor !== String) return this.isspace.apply(this, arguments);
    return Boolean(/^\s+$/.test(this));
};
var _pymeth_istitle = function () { // nargs: 0
    if (this.constructor !== String) return this.istitle.apply(this, arguments);
    var low = this.toLowerCase(), title = _pymeth_title.call(this);
    return low != title && title == this;
};
var _pymeth_isupper = function () { // nargs: 0
    if (this.constructor !== String) return this.isupper.apply(this, arguments);
    var low = this.toLowerCase(), high = this.toUpperCase();
    return low != high && high == this;
};
var _pymeth_items = function () { // nargs: 0
    if (this.constructor !== Object) return this.items.apply(this, arguments);
    var key, keys = Object.keys(this), res = []
    for (var i=0; i<keys.length; i++) {key = keys[i]; res.push([key, this[key]]);}
    return res;
};
var _pymeth_join = function (x) { // nargs: 1
    if (this.constructor !== String) return this.join.apply(this, arguments);
    return x.join(this);  // call join on the list instead of the string.
};
var _pymeth_keys = function () { // nargs: 0
    if (typeof this['keys'] === 'function') return this.keys.apply(this, arguments);
    return Object.keys(this);
};
var _pymeth_ljust = function (w, fill) { // nargs: 1 2
    if (this.constructor !== String) return this.ljust.apply(this, arguments);
    fill = (fill === undefined) ? ' ' : fill;
    var tofill = Math.max(0, w - this.length);
    return this + _pymeth_repeat.call(fill, tofill);
};
var _pymeth_lower = function () { // nargs: 0
    if (this.constructor !== String) return this.lower.apply(this, arguments);
    return this.toLowerCase();
};
var _pymeth_lstrip = function (chars) { // nargs: 0 1
    if (this.constructor !== String) return this.lstrip.apply(this, arguments);
    chars = (chars === undefined) ? ' \t\r\n' : chars;
    for (var i=0; i<this.length; i++) {
        if (chars.indexOf(this[i]) < 0) return this.slice(i);
    } return '';
};
var _pymeth_partition = function (sep) { // nargs: 1
    if (this.constructor !== String) return this.partition.apply(this, arguments);
    if (sep === '') {var e = Error('empty sep'); e.name='ValueError'; throw e;}
    var i1 = this.indexOf(sep);
    if (i1 < 0) return [this.slice(0), '', '']
    var i2 = i1 + sep.length;
    return [this.slice(0, i1), this.slice(i1, i2), this.slice(i2)];
};
var _pymeth_pop = function (i, d) { // nargs: 1 2
    if (Array.isArray(this)) {
        i = (i === undefined) ? -1 : i;
        i = (i < 0) ? (this.length + i) : i;
        var popped = this.splice(i, 1);
        if (popped.length)  return popped[0];
        var e = Error(i); e.name='IndexError'; throw e;
    } else if (this.constructor === Object) {
        var res = this[i]
        if (res !== undefined) {delete this[i]; return res;}
        else if (d !== undefined) return d;
        var e = Error(i); e.name='KeyError'; throw e;
    } else return this.pop.apply(this, arguments);
};
var _pymeth_popitem = function () { // nargs: 0
    if (this.constructor !== Object) return this.popitem.apply(this, arguments);
    var keys, key, val;
    keys = Object.keys(this);
    if (keys.length == 0) {var e = Error(); e.name='KeyError'; throw e;}
    key = keys[0]; val = this[key]; delete this[key];
    return [key, val];
};
var _pymeth_remove = function (x) { // nargs: 1
    if (!Array.isArray(this)) return this.remove.apply(this, arguments);
    for (var i=0; i<this.length; i++) {
        if (_pyfunc_op_equals(this[i], x)) {this.splice(i, 1); return;}
    }
    var e = Error(x); e.name='ValueError'; throw e;
};
var _pymeth_repeat = function(count) { // nargs: 0
    if (this.repeat) return this.repeat(count);
    if (count < 1) return '';
    var result = '', pattern = this.valueOf();
    while (count > 1) {
        if (count & 1) result += pattern;
        count >>= 1, pattern += pattern;
    }
    return result + pattern;
};
var _pymeth_replace = function (s1, s2, count) {  // nargs: 2 3
    if (this.constructor !== String) return this.replace.apply(this, arguments);
    var i = 0, i2, parts = [];
    count = (count === undefined) ? 1e20 : count;
    while (count > 0) {
        i2 = this.indexOf(s1, i);
        if (i2 >= 0) {
            parts.push(this.slice(i, i2));
            parts.push(s2);
            i = i2 + s1.length;
            count -= 1;
        } else break;
    }
    parts.push(this.slice(i));
    return parts.join('');
};
var _pymeth_reverse = function () { // nargs: 0
    this.reverse();
};
var _pymeth_rfind = function (x, start, stop) { // nargs: 1 2 3
    if (this.constructor !== String) return this.rfind.apply(this, arguments);
    start = (start === undefined) ? 0 : start;
    stop = (stop === undefined) ? this.length : stop;
    start = Math.max(0, ((start < 0) ? this.length + start : start));
    stop = Math.min(this.length, ((stop < 0) ? this.length + stop : stop));
    var i = this.slice(start, stop).lastIndexOf(x);
    if (i >= 0) return i + start;
    return -1;
};
var _pymeth_rindex = function (x, start, stop) {  // nargs: 1 2 3
    if (this.constructor !== String) return this.rindex.apply(this, arguments);
    var i = _pymeth_rfind.call(this, x, start, stop);
    if (i >= 0) return i;
    var e = Error(x); e.name='ValueError'; throw e;
};
var _pymeth_rjust = function (w, fill) { // nargs: 1 2
    if (this.constructor !== String) return this.rjust.apply(this, arguments);
    fill = (fill === undefined) ? ' ' : fill;
    var tofill = Math.max(0, w - this.length);
    return _pymeth_repeat.call(fill, tofill) + this;
};
var _pymeth_rpartition = function (sep) { // nargs: 1
    if (this.constructor !== String) return this.rpartition.apply(this, arguments);
    if (sep === '') {var e = Error('empty sep'); e.name='ValueError'; throw e;}
    var i1 = this.lastIndexOf(sep);
    if (i1 < 0) return ['', '', this.slice(0)]
    var i2 = i1 + sep.length;
    return [this.slice(0, i1), this.slice(i1, i2), this.slice(i2)];
};
var _pymeth_rsplit = function (sep, count) { // nargs: 1 2
    if (this.constructor !== String) return this.rsplit.apply(this, arguments);
    sep = (sep === undefined) ? /\s/ : sep;
    count = Math.max(0, (count === undefined) ? 1e20 : count);
    var parts = this.split(sep);
    var limit = Math.max(0, parts.length-count);
    var res = parts.slice(limit);
    if (count < parts.length) res.splice(0, 0, parts.slice(0, limit).join(sep));
    return res;
};
var _pymeth_rstrip = function (chars) { // nargs: 0 1
    if (this.constructor !== String) return this.rstrip.apply(this, arguments);
    chars = (chars === undefined) ? ' \t\r\n' : chars;
    for (var i=this.length-1; i>=0; i--) {
        if (chars.indexOf(this[i]) < 0) return this.slice(0, i+1);
    } return '';
};
var _pymeth_setdefault = function (key, d) { // nargs: 1 2
    if (this.constructor !== Object) return this.setdefault.apply(this, arguments);
    if (this[key] !== undefined) {return this[key];}
    else if (d !== undefined) { this[key] = d; return d;}
    else {return null;}
};
var _pymeth_sort = function (key, reverse) { // nargs: 0 1 2
    if (!Array.isArray(this)) return this.sort.apply(this, arguments);
    var comp = function (a, b) {a = key(a); b = key(b);
        if (a<b) {return -1;} if (a>b) {return 1;} return 0;};
    comp = Boolean(key) ? comp : undefined;
    this.sort(comp);
    if (reverse) this.reverse();
};
var _pymeth_split = function (sep, count) { // nargs: 0, 1 2
    if (this.constructor !== String) return this.split.apply(this, arguments);
    if (sep === '') {var e = Error('empty sep'); e.name='ValueError'; throw e;}
    sep = (sep === undefined) ? /\s/ : sep;
    if (count === undefined) { return this.split(sep); }
    var res = [], i = 0, index1 = 0, index2 = 0;
    while (i < count && index1 < this.length) {
        index2 = this.indexOf(sep, index1);
        if (index2 < 0) { break; }
        res.push(this.slice(index1, index2));
        index1 = index2 + sep.length || 1;
        i += 1;
    }
    res.push(this.slice(index1));
    return res;
};
var _pymeth_splitlines = function (keepends) { // nargs: 0 1
    if (this.constructor !== String) return this.splitlines.apply(this, arguments);
    keepends = keepends ? 1 : 0
    var finder = /\r\n|\r|\n/g;
    var i = 0, i2, isrn, parts = [];
    while (finder.exec(this) !== null) {
        i2 = finder.lastIndex -1;
        isrn = i2 > 0 && this[i2-1] == '\r' && this[i2] == '\n';
        if (keepends) parts.push(this.slice(i, finder.lastIndex));
        else parts.push(this.slice(i, i2 - isrn));
        i = finder.lastIndex;
    }
    if (i < this.length) parts.push(this.slice(i));
    else if (!parts.length) parts.push('');
    return parts;
};
var _pymeth_startswith = function (x) { // nargs: 1
    if (this.constructor !== String) return this.startswith.apply(this, arguments);
    return this.indexOf(x) == 0;
};
var _pymeth_strip = function (chars) { // nargs: 0 1
    if (this.constructor !== String) return this.strip.apply(this, arguments);
    chars = (chars === undefined) ? ' \t\r\n' : chars;
    var i, s1 = this, s2 = '', s3 = '';
    for (i=0; i<s1.length; i++) {
        if (chars.indexOf(s1[i]) < 0) {s2 = s1.slice(i); break;}
    } for (i=s2.length-1; i>=0; i--) {
        if (chars.indexOf(s2[i]) < 0) {s3 = s2.slice(0, i+1); break;}
    } return s3;
};
var _pymeth_swapcase = function () { // nargs: 0
    if (this.constructor !== String) return this.swapcase.apply(this, arguments);
    var c, res = [];
    for (var i=0; i<this.length; i++) {
        c = this[i];
        if (c.toUpperCase() == c) res.push(c.toLowerCase());
        else res.push(c.toUpperCase());
    } return res.join('');
};
var _pymeth_title = function () { // nargs: 0
    if (this.constructor !== String) return this.title.apply(this, arguments);
    var i0, res = [], tester = /^[^A-Za-z]?[A-Za-z]$/;
    for (var i=0; i<this.length; i++) {
        i0 = Math.max(0, i-1);
        if (tester.test(this.slice(i0, i+1))) res.push(this[i].toUpperCase());
        else res.push(this[i].toLowerCase());
    } return res.join('');
};
var _pymeth_translate = function (table) { // nargs: 1
    if (this.constructor !== String) return this.translate.apply(this, arguments);
    var c, res = [];
    for (var i=0; i<this.length; i++) {
        c = table[this[i]];
        if (c === undefined) res.push(this[i]);
        else if (c !== null) res.push(c);
    } return res.join('');
};
var _pymeth_update = function (other) { // nargs: 1
    if (this.constructor !== Object) return this.update.apply(this, arguments);
    var key, keys = Object.keys(other);
    for (var i=0; i<keys.length; i++) {key = keys[i]; this[key] = other[key];}
    return null;
};
var _pymeth_upper = function () { // nargs: 0
    if (this.constructor !== String) return this.upper.apply(this, arguments);
    return this.toUpperCase();
};
var _pymeth_values = function () { // nargs: 0
    if (this.constructor !== Object) return this.values.apply(this, arguments);
    var key, keys = Object.keys(this), res = [];
    for (var i=0; i<keys.length; i++) {key = keys[i]; res.push(this[key]);}
    return res;
};
var _pymeth_zfill = function (width) { // nargs: 1
    if (this.constructor !== String) return this.zfill.apply(this, arguments);
    return _pymeth_rjust.call(this, width, '0');
};