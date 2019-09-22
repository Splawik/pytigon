"use strict";
// Transcrypt'ed from Python, 2019-05-14 23:06:49
function pytigon () {
    var __symbols__ = ['__py3.7__', '__esv5__'];
    var __all__ = {};
    var __world__ = __all__;
    var __nest__ = function (headObject, tailNames, value) {
        var current = headObject;
        if (tailNames != '') {
            var tailChain = tailNames.split ('.');
            var firstNewIndex = tailChain.length;
            for (var index = 0; index < tailChain.length; index++) {
                if (!current.hasOwnProperty (tailChain [index])) {
                    firstNewIndex = index;
                    break;
                }
                current = current [tailChain [index]];
            }
            for (var index = firstNewIndex; index < tailChain.length; index++) {
                current [tailChain [index]] = {};
                current = current [tailChain [index]];
            }
        }
        for (var attrib in value) {
            current [attrib] = value [attrib];
        }
    };
    __all__.__nest__ = __nest__;
    var __init__ = function (module) {
        if (!module.__inited__) {
            module.__all__.__init__ (module.__all__);
            module.__inited__ = true;
        }
        return module.__all__;
    };
    __all__.__init__ = __init__;
    var __get__ = function (self, func, quotedFuncName) {
        if (self) {
            if (self.hasOwnProperty ('__class__') || typeof self == 'string' || self instanceof String) {
                if (quotedFuncName) {
                    Object.defineProperty (self, quotedFuncName, {
                        value: function () {
                            var args = [] .slice.apply (arguments);
                            return func.apply (null, [self] .concat (args));
                        },
                        writable: true,
                        enumerable: true,
                        configurable: true
                    });
                }
                return function () {
                    var args = [] .slice.apply (arguments);
                    return func.apply (null, [self] .concat (args));
                };
            }
            else {
                return func;
            }
        }
        else {
            return func;
        }
    }
    __all__.__get__ = __get__;
    var __getcm__ = function (self, func, quotedFuncName) {
        if (self.hasOwnProperty ('__class__')) {
            return function () {
                var args = [] .slice.apply (arguments);
                return func.apply (null, [self.__class__] .concat (args));
            };
        }
        else {
            return function () {
                var args = [] .slice.apply (arguments);
                return func.apply (null, [self] .concat (args));
            };
        }
    }
    __all__.__getcm__ = __getcm__;
    var __getsm__ = function (self, func, quotedFuncName) {
        return func;
    }
    __all__.__getsm__ = __getsm__;
    var py_metatype = {
        __name__: 'type',
        __bases__: [],
        __new__: function (meta, name, bases, attribs) {
            var cls = function () {
                var args = [] .slice.apply (arguments);
                return cls.__new__ (args);
            };
            for (var index = bases.length - 1; index >= 0; index--) {
                var base = bases [index];
                for (var attrib in base) {
                    var descrip = Object.getOwnPropertyDescriptor (base, attrib);
                    Object.defineProperty (cls, attrib, descrip);
                }
            }
            cls.__metaclass__ = meta;
            cls.__name__ = name.startsWith ('py_') ? name.slice (3) : name;
            cls.__bases__ = bases;
            for (var attrib in attribs) {
                var descrip = Object.getOwnPropertyDescriptor (attribs, attrib);
                Object.defineProperty (cls, attrib, descrip);
            }
            return cls;
        }
    };
    py_metatype.__metaclass__ = py_metatype;
    __all__.py_metatype = py_metatype;
    var object = {
        __init__: function (self) {},
        __metaclass__: py_metatype,
        __name__: 'object',
        __bases__: [],
        __new__: function (args) {
            var instance = Object.create (this, {__class__: {value: this, enumerable: true}});
            this.__init__.apply (null, [instance] .concat (args));
            return instance;
        }
    };
    __all__.object = object;
    var __class__ = function (name, bases, attribs, meta) {
        if (meta === undefined) {
            meta = bases [0] .__metaclass__;
        }
        return meta.__new__ (meta, name, bases, attribs);
    }
    __all__.__class__ = __class__;
    var __pragma__ = function () {};
    __all__.__pragma__ = __pragma__;
	__nest__ (
		__all__,
		'org.transcrypt.__base__', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'org.transcrypt.__base__';
					var __Envir__ = __class__ ('__Envir__', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.interpreter_name = 'python';
							self.transpiler_name = 'transcrypt';
							self.transpiler_version = '3.6.101';
							self.target_subdir = '__javascript__';
						});}
					});
					var __envir__ = __Envir__ ();
					__pragma__ ('<all>')
						__all__.__Envir__ = __Envir__;
						__all__.__envir__ = __envir__;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'org.transcrypt.__standard__', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'org.transcrypt.__standard__';
					var Exception = __class__ ('Exception', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							var kwargs = dict ();
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
										}
									}
									delete kwargs.__kwargtrans__;
								}
								var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
							}
							else {
								var args = tuple ();
							}
							self.__args__ = args;
							try {
								self.stack = kwargs.error.stack;
							}
							catch (__except0__) {
								self.stack = 'No stack trace available';
							}
						});},
						__repr__: function () {
							var self = this;
							if (len (self.__args__)) {
								return '{}{}'.format (self.__class__.__name__, repr (tuple (self.__args__)));
							}
							else {
								return '{}()'.format (self.__class__.__name__);
							}
						},
						__str__: function () {
							var self = this;
							if (len (self.__args__) > 1) {
								return str (tuple (self.__args__));
							}
							else if (len (self.__args__)) {
								return str (self.__args__ [0]);
							}
							else {
								return '';
							}
						}
					});
					var IterableError = __class__ ('IterableError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, error) {
							Exception.__init__ (self, "Can't iterate over non-iterable", __kwargtrans__ ({error: error}));
						});}
					});
					var StopIteration = __class__ ('StopIteration', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, error) {
							Exception.__init__ (self, 'Iterator exhausted', __kwargtrans__ ({error: error}));
						});}
					});
					var ValueError = __class__ ('ValueError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var KeyError = __class__ ('KeyError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var AssertionError = __class__ ('AssertionError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							if (message) {
								Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
							}
							else {
								Exception.__init__ (self, __kwargtrans__ ({error: error}));
							}
						});}
					});
					var NotImplementedError = __class__ ('NotImplementedError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var IndexError = __class__ ('IndexError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var AttributeError = __class__ ('AttributeError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var py_TypeError = __class__ ('py_TypeError', [Exception], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, error) {
							Exception.__init__ (self, message, __kwargtrans__ ({error: error}));
						});}
					});
					var Warning = __class__ ('Warning', [Exception], {
						__module__: __name__,
					});
					var UserWarning = __class__ ('UserWarning', [Warning], {
						__module__: __name__,
					});
					var DeprecationWarning = __class__ ('DeprecationWarning', [Warning], {
						__module__: __name__,
					});
					var RuntimeWarning = __class__ ('RuntimeWarning', [Warning], {
						__module__: __name__,
					});
					var __sort__ = function (iterable, key, reverse) {
						if (typeof key == 'undefined' || (key != null && key .hasOwnProperty ("__kwargtrans__"))) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .hasOwnProperty ("__kwargtrans__"))) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'iterable': var iterable = __allkwargs0__ [__attrib0__]; break;
										case 'key': var key = __allkwargs0__ [__attrib0__]; break;
										case 'reverse': var reverse = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						if (key) {
							iterable.sort ((function __lambda__ (a, b) {
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
											switch (__attrib0__) {
												case 'a': var a = __allkwargs0__ [__attrib0__]; break;
												case 'b': var b = __allkwargs0__ [__attrib0__]; break;
											}
										}
									}
								}
								else {
								}
								return (key (a) > key (b) ? 1 : -(1));
							}));
						}
						else {
							iterable.sort ();
						}
						if (reverse) {
							iterable.reverse ();
						}
					};
					var sorted = function (iterable, key, reverse) {
						if (typeof key == 'undefined' || (key != null && key .hasOwnProperty ("__kwargtrans__"))) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .hasOwnProperty ("__kwargtrans__"))) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'iterable': var iterable = __allkwargs0__ [__attrib0__]; break;
										case 'key': var key = __allkwargs0__ [__attrib0__]; break;
										case 'reverse': var reverse = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						if (py_typeof (iterable) == dict) {
							var result = copy (iterable.py_keys ());
						}
						else {
							var result = copy (iterable);
						}
						__sort__ (result, key, reverse);
						return result;
					};
					var map = function (func, iterable) {
						return (function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var item = __iterable0__ [__index0__];
								__accu0__.append (func (item));
							}
							return __accu0__;
						}) ();
					};
					var filter = function (func, iterable) {
						if (func == null) {
							var func = bool;
						}
						return (function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var item = __iterable0__ [__index0__];
								if (func (item)) {
									__accu0__.append (item);
								}
							}
							return __accu0__;
						}) ();
					};
					var __Terminal__ = __class__ ('__Terminal__', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.buffer = '';
							try {
								self.element = document.getElementById ('__terminal__');
							}
							catch (__except0__) {
								self.element = null;
							}
							if (self.element) {
								self.element.style.overflowX = 'auto';
								self.element.style.boxSizing = 'border-box';
								self.element.style.padding = '5px';
								self.element.innerHTML = '_';
							}
						});},
						print: function () {
							var sep = ' ';
							var end = '\n';
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'sep': var sep = __allkwargs0__ [__attrib0__]; break;
											case 'end': var end = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
								var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
							}
							else {
								var args = tuple ();
							}
							var self = this;
							self.buffer = '{}{}{}'.format (self.buffer, sep.join ((function () {
								var __accu0__ = [];
								var __iterable0__ = args;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var arg = __iterable0__ [__index0__];
									__accu0__.append (str (arg));
								}
								return __accu0__;
							}) ()), end).__getslice__ (-(4096), null, 1);
							if (self.element) {
								self.element.innerHTML = self.buffer.py_replace ('\n', '<br>').py_replace (' ', '&nbsp');
								self.element.scrollTop = self.element.scrollHeight;
							}
							else {
								console.log (sep.join ((function () {
									var __accu0__ = [];
									var __iterable0__ = args;
									for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
										var arg = __iterable0__ [__index0__];
										__accu0__.append (str (arg));
									}
									return __accu0__;
								}) ()));
							}
						},
						input: function (question) {
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'question': var question = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
							}
							else {
							}
							var self = this;
							self.print ('{}'.format (question), __kwargtrans__ ({end: ''}));
							var answer = window.prompt ('\n'.join (self.buffer.py_split ('\n').__getslice__ (-(16), null, 1)));
							self.print (answer);
							return answer;
						}
					});
					var __terminal__ = __Terminal__ ();
					__pragma__ ('<all>')
						__all__.AssertionError = AssertionError;
						__all__.AttributeError = AttributeError;
						__all__.DeprecationWarning = DeprecationWarning;
						__all__.Exception = Exception;
						__all__.IndexError = IndexError;
						__all__.IterableError = IterableError;
						__all__.KeyError = KeyError;
						__all__.NotImplementedError = NotImplementedError;
						__all__.RuntimeWarning = RuntimeWarning;
						__all__.StopIteration = StopIteration;
						__all__.py_TypeError = py_TypeError;
						__all__.UserWarning = UserWarning;
						__all__.ValueError = ValueError;
						__all__.Warning = Warning;
						__all__.__Terminal__ = __Terminal__;
						__all__.__name__ = __name__;
						__all__.__sort__ = __sort__;
						__all__.__terminal__ = __terminal__;
						__all__.filter = filter;
						__all__.map = map;
						__all__.sorted = sorted;
					__pragma__ ('</all>')
				}
			}
		}
	);

    var __call__ = function (/* <callee>, <this>, <params>* */) {
        var args = [] .slice.apply (arguments);
        if (typeof args [0] == 'object' && '__call__' in args [0]) {
            return args [0] .__call__ .apply (args [1], args.slice (2));
        }
        else {
            return args [0] .apply (args [1], args.slice (2));
        }
    };
    __all__.__call__ = __call__;
    __nest__ (__all__, '', __init__ (__all__.org.transcrypt.__base__));
    var __envir__ = __all__.__envir__;
    __nest__ (__all__, '', __init__ (__all__.org.transcrypt.__standard__));
    var Exception = __all__.Exception;
    var IterableError = __all__.IterableError;
    var StopIteration = __all__.StopIteration;
    var ValueError = __all__.ValueError;
    var KeyError = __all__.KeyError;
    var AssertionError = __all__.AssertionError;
    var NotImplementedError = __all__.NotImplementedError;
    var IndexError = __all__.IndexError;
    var AttributeError = __all__.AttributeError;
    var py_TypeError = __all__.py_TypeError;
    var Warning = __all__.Warning;
    var UserWarning = __all__.UserWarning;
    var DeprecationWarning = __all__.DeprecationWarning;
    var RuntimeWarning = __all__.RuntimeWarning;
    var __sort__ = __all__.__sort__;
    var sorted = __all__.sorted;
    var map = __all__.map;
    var filter = __all__.filter;
    __all__.print = __all__.__terminal__.print;
    __all__.input = __all__.__terminal__.input;
    var __terminal__ = __all__.__terminal__;
    var print = __all__.print;
    var input = __all__.input;
    __envir__.executor_name = __envir__.transpiler_name;
    var __main__ = {__file__: ''};
    __all__.main = __main__;
    var __except__ = null;
    __all__.__except__ = __except__;
    var __kwargtrans__ = function (anObject) {
        anObject.__kwargtrans__ = null;
        anObject.constructor = Object;
        return anObject;
    }
    __all__.__kwargtrans__ = __kwargtrans__;
    var __globals__ = function (anObject) {
        if (isinstance (anObject, dict)) {
            return anObject;
        }
        else {
            return dict (anObject)
        }
    }
    __all__.__globals__ = __globals__
    var __super__ = function (aClass, methodName) {
        for (var index = 0; index < aClass.__bases__.length; index++) {
            var base = aClass.__bases__ [index];
            if (methodName in base) {
               return base [methodName];
            }
        }
        throw new Exception ('Superclass method not found');
    }
    __all__.__super__ = __super__
    var property = function (getter, setter) {
        if (!setter) {
            setter = function () {};
        }
        return {get: function () {return getter (this)}, set: function (value) {setter (this, value)}, enumerable: true};
    }
    __all__.property = property;
    var __setProperty__ = function (anObject, name, descriptor) {
        if (!anObject.hasOwnProperty (name)) {
            Object.defineProperty (anObject, name, descriptor);
        }
    }
    __all__.__setProperty__ = __setProperty__
    function assert (condition, message) {
        if (!condition) {
            throw AssertionError (message, new Error ());
        }
    }
    __all__.assert = assert;
    var __merge__ = function (object0, object1) {
        var result = {};
        for (var attrib in object0) {
            result [attrib] = object0 [attrib];
        }
        for (var attrib in object1) {
            result [attrib] = object1 [attrib];
        }
        return result;
    };
    __all__.__merge__ = __merge__;
    var dir = function (obj) {
        var aList = [];
        for (var aKey in obj) {
            aList.push (aKey.startsWith ('py_') ? aKey.slice (3) : aKey);
        }
        aList.sort ();
        return aList;
    };
    __all__.dir = dir;
    var setattr = function (obj, name, value) {
        obj [name] = value;
    };
    __all__.setattr = setattr;
    var getattr = function (obj, name) {
        return name in obj ? obj [name] : obj ['py_' + name];
    };
    __all__.getattr = getattr;
    var hasattr = function (obj, name) {
        try {
            return name in obj || 'py_' + name in obj;
        }
        catch (exception) {
            return false;
        }
    };
    __all__.hasattr = hasattr;
    var delattr = function (obj, name) {
        if (name in obj) {
            delete obj [name];
        }
        else {
            delete obj ['py_' + name];
        }
    };
    __all__.delattr = (delattr);
    var __in__ = function (element, container) {
        if (container === undefined || container === null) {
            return false;
        }
        if (container.__contains__ instanceof Function) {
            return container.__contains__ (element);
        }
        else {
            return (
                container.indexOf ?
                container.indexOf (element) > -1 :
                container.hasOwnProperty (element)
            );
        }
    };
    __all__.__in__ = __in__;
    var __specialattrib__ = function (attrib) {
        return (attrib.startswith ('__') && attrib.endswith ('__')) || attrib == 'constructor' || attrib.startswith ('py_');
    };
    __all__.__specialattrib__ = __specialattrib__;
    var len = function (anObject) {
        if (anObject === undefined || anObject === null) {
            return 0;
        }
        if (anObject.__len__ instanceof Function) {
            return anObject.__len__ ();
        }
        if (anObject.length !== undefined) {
            return anObject.length;
        }
        var length = 0;
        for (var attr in anObject) {
            if (!__specialattrib__ (attr)) {
                length++;
            }
        }
        return length;
    };
    __all__.len = len;
    function __i__ (any) {
        return py_typeof (any) == dict ? any.py_keys () : any;
    }
    function __k__ (keyed, key) {
        var result = keyed [key];
        if (typeof result == 'undefined') {
            if (keyed instanceof Array)
                if (key == +key && key >= 0 && keyed.length > key)
                    return result;
                else
                    throw IndexError (key, new Error());
            else
                throw KeyError (key, new Error());
        }
        return result;
    }
    function __t__ (target) {
        return (
            target === undefined || target === null ? false :
            ['boolean', 'number'] .indexOf (typeof target) >= 0 ? target :
            target.__bool__ instanceof Function ? (target.__bool__ () ? target : false) :
            target.__len__ instanceof Function ?  (target.__len__ () !== 0 ? target : false) :
            target instanceof Function ? target :
            len (target) !== 0 ? target :
            false
        );
    }
    __all__.__t__ = __t__;
    var float = function (any) {
        if (any == 'inf') {
            return Infinity;
        }
        else if (any == '-inf') {
            return -Infinity;
        }
        else if (any == 'nan') {
            return NaN;
        }
        else if (isNaN (parseFloat (any))) {
            if (any === false) {
                return 0;
            }
            else if (any === true) {
                return 1;
            }
            else {
                throw ValueError ("could not convert string to float: '" + str(any) + "'", new Error ());
            }
        }
        else {
            return +any;
        }
    };
    float.__name__ = 'float';
    float.__bases__ = [object];
    __all__.float = float;
    var int = function (any) {
        return float (any) | 0
    };
    int.__name__ = 'int';
    int.__bases__ = [object];
    __all__.int = int;
    var bool = function (any) {
        return !!__t__ (any);
    };
    bool.__name__ = 'bool';
    bool.__bases__ = [int];
    __all__.bool = bool;
    var py_typeof = function (anObject) {
        var aType = typeof anObject;
        if (aType == 'object') {
            try {
                return '__class__' in anObject ? anObject.__class__ : object;
            }
            catch (exception) {
                return aType;
            }
        }
        else {
            return (
                aType == 'boolean' ? bool :
                aType == 'string' ? str :
                aType == 'number' ? (anObject % 1 == 0 ? int : float) :
                null
            );
        }
    };
    __all__.py_typeof = py_typeof;
    var issubclass = function (aClass, classinfo) {
        if (classinfo instanceof Array) {
            for (var index = 0; index < classinfo.length; index++) {
                var aClass2 = classinfo [index];
                if (issubclass (aClass, aClass2)) {
                    return true;
                }
            }
            return false;
        }
        try {
            var aClass2 = aClass;
            if (aClass2 == classinfo) {
                return true;
            }
            else {
                var bases = [].slice.call (aClass2.__bases__);
                while (bases.length) {
                    aClass2 = bases.shift ();
                    if (aClass2 == classinfo) {
                        return true;
                    }
                    if (aClass2.__bases__.length) {
                        bases = [].slice.call (aClass2.__bases__).concat (bases);
                    }
                }
                return false;
            }
        }
        catch (exception) {
            return aClass == classinfo || classinfo == object;
        }
    };
    __all__.issubclass = issubclass;
    var isinstance = function (anObject, classinfo) {
        try {
            return '__class__' in anObject ? issubclass (anObject.__class__, classinfo) : issubclass (py_typeof (anObject), classinfo);
        }
        catch (exception) {
            return issubclass (py_typeof (anObject), classinfo);
        }
    };
    __all__.isinstance = isinstance;
    var callable = function (anObject) {
        return anObject && typeof anObject == 'object' && '__call__' in anObject ? true : typeof anObject === 'function';
    };
    __all__.callable = callable;
    var repr = function (anObject) {
        try {
            return anObject.__repr__ ();
        }
        catch (exception) {
            try {
                return anObject.__str__ ();
            }
            catch (exception) {
                try {
                    if (anObject == null) {
                        return 'None';
                    }
                    else if (anObject.constructor == Object) {
                        var result = '{';
                        var comma = false;
                        for (var attrib in anObject) {
                            if (!__specialattrib__ (attrib)) {
                                if (attrib.isnumeric ()) {
                                    var attribRepr = attrib;
                                }
                                else {
                                    var attribRepr = '\'' + attrib + '\'';
                                }
                                if (comma) {
                                    result += ', ';
                                }
                                else {
                                    comma = true;
                                }
                                result += attribRepr + ': ' + repr (anObject [attrib]);
                            }
                        }
                        result += '}';
                        return result;
                    }
                    else {
                        return typeof anObject == 'boolean' ? anObject.toString () .capitalize () : anObject.toString ();
                    }
                }
                catch (exception) {
                    return '<object of type: ' + typeof anObject + '>';
                }
            }
        }
    };
    __all__.repr = repr;
    var chr = function (charCode) {
        return String.fromCharCode (charCode);
    };
    __all__.chr = chr;
    var ord = function (aChar) {
        return aChar.charCodeAt (0);
    };
    __all__.ord = ord;
    var max = function (nrOrSeq) {
        return arguments.length == 1 ? Math.max.apply (null, nrOrSeq) : Math.max.apply (null, arguments);
    };
    __all__.max = max;
    var min = function (nrOrSeq) {
        return arguments.length == 1 ? Math.min.apply (null, nrOrSeq) : Math.min.apply (null, arguments);
    };
    __all__.min = min;
    var abs = Math.abs;
    __all__.abs = abs;
    var round = function (number, ndigits) {
        if (ndigits) {
            var scale = Math.pow (10, ndigits);
            number *= scale;
        }
        var rounded = Math.round (number);
        if (rounded - number == 0.5 && rounded % 2) {
            rounded -= 1;
        }
        if (ndigits) {
            rounded /= scale;
        }
        return rounded;
    };
    __all__.round = round;
    function __jsUsePyNext__ () {
        try {
            var result = this.__next__ ();
            return {value: result, done: false};
        }
        catch (exception) {
            return {value: undefined, done: true};
        }
    }
    function __pyUseJsNext__ () {
        var result = this.next ();
        if (result.done) {
            throw StopIteration (new Error ());
        }
        else {
            return result.value;
        }
    }
    function py_iter (iterable) {
        if (typeof iterable == 'string' || '__iter__' in iterable) {
            var result = iterable.__iter__ ();
            result.next = __jsUsePyNext__;
        }
        else if ('selector' in iterable) {
            var result = list (iterable) .__iter__ ();
            result.next = __jsUsePyNext__;
        }
        else if ('next' in iterable) {
            var result = iterable
            if (! ('__next__' in result)) {
                result.__next__ = __pyUseJsNext__;
            }
        }
        else if (Symbol.iterator in iterable) {
            var result = iterable [Symbol.iterator] ();
            result.__next__ = __pyUseJsNext__;
        }
        else {
            throw IterableError (new Error ());
        }
        result [Symbol.iterator] = function () {return result;};
        return result;
    }
    function py_next (iterator) {
        try {
            var result = iterator.__next__ ();
        }
        catch (exception) {
            var result = iterator.next ();
            if (result.done) {
                throw StopIteration (new Error ());
            }
            else {
                return result.value;
            }
        }
        if (result == undefined) {
            throw StopIteration (new Error ());
        }
        else {
            return result;
        }
    }
    function __PyIterator__ (iterable) {
        this.iterable = iterable;
        this.index = 0;
    }
    __PyIterator__.prototype.__next__ = function () {
        if (this.index < this.iterable.length) {
            return this.iterable [this.index++];
        }
        else {
            throw StopIteration (new Error ());
        }
    };
    function __JsIterator__ (iterable) {
        this.iterable = iterable;
        this.index = 0;
    }
    __JsIterator__.prototype.next = function () {
        if (this.index < this.iterable.py_keys.length) {
            return {value: this.index++, done: false};
        }
        else {
            return {value: undefined, done: true};
        }
    };
    var py_reversed = function (iterable) {
        iterable = iterable.slice ();
        iterable.reverse ();
        return iterable;
    };
    __all__.py_reversed = py_reversed;
    var zip = function () {
        var args = [] .slice.call (arguments);
        for (var i = 0; i < args.length; i++) {
            if (typeof args [i] == 'string') {
                args [i] = args [i] .split ('');
            }
            else if (!Array.isArray (args [i])) {
                args [i] = Array.from (args [i]);
            }
        }
        var shortest = args.length == 0 ? [] : args.reduce (
            function (array0, array1) {
                return array0.length < array1.length ? array0 : array1;
            }
        );
        return shortest.map (
            function (current, index) {
                return args.map (
                    function (current) {
                        return current [index];
                    }
                );
            }
        );
    };
    __all__.zip = zip;
    function range (start, stop, step) {
        if (stop == undefined) {
            stop = start;
            start = 0;
        }
        if (step == undefined) {
            step = 1;
        }
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }
        var result = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.push(i);
        }
        return result;
    };
    __all__.range = range;
    function any (iterable) {
        for (var index = 0; index < iterable.length; index++) {
            if (bool (iterable [index])) {
                return true;
            }
        }
        return false;
    }
    function all (iterable) {
        for (var index = 0; index < iterable.length; index++) {
            if (! bool (iterable [index])) {
                return false;
            }
        }
        return true;
    }
    function sum (iterable) {
        var result = 0;
        for (var index = 0; index < iterable.length; index++) {
            result += iterable [index];
        }
        return result;
    }
    __all__.any = any;
    __all__.all = all;
    __all__.sum = sum;
    function enumerate (iterable) {
        return zip (range (len (iterable)), iterable);
    }
    __all__.enumerate = enumerate;
    function copy (anObject) {
        if (anObject == null || typeof anObject == "object") {
            return anObject;
        }
        else {
            var result = {};
            for (var attrib in obj) {
                if (anObject.hasOwnProperty (attrib)) {
                    result [attrib] = anObject [attrib];
                }
            }
            return result;
        }
    }
    __all__.copy = copy;
    function deepcopy (anObject) {
        if (anObject == null || typeof anObject == "object") {
            return anObject;
        }
        else {
            var result = {};
            for (var attrib in obj) {
                if (anObject.hasOwnProperty (attrib)) {
                    result [attrib] = deepcopy (anObject [attrib]);
                }
            }
            return result;
        }
    }
    __all__.deepcopy = deepcopy;
    function list (iterable) {
        var instance = iterable ? [] .slice.apply (iterable) : [];
        return instance;
    }
    __all__.list = list;
    Array.prototype.__class__ = list;
    list.__name__ = 'list';
    list.__bases__ = [object];
    Array.prototype.__iter__ = function () {return new __PyIterator__ (this);};
    Array.prototype.__getslice__ = function (start, stop, step) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        else if (stop > this.length) {
            stop = this.length;
        }
        var result = list ([]);
        for (var index = start; index < stop; index += step) {
            result.push (this [index]);
        }
        return result;
    };
    Array.prototype.__setslice__ = function (start, stop, step, source) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        if (step == null) {
            Array.prototype.splice.apply (this, [start, stop - start] .concat (source));
        }
        else {
            var sourceIndex = 0;
            for (var targetIndex = start; targetIndex < stop; targetIndex += step) {
                this [targetIndex] = source [sourceIndex++];
            }
        }
    };
    Array.prototype.__repr__ = function () {
        if (this.__class__ == set && !this.length) {
            return 'set()';
        }
        var result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';
        for (var index = 0; index < this.length; index++) {
            if (index) {
                result += ', ';
            }
            result += repr (this [index]);
        }
        if (this.__class__ == tuple && this.length == 1) {
            result += ',';
        }
        result += !this.__class__ || this.__class__ == list ? ']' : this.__class__ == tuple ? ')' : '}';;
        return result;
    };
    Array.prototype.__str__ = Array.prototype.__repr__;
    Array.prototype.append = function (element) {
        this.push (element);
    };
    Array.prototype.py_clear = function () {
        this.length = 0;
    };
    Array.prototype.extend = function (aList) {
        this.push.apply (this, aList);
    };
    Array.prototype.insert = function (index, element) {
        this.splice (index, 0, element);
    };
    Array.prototype.remove = function (element) {
        var index = this.indexOf (element);
        if (index == -1) {
            throw ValueError ("list.remove(x): x not in list", new Error ());
        }
        this.splice (index, 1);
    };
    Array.prototype.index = function (element) {
        return this.indexOf (element);
    };
    Array.prototype.py_pop = function (index) {
        if (index == undefined) {
            return this.pop ();
        }
        else {
            return this.splice (index, 1) [0];
        }
    };
    Array.prototype.py_sort = function () {
        __sort__.apply  (null, [this].concat ([] .slice.apply (arguments)));
    };
    Array.prototype.__add__ = function (aList) {
        return list (this.concat (aList));
    };
    Array.prototype.__mul__ = function (scalar) {
        var result = this;
        for (var i = 1; i < scalar; i++) {
            result = result.concat (this);
        }
        return result;
    };
    Array.prototype.__rmul__ = Array.prototype.__mul__;
    function tuple (iterable) {
        var instance = iterable ? [] .slice.apply (iterable) : [];
        instance.__class__ = tuple;
        return instance;
    }
    __all__.tuple = tuple;
    tuple.__name__ = 'tuple';
    tuple.__bases__ = [object];
    function set (iterable) {
        var instance = [];
        if (iterable) {
            for (var index = 0; index < iterable.length; index++) {
                instance.add (iterable [index]);
            }
        }
        instance.__class__ = set;
        return instance;
    }
    __all__.set = set;
    set.__name__ = 'set';
    set.__bases__ = [object];
    Array.prototype.__bindexOf__ = function (element) {
        element += '';
        var mindex = 0;
        var maxdex = this.length - 1;
        while (mindex <= maxdex) {
            var index = (mindex + maxdex) / 2 | 0;
            var middle = this [index] + '';
            if (middle < element) {
                mindex = index + 1;
            }
            else if (middle > element) {
                maxdex = index - 1;
            }
            else {
                return index;
            }
        }
        return -1;
    };
    Array.prototype.add = function (element) {
        if (this.indexOf (element) == -1) {
            this.push (element);
        }
    };
    Array.prototype.discard = function (element) {
        var index = this.indexOf (element);
        if (index != -1) {
            this.splice (index, 1);
        }
    };
    Array.prototype.isdisjoint = function (other) {
        this.sort ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) != -1) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.issuperset = function (other) {
        this.sort ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) == -1) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.issubset = function (other) {
        return set (other.slice ()) .issuperset (this);
    };
    Array.prototype.union = function (other) {
        var result = set (this.slice () .sort ());
        for (var i = 0; i < other.length; i++) {
            if (result.__bindexOf__ (other [i]) == -1) {
                result.push (other [i]);
            }
        }
        return result;
    };
    Array.prototype.intersection = function (other) {
        this.sort ();
        var result = set ();
        for (var i = 0; i < other.length; i++) {
            if (this.__bindexOf__ (other [i]) != -1) {
                result.push (other [i]);
            }
        }
        return result;
    };
    Array.prototype.difference = function (other) {
        var sother = set (other.slice () .sort ());
        var result = set ();
        for (var i = 0; i < this.length; i++) {
            if (sother.__bindexOf__ (this [i]) == -1) {
                result.push (this [i]);
            }
        }
        return result;
    };
    Array.prototype.symmetric_difference = function (other) {
        return this.union (other) .difference (this.intersection (other));
    };
    Array.prototype.py_update = function () {
        var updated = [] .concat.apply (this.slice (), arguments) .sort ();
        this.py_clear ();
        for (var i = 0; i < updated.length; i++) {
            if (updated [i] != updated [i - 1]) {
                this.push (updated [i]);
            }
        }
    };
    Array.prototype.__eq__ = function (other) {
        if (this.length != other.length) {
            return false;
        }
        if (this.__class__ == set) {
            this.sort ();
            other.sort ();
        }
        for (var i = 0; i < this.length; i++) {
            if (this [i] != other [i]) {
                return false;
            }
        }
        return true;
    };
    Array.prototype.__ne__ = function (other) {
        return !this.__eq__ (other);
    };
    Array.prototype.__le__ = function (other) {
        return this.issubset (other);
    };
    Array.prototype.__ge__ = function (other) {
        return this.issuperset (other);
    };
    Array.prototype.__lt__ = function (other) {
        return this.issubset (other) && !this.issuperset (other);
    };
    Array.prototype.__gt__ = function (other) {
        return this.issuperset (other) && !this.issubset (other);
    };
    function bytearray (bytable, encoding) {
        if (bytable == undefined) {
            return new Uint8Array (0);
        }
        else {
            var aType = py_typeof (bytable);
            if (aType == int) {
                return new Uint8Array (bytable);
            }
            else if (aType == str) {
                var aBytes = new Uint8Array (len (bytable));
                for (var i = 0; i < len (bytable); i++) {
                    aBytes [i] = bytable.charCodeAt (i);
                }
                return aBytes;
            }
            else if (aType == list || aType == tuple) {
                return new Uint8Array (bytable);
            }
            else {
                throw py_TypeError;
            }
        }
    }
    var bytes = bytearray;
    __all__.bytearray = bytearray;
    __all__.bytes = bytearray;
    Uint8Array.prototype.__add__ = function (aBytes) {
        var result = new Uint8Array (this.length + aBytes.length);
        result.set (this);
        result.set (aBytes, this.length);
        return result;
    };
    Uint8Array.prototype.__mul__ = function (scalar) {
        var result = new Uint8Array (scalar * this.length);
        for (var i = 0; i < scalar; i++) {
            result.set (this, i * this.length);
        }
        return result;
    };
    Uint8Array.prototype.__rmul__ = Uint8Array.prototype.__mul__;
    function str (stringable) {
        if (typeof stringable === 'number')
            return stringable.toString();
        else {
            try {
                return stringable.__str__ ();
            }
            catch (exception) {
                try {
                    return repr (stringable);
                }
                catch (exception) {
                    return String (stringable);
                }
            }
        }
    };
    __all__.str = str;
    String.prototype.__class__ = str;
    str.__name__ = 'str';
    str.__bases__ = [object];
    String.prototype.__iter__ = function () {new __PyIterator__ (this);};
    String.prototype.__repr__ = function () {
        return (this.indexOf ('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"') .py_replace ('\t', '\\t') .py_replace ('\n', '\\n');
    };
    String.prototype.__str__ = function () {
        return this;
    };
    String.prototype.capitalize = function () {
        return this.charAt (0).toUpperCase () + this.slice (1);
    };
    String.prototype.endswith = function (suffix) {
        if (suffix instanceof Array) {
            for (var i=0;i<suffix.length;i++) {
                if (this.slice (-suffix[i].length) == suffix[i])
                    return true;
            }
        } else
            return suffix == '' || this.slice (-suffix.length) == suffix;
        return false;
    };
    String.prototype.find  = function (sub, start) {
        return this.indexOf (sub, start);
    };
    String.prototype.__getslice__ = function (start, stop, step) {
        if (start < 0) {
            start = this.length + start;
        }
        if (stop == null) {
            stop = this.length;
        }
        else if (stop < 0) {
            stop = this.length + stop;
        }
        var result = '';
        if (step == 1) {
            result = this.substring (start, stop);
        }
        else {
            for (var index = start; index < stop; index += step) {
                result = result.concat (this.charAt(index));
            }
        }
        return result;
    };
    __setProperty__ (String.prototype, 'format', {
        get: function () {return __get__ (this, function (self) {
            var args = tuple ([] .slice.apply (arguments).slice (1));
            var autoIndex = 0;
            return self.replace (/\{(\w*)\}/g, function (match, key) {
                if (key == '') {
                    key = autoIndex++;
                }
                if (key == +key) {
                    return args [key] == undefined ? match : str (args [key]);
                }
                else {
                    for (var index = 0; index < args.length; index++) {
                        if (typeof args [index] == 'object' && args [index][key] != undefined) {
                            return str (args [index][key]);
                        }
                    }
                    return match;
                }
            });
        });},
        enumerable: true
    });
    String.prototype.isalnum = function () {
        return /^[0-9a-zA-Z]{1,}$/.test(this)
    }
    String.prototype.isalpha = function () {
        return /^[a-zA-Z]{1,}$/.test(this)
    }
    String.prototype.isdecimal = function () {
        return /^[0-9]{1,}$/.test(this)
    }
    String.prototype.isdigit = function () {
        return this.isdecimal()
    }
    String.prototype.islower = function () {
        return /^[a-z]{1,}$/.test(this)
    }
    String.prototype.isupper = function () {
        return /^[A-Z]{1,}$/.test(this)
    }
    String.prototype.isspace = function () {
        return /^[\s]{1,}$/.test(this)
    }
    String.prototype.isnumeric = function () {
        return !isNaN (parseFloat (this)) && isFinite (this);
    };
    String.prototype.join = function (strings) {
        return strings.join (this);
    };
    String.prototype.lower = function () {
        return this.toLowerCase ();
    };
    String.prototype.py_replace = function (old, aNew, maxreplace) {
        return this.split (old, maxreplace) .join (aNew);
    };
    String.prototype.lstrip = function () {
        return this.replace (/^\s*/g, '');
    };
    String.prototype.rfind = function (sub, start) {
        return this.lastIndexOf (sub, start);
    };
    String.prototype.rsplit = function (sep, maxsplit) {
        if (sep == undefined || sep == null) {
            sep = /\s+/;
            var stripped = this.strip ();
        }
        else {
            var stripped = this;
        }
        if (maxsplit == undefined || maxsplit == -1) {
            return stripped.split (sep);
        }
        else {
            var result = stripped.split (sep);
            if (maxsplit < result.length) {
                var maxrsplit = result.length - maxsplit;
                return [result.slice (0, maxrsplit) .join (sep)] .concat (result.slice (maxrsplit));
            }
            else {
                return result;
            }
        }
    };
    String.prototype.rstrip = function () {
        return this.replace (/\s*$/g, '');
    };
    String.prototype.py_split = function (sep, maxsplit) {
        if (sep == undefined || sep == null) {
            sep = /\s+/;
            var stripped = this.strip ();
        }
        else {
            var stripped = this;
        }
        if (maxsplit == undefined || maxsplit == -1) {
            return stripped.split (sep);
        }
        else {
            var result = stripped.split (sep);
            if (maxsplit < result.length) {
                return result.slice (0, maxsplit).concat ([result.slice (maxsplit).join (sep)]);
            }
            else {
                return result;
            }
        }
    };
    String.prototype.startswith = function (prefix) {
        if (prefix instanceof Array) {
            for (var i=0;i<prefix.length;i++) {
                if (this.indexOf (prefix [i]) == 0)
                    return true;
            }
        } else
            return this.indexOf (prefix) == 0;
        return false;
    };
    String.prototype.strip = function () {
        return this.trim ();
    };
    String.prototype.upper = function () {
        return this.toUpperCase ();
    };
    String.prototype.__mul__ = function (scalar) {
        var result = '';
        for (var i = 0; i < scalar; i++) {
            result = result + this;
        }
        return result;
    };
    String.prototype.__rmul__ = String.prototype.__mul__;
    function __contains__ (element) {
        return this.hasOwnProperty (element);
    }
    function __keys__ () {
        var keys = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                keys.push (attrib);
            }
        }
        return keys;
    }
    function __items__ () {
        var items = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                items.push ([attrib, this [attrib]]);
            }
        }
        return items;
    }
    function __del__ (key) {
        delete this [key];
    }
    function __clear__ () {
        for (var attrib in this) {
            delete this [attrib];
        }
    }
    function __getdefault__ (aKey, aDefault) {
        var result = this [aKey];
        if (result == undefined) {
            result = this ['py_' + aKey]
        }
        return result == undefined ? (aDefault == undefined ? null : aDefault) : result;
    }
    function __setdefault__ (aKey, aDefault) {
        var result = this [aKey];
        if (result != undefined) {
            return result;
        }
        var val = aDefault == undefined ? null : aDefault;
        this [aKey] = val;
        return val;
    }
    function __pop__ (aKey, aDefault) {
        var result = this [aKey];
        if (result != undefined) {
            delete this [aKey];
            return result;
        } else {
            if ( aDefault === undefined ) {
                throw KeyError (aKey, new Error());
            }
        }
        return aDefault;
    }
    function __popitem__ () {
        var aKey = Object.keys (this) [0];
        if (aKey == null) {
            throw KeyError ("popitem(): dictionary is empty", new Error ());
        }
        var result = tuple ([aKey, this [aKey]]);
        delete this [aKey];
        return result;
    }
    function __update__ (aDict) {
        for (var aKey in aDict) {
            this [aKey] = aDict [aKey];
        }
    }
    function __values__ () {
        var values = [];
        for (var attrib in this) {
            if (!__specialattrib__ (attrib)) {
                values.push (this [attrib]);
            }
        }
        return values;
    }
    function __dgetitem__ (aKey) {
        return this [aKey];
    }
    function __dsetitem__ (aKey, aValue) {
        this [aKey] = aValue;
    }
    function dict (objectOrPairs) {
        var instance = {};
        if (!objectOrPairs || objectOrPairs instanceof Array) {
            if (objectOrPairs) {
                for (var index = 0; index < objectOrPairs.length; index++) {
                    var pair = objectOrPairs [index];
                    if ( !(pair instanceof Array) || pair.length != 2) {
                        throw ValueError(
                            "dict update sequence element #" + index +
                            " has length " + pair.length +
                            "; 2 is required", new Error());
                    }
                    var key = pair [0];
                    var val = pair [1];
                    if (!(objectOrPairs instanceof Array) && objectOrPairs instanceof Object) {
                         if (!isinstance (objectOrPairs, dict)) {
                             val = dict (val);
                         }
                    }
                    instance [key] = val;
                }
            }
        }
        else {
            if (isinstance (objectOrPairs, dict)) {
                var aKeys = objectOrPairs.py_keys ();
                for (var index = 0; index < aKeys.length; index++ ) {
                    var key = aKeys [index];
                    instance [key] = objectOrPairs [key];
                }
            } else if (objectOrPairs instanceof Object) {
                instance = objectOrPairs;
            } else {
                throw ValueError ("Invalid type of object for dict creation", new Error ());
            }
        }
        __setProperty__ (instance, '__class__', {value: dict, enumerable: false, writable: true});
        __setProperty__ (instance, '__contains__', {value: __contains__, enumerable: false});
        __setProperty__ (instance, 'py_keys', {value: __keys__, enumerable: false});
        __setProperty__ (instance, '__iter__', {value: function () {new __PyIterator__ (this.py_keys ());}, enumerable: false});
        __setProperty__ (instance, Symbol.iterator, {value: function () {new __JsIterator__ (this.py_keys ());}, enumerable: false});
        __setProperty__ (instance, 'py_items', {value: __items__, enumerable: false});
        __setProperty__ (instance, 'py_del', {value: __del__, enumerable: false});
        __setProperty__ (instance, 'py_clear', {value: __clear__, enumerable: false});
        __setProperty__ (instance, 'py_get', {value: __getdefault__, enumerable: false});
        __setProperty__ (instance, 'py_setdefault', {value: __setdefault__, enumerable: false});
        __setProperty__ (instance, 'py_pop', {value: __pop__, enumerable: false});
        __setProperty__ (instance, 'py_popitem', {value: __popitem__, enumerable: false});
        __setProperty__ (instance, 'py_update', {value: __update__, enumerable: false});
        __setProperty__ (instance, 'py_values', {value: __values__, enumerable: false});
        __setProperty__ (instance, '__getitem__', {value: __dgetitem__, enumerable: false});
        __setProperty__ (instance, '__setitem__', {value: __dsetitem__, enumerable: false});
        return instance;
    }
    __all__.dict = dict;
    dict.__name__ = 'dict';
    dict.__bases__ = [object];
    function __setdoc__ (docString) {
        this.__doc__ = docString;
        return this;
    }
    __setProperty__ (Function.prototype, '__setdoc__', {value: __setdoc__, enumerable: false});
    var __jsmod__ = function (a, b) {
        if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return a % b;
        }
    };
    __all__.__jsmod__ = __jsmod__;
    var __mod__ = function (a, b) {
        if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return ((a % b) + b) % b;
        }
    };
    __all__.mod = __mod__;
    var __pow__ = function (a, b) {
        if (typeof a == 'object' && '__pow__' in a) {
            return a.__pow__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rpow__ (a);
        }
        else {
            return Math.pow (a, b);
        }
    };
    __all__.pow = __pow__;
    var __neg__ = function (a) {
        if (typeof a == 'object' && '__neg__' in a) {
            return a.__neg__ ();
        }
        else {
            return -a;
        }
    };
    __all__.__neg__ = __neg__;
    var __matmul__ = function (a, b) {
        return a.__matmul__ (b);
    };
    __all__.__matmul__ = __matmul__;
    var __mul__ = function (a, b) {
        if (typeof a == 'object' && '__mul__' in a) {
            return a.__mul__ (b);
        }
        else if (typeof b == 'object' && '__rmul__' in b) {
            return b.__rmul__ (a);
        }
        else if (typeof a == 'string') {
            return a.__mul__ (b);
        }
        else if (typeof b == 'string') {
            return b.__rmul__ (a);
        }
        else {
            return a * b;
        }
    };
    __all__.__mul__ = __mul__;
    var __truediv__ = function (a, b) {
        if (typeof a == 'object' && '__truediv__' in a) {
            return a.__truediv__ (b);
        }
        else if (typeof b == 'object' && '__rtruediv__' in b) {
            return b.__rtruediv__ (a);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return b.__rdiv__ (a);
        }
        else {
            return a / b;
        }
    };
    __all__.__truediv__ = __truediv__;
    var __floordiv__ = function (a, b) {
        if (typeof a == 'object' && '__floordiv__' in a) {
            return a.__floordiv__ (b);
        }
        else if (typeof b == 'object' && '__rfloordiv__' in b) {
            return b.__rfloordiv__ (a);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return b.__rdiv__ (a);
        }
        else {
            return Math.floor (a / b);
        }
    };
    __all__.__floordiv__ = __floordiv__;
    var __add__ = function (a, b) {
        if (typeof a == 'object' && '__add__' in a) {
            return a.__add__ (b);
        }
        else if (typeof b == 'object' && '__radd__' in b) {
            return b.__radd__ (a);
        }
        else {
            return a + b;
        }
    };
    __all__.__add__ = __add__;
    var __sub__ = function (a, b) {
        if (typeof a == 'object' && '__sub__' in a) {
            return a.__sub__ (b);
        }
        else if (typeof b == 'object' && '__rsub__' in b) {
            return b.__rsub__ (a);
        }
        else {
            return a - b;
        }
    };
    __all__.__sub__ = __sub__;
    var __lshift__ = function (a, b) {
        if (typeof a == 'object' && '__lshift__' in a) {
            return a.__lshift__ (b);
        }
        else if (typeof b == 'object' && '__rlshift__' in b) {
            return b.__rlshift__ (a);
        }
        else {
            return a << b;
        }
    };
    __all__.__lshift__ = __lshift__;
    var __rshift__ = function (a, b) {
        if (typeof a == 'object' && '__rshift__' in a) {
            return a.__rshift__ (b);
        }
        else if (typeof b == 'object' && '__rrshift__' in b) {
            return b.__rrshift__ (a);
        }
        else {
            return a >> b;
        }
    };
    __all__.__rshift__ = __rshift__;
    var __or__ = function (a, b) {
        if (typeof a == 'object' && '__or__' in a) {
            return a.__or__ (b);
        }
        else if (typeof b == 'object' && '__ror__' in b) {
            return b.__ror__ (a);
        }
        else {
            return a | b;
        }
    };
    __all__.__or__ = __or__;
    var __xor__ = function (a, b) {
        if (typeof a == 'object' && '__xor__' in a) {
            return a.__xor__ (b);
        }
        else if (typeof b == 'object' && '__rxor__' in b) {
            return b.__rxor__ (a);
        }
        else {
            return a ^ b;
        }
    };
    __all__.__xor__ = __xor__;
    var __and__ = function (a, b) {
        if (typeof a == 'object' && '__and__' in a) {
            return a.__and__ (b);
        }
        else if (typeof b == 'object' && '__rand__' in b) {
            return b.__rand__ (a);
        }
        else {
            return a & b;
        }
    };
    __all__.__and__ = __and__;
    var __eq__ = function (a, b) {
        if (typeof a == 'object' && '__eq__' in a) {
            return a.__eq__ (b);
        }
        else {
            return a == b;
        }
    };
    __all__.__eq__ = __eq__;
    var __ne__ = function (a, b) {
        if (typeof a == 'object' && '__ne__' in a) {
            return a.__ne__ (b);
        }
        else {
            return a != b
        }
    };
    __all__.__ne__ = __ne__;
    var __lt__ = function (a, b) {
        if (typeof a == 'object' && '__lt__' in a) {
            return a.__lt__ (b);
        }
        else {
            return a < b;
        }
    };
    __all__.__lt__ = __lt__;
    var __le__ = function (a, b) {
        if (typeof a == 'object' && '__le__' in a) {
            return a.__le__ (b);
        }
        else {
            return a <= b;
        }
    };
    __all__.__le__ = __le__;
    var __gt__ = function (a, b) {
        if (typeof a == 'object' && '__gt__' in a) {
            return a.__gt__ (b);
        }
        else {
            return a > b;
        }
    };
    __all__.__gt__ = __gt__;
    var __ge__ = function (a, b) {
        if (typeof a == 'object' && '__ge__' in a) {
            return a.__ge__ (b);
        }
        else {
            return a >= b;
        }
    };
    __all__.__ge__ = __ge__;
    var __imatmul__ = function (a, b) {
        if ('__imatmul__' in a) {
            return a.__imatmul__ (b);
        }
        else {
            return a.__matmul__ (b);
        }
    };
    __all__.__imatmul__ = __imatmul__;
    var __ipow__ = function (a, b) {
        if (typeof a == 'object' && '__pow__' in a) {
            return a.__ipow__ (b);
        }
        else if (typeof a == 'object' && '__ipow__' in a) {
            return a.__pow__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rpow__ (a);
        }
        else {
            return Math.pow (a, b);
        }
    };
    __all__.ipow = __ipow__;
    var __ijsmod__ = function (a, b) {
        if (typeof a == 'object' && '__imod__' in a) {
            return a.__ismod__ (b);
        }
        else if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rpow__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return a % b;
        }
    };
    __all__.ijsmod__ = __ijsmod__;
    var __imod__ = function (a, b) {
        if (typeof a == 'object' && '__imod__' in a) {
            return a.__imod__ (b);
        }
        else if (typeof a == 'object' && '__mod__' in a) {
            return a.__mod__ (b);
        }
        else if (typeof b == 'object' && '__rmod__' in b) {
            return b.__rmod__ (a);
        }
        else {
            return ((a % b) + b) % b;
        }
    };
    __all__.imod = __imod__;
    var __imul__ = function (a, b) {
        if (typeof a == 'object' && '__imul__' in a) {
            return a.__imul__ (b);
        }
        else if (typeof a == 'object' && '__mul__' in a) {
            return a = a.__mul__ (b);
        }
        else if (typeof b == 'object' && '__rmul__' in b) {
            return a = b.__rmul__ (a);
        }
        else if (typeof a == 'string') {
            return a = a.__mul__ (b);
        }
        else if (typeof b == 'string') {
            return a = b.__rmul__ (a);
        }
        else {
            return a *= b;
        }
    };
    __all__.__imul__ = __imul__;
    var __idiv__ = function (a, b) {
        if (typeof a == 'object' && '__idiv__' in a) {
            return a.__idiv__ (b);
        }
        else if (typeof a == 'object' && '__div__' in a) {
            return a = a.__div__ (b);
        }
        else if (typeof b == 'object' && '__rdiv__' in b) {
            return a = b.__rdiv__ (a);
        }
        else {
            return a /= b;
        }
    };
    __all__.__idiv__ = __idiv__;
    var __iadd__ = function (a, b) {
        if (typeof a == 'object' && '__iadd__' in a) {
            return a.__iadd__ (b);
        }
        else if (typeof a == 'object' && '__add__' in a) {
            return a = a.__add__ (b);
        }
        else if (typeof b == 'object' && '__radd__' in b) {
            return a = b.__radd__ (a);
        }
        else {
            return a += b;
        }
    };
    __all__.__iadd__ = __iadd__;
    var __isub__ = function (a, b) {
        if (typeof a == 'object' && '__isub__' in a) {
            return a.__isub__ (b);
        }
        else if (typeof a == 'object' && '__sub__' in a) {
            return a = a.__sub__ (b);
        }
        else if (typeof b == 'object' && '__rsub__' in b) {
            return a = b.__rsub__ (a);
        }
        else {
            return a -= b;
        }
    };
    __all__.__isub__ = __isub__;
    var __ilshift__ = function (a, b) {
        if (typeof a == 'object' && '__ilshift__' in a) {
            return a.__ilshift__ (b);
        }
        else if (typeof a == 'object' && '__lshift__' in a) {
            return a = a.__lshift__ (b);
        }
        else if (typeof b == 'object' && '__rlshift__' in b) {
            return a = b.__rlshift__ (a);
        }
        else {
            return a <<= b;
        }
    };
    __all__.__ilshift__ = __ilshift__;
    var __irshift__ = function (a, b) {
        if (typeof a == 'object' && '__irshift__' in a) {
            return a.__irshift__ (b);
        }
        else if (typeof a == 'object' && '__rshift__' in a) {
            return a = a.__rshift__ (b);
        }
        else if (typeof b == 'object' && '__rrshift__' in b) {
            return a = b.__rrshift__ (a);
        }
        else {
            return a >>= b;
        }
    };
    __all__.__irshift__ = __irshift__;
    var __ior__ = function (a, b) {
        if (typeof a == 'object' && '__ior__' in a) {
            return a.__ior__ (b);
        }
        else if (typeof a == 'object' && '__or__' in a) {
            return a = a.__or__ (b);
        }
        else if (typeof b == 'object' && '__ror__' in b) {
            return a = b.__ror__ (a);
        }
        else {
            return a |= b;
        }
    };
    __all__.__ior__ = __ior__;
    var __ixor__ = function (a, b) {
        if (typeof a == 'object' && '__ixor__' in a) {
            return a.__ixor__ (b);
        }
        else if (typeof a == 'object' && '__xor__' in a) {
            return a = a.__xor__ (b);
        }
        else if (typeof b == 'object' && '__rxor__' in b) {
            return a = b.__rxor__ (a);
        }
        else {
            return a ^= b;
        }
    };
    __all__.__ixor__ = __ixor__;
    var __iand__ = function (a, b) {
        if (typeof a == 'object' && '__iand__' in a) {
            return a.__iand__ (b);
        }
        else if (typeof a == 'object' && '__and__' in a) {
            return a = a.__and__ (b);
        }
        else if (typeof b == 'object' && '__rand__' in b) {
            return a = b.__rand__ (a);
        }
        else {
            return a &= b;
        }
    };
    __all__.__iand__ = __iand__;
    var __getitem__ = function (container, key) {
        if (typeof container == 'object' && '__getitem__' in container) {
            return container.__getitem__ (key);
        }
        else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
            return container [container.length + key];
        }
        else {
            return container [key];
        }
    };
    __all__.__getitem__ = __getitem__;
    var __setitem__ = function (container, key, value) {
        if (typeof container == 'object' && '__setitem__' in container) {
            container.__setitem__ (key, value);
        }
        else if ((typeof container == 'string' || container instanceof Array) && key < 0) {
            container [container.length + key] = value;
        }
        else {
            container [key] = value;
        }
    };
    __all__.__setitem__ = __setitem__;
    var __getslice__ = function (container, lower, upper, step) {
        if (typeof container == 'object' && '__getitem__' in container) {
            return container.__getitem__ ([lower, upper, step]);
        }
        else {
            return container.__getslice__ (lower, upper, step);
        }
    };
    __all__.__getslice__ = __getslice__;
    var __setslice__ = function (container, lower, upper, step, value) {
        if (typeof container == 'object' && '__setitem__' in container) {
            container.__setitem__ ([lower, upper, step], value);
        }
        else {
            container.__setslice__ (lower, upper, step, value);
        }
    };
    __all__.__setslice__ = __setslice__;
	__nest__ (
		__all__,
		'click_process', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'click_process';
					var corect_href = __init__ (__world__.tools).corect_href;
					var ajax_get = __init__ (__world__.tools).ajax_get;
					var mount_html = __init__ (__world__.tools).mount_html;
					var refresh_fragment = __init__ (__world__.popup).refresh_fragment;
					var get_menu = __init__ (__world__.tabmenu).get_menu;
					var get_value = function (elem, py_name) {
						if (elem.length > 0) {
							var x = elem.closest ('.refr_object');
							if (x.length > 0) {
								var x2 = x.find (sprintf ("[name='%s']", py_name));
								if (x2.length > 0) {
									return x2.val ();
								}
							}
						}
						return '[[ERROR]]';
					};
					var process_href = function (href, elem) {
						var ret = list ([]);
						if (__in__ ('[[', href) && __in__ (']]', href)) {
							var x1 = href.py_split ('[[');
							var process = false;
							var __iterable0__ = x1;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (process) {
									if (__in__ (']]', pos)) {
										var x2 = pos.py_split (']]', 1);
										var value = get_value (elem, x2 [0]);
										if (value && value != 'None') {
											ret.append (value + x2 [1]);
										}
										else {
											ret.append (x2 [1]);
										}
									}
									else {
										ret.append (pos);
									}
									var process = false;
								}
								else {
									ret.append (pos);
									var process = true;
								}
							}
							return ''.join (ret);
						}
						else {
							return href;
						}
					};
					var process_on_click = function (event_tab, elem) {
						if (typeof elem == 'undefined' || (elem != null && elem .hasOwnProperty ("__kwargtrans__"))) {;
							var elem = null;
						};
						var _on_click = function (e) {
							var target = jQuery (e.currentTarget).attr ('target');
							if (target == '_blank' || target == '_parent') {
								return true;
							}
							var src_obj = jQuery (this);
							if (__in__ ('xlink:href', e.currentTarget.attributes)) {
								var href = jQuery (this).attr ('xlink:href');
							}
							else {
								var href = jQuery (this).attr ('href');
							}
							if (href && __in__ ('#', href)) {
								return true;
							}
							if (!(href)) {
								return true;
							}
							var href = process_href (href, src_obj);
							var __iterable0__ = event_tab;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (pos [0] == '*' || pos [0] == target) {
									if (pos [1] == '*' || src_obj.hasClass (pos [1])) {
										if (pos [3]) {
											var url = corect_href (href, true);
										}
										else if (pos [2]) {
											var url = corect_href (href, false);
										}
										else {
											var url = href;
										}
										e.preventDefault ();
										pos [4] (url, this, e);
										return true;
									}
								}
							}
							e.preventDefault ();
							var href2 = corect_href (href);
							var _on_data = function (data) {
								if (data && __in__ ('_parent_refr', data) || __in__ (target, tuple (['refresh_obj', 'refresh_page']))) {
									if (target == 'refresh_obj') {
										if (!(refresh_fragment (src_obj, null, true))) {
											refresh_fragment (src_obj);
										}
									}
									else {
										refresh_fragment (src_obj);
									}
								}
								else {
									if (window.APPLICATION_TEMPLATE == 'modern') {
										if (window.ACTIVE_PAGE) {
											mount_html (window.ACTIVE_PAGE.page, data);
										}
										else {
											mount_html (jQuery ('#wiki_start'), data);
											return ;
										}
										window.ACTIVE_PAGE.set_href (href);
									}
									else {
										mount_html (jQuery ('#body_body'), data);
									}
									window.ACTIVE_PAGE.set_href (href);
									get_menu ().get_active_item ().url = href;
									if (window.PUSH_STATE) {
										history_push_state ('title', href);
									}
								}
							};
							ajax_get (href2, _on_data);
						};
						if (elem) {
							elem.on ('click', 'a', _on_click);
						}
						else {
							jQuery ('#tabs2_content').on ('click', 'a', _on_click);
							jQuery ('#dialog-form-modal').on ('click', 'a', _on_click);
							jQuery ('#body_body').on ('click', 'a', _on_click);
							jQuery ('#wiki_start').on ('click', 'a', _on_click);
						}
					};
					__pragma__ ('<use>' +
						'popup' +
						'tabmenu' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.ajax_get = ajax_get;
						__all__.corect_href = corect_href;
						__all__.get_menu = get_menu;
						__all__.get_value = get_value;
						__all__.mount_html = mount_html;
						__all__.process_href = process_href;
						__all__.process_on_click = process_on_click;
						__all__.refresh_fragment = refresh_fragment;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'db', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'db';
					var INIT_DB_STRUCT = null;
					var init_db = function (struct) {
						INIT_DB_STRUCT = struct;
					};
					window.init_db = init_db;
					var open_database = function (on_open) {
						if (!(window.indexedDB)) {
							console.log ('Your Browser does not support IndexedDB');
						}
						else {
							var request = window.indexedDB.open (window.PRJ_NAME, 1);
							var _onerror = function (event) {
								console.log ('Error opening DB', event);
							};
							request.onerror = _onerror;
							var _onupgradeneeded = function (event) {
								console.log ('Upgrading');
								var db = event.target.result;
								var objectStore = db.createObjectStore ('param', dict ({'keyPath': 'key'}));
								if (INIT_DB_STRUCT) {
									var __iterable0__ = INIT_DB_STRUCT;
									for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
										var pos = __iterable0__ [__index0__];
										var objectStore = db.createObjectStore (pos [0], pos [1]);
									}
								}
							};
							request.onupgradeneeded = _onupgradeneeded;
							var _onsuccess = function (event) {
								var db = event.target.result;
								on_open (db);
							};
							request.onsuccess = _onsuccess;
						}
					};
					window.open_database = open_database;
					var get_table = function (table_name, on_open, read_only) {
						if (typeof read_only == 'undefined' || (read_only != null && read_only .hasOwnProperty ("__kwargtrans__"))) {;
							var read_only = true;
						};
						var _on_open = function (db) {
							if (read_only == true) {
								var mode = 'readonly';
							}
							else {
								var mode = 'readwrite';
							}
							var tabTrans = db.transaction (table_name, mode);
							var tabObjectStore = tabTrans.objectStore (table_name);
							on_open (tabTrans, tabObjectStore);
						};
						open_database (_on_open);
					};
					window.get_table = get_table;
					var get_list_from_table = function (table, on_open_list) {
						var on_open = function (trans, table) {
							var py_items = list ([]);
							var oncomplete = function (evt) {
								on_open_list (py_items);
							};
							trans.oncomplete = oncomplete;
							var cursor_request = table.openCursor ();
							var onerror = function (error) {
								console.log (error);
							};
							cursor_request.onerror = onerror;
							var onsuccess = function (evt) {
								var cursor = evt.target.result;
								if (cursor) {
									py_items.push (cursor.value);
									cursor.continue ();
								}
							};
							cursor_request.onsuccess = onsuccess;
						};
						get_table (table, on_open);
					};
					window.get_list_from_table = get_list_from_table;
					var on_sys_sync = function (fun) {
						var _fun = function (cache_deleted) {
							if (cache_deleted) {
								fun ('OK-refresh');
							}
							else {
								fun ('OK-no cache');
							}
						};
						caches.delete ('PYTIGON_' + window.PRJ_NAME).then (_fun);
					};
					var _UA = window.navigator.userAgent;
					var _MSIE = _UA.indexOf ('MSIE ');
					var _MSIE2 = _UA.indexOf ('Trident/');
					if (_MSIE > 0 || _MSIE2 > 0) {
						var SYNC_STRUCT = list ([]);
					}
					else {
						var SYNC_STRUCT = list ([list (['sys', window.BASE_PATH + 'schsys/app_time_stamp/', on_sys_sync])]);
					}
					var init_sync = function (sync_struct) {
						var __iterable0__ = sync_struct;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							SYNC_STRUCT.append (pos);
						}
					};
					window.init_sync = init_sync;
					var sync_and_run = function (tbl, fun) {
						var rec = null;
						var __iterable0__ = SYNC_STRUCT;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							if (pos [0] == tbl) {
								var rec = pos;
								break;
							}
						}
						if (!(rec)) {
							fun ('error - no reg function');
							return ;
						}
						if (navigator.onLine) {
							var complete = function (responseText) {
								var _on_open_param = function (trans, db) {
									var param_get_request = db.get ('time_sync_' + tbl);
									var _on_param_error = function (event) {
										rec [2] (fun);
										db.add (dict ({'key': 'time_sync_' + tbl, 'value': time}));
									};
									var _on_param_success = function (event) {
										var param = param_get_request.result;
										if (param) {
											var time2 = param.value;
											if (time2 < time) {
												param.value = time;
												var param_update_request = db.put (param);
												var _on_update = function (event) {
													rec [2] (fun);
												};
												param_update_request.onerror = _on_update;
												param_update_request.onsuccess = _on_update;
											}
											else {
												fun ('OK');
											}
										}
										else {
											var param_add_request = db.add (dict ({'key': 'time_sync_' + tbl, 'value': time}));
											var _on_add_success = function (event) {
												rec [2] (fun);
											};
											var _on_add_error = function (event) {
												rec [2] (fun);
											};
											param_add_request.onerror = _on_add_error;
											param_add_request.onsuccess = _on_add_success;
										}
									};
									param_get_request.onerror = _on_param_error;
									param_get_request.onsuccess = _on_param_success;
								};
								try {
									var x = JSON.parse (responseText);
									var time = x ['TIME'];
									get_table ('param', _on_open_param, false);
								}
								catch (__except0__) {
									console.log (responseText);
									window.open ().document.write (responseText);
								}
							};
							var _on_request_init = function (request) {
								var _on_timeout = function (event) {
									fun ('timeout');
								};
								try {
									request.timeout = 2000;
								}
								catch (__except0__) {
									// pass;
								}
								request.ontimeout = _on_timeout;
							};
							ajax_get (rec [1], complete, _on_request_init);
						}
						else {
							fun ('offline');
						}
					};
					window.sync_and_run = sync_and_run;
					__pragma__ ('<all>')
						__all__.INIT_DB_STRUCT = INIT_DB_STRUCT;
						__all__.SYNC_STRUCT = SYNC_STRUCT;
						__all__._MSIE = _MSIE;
						__all__._MSIE2 = _MSIE2;
						__all__._UA = _UA;
						__all__.__name__ = __name__;
						__all__.get_list_from_table = get_list_from_table;
						__all__.get_table = get_table;
						__all__.init_db = init_db;
						__all__.init_sync = init_sync;
						__all__.on_sys_sync = on_sys_sync;
						__all__.open_database = open_database;
						__all__.sync_and_run = sync_and_run;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'offline', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'offline';
					var install_service_worker = function () {
						if (hasattr (navigator, 'serviceWorker')) {
							var reg = function (registration) {
								if (registration.installing) {
									var serviceWorker = registration.installing;
								}
								else if (registration.waiting) {
									var serviceWorker = registration.waiting;
								}
								else if (registration.active) {
									var serviceWorker = registration.active;
								}
								if (serviceWorker) {
									console.log (serviceWorker.state);
									var onstatechange = function (e) {
										console.log (e.target.state);
									};
									serviceWorker.addEventListener ('statechange', onstatechange);
								}
							};
							var err = function (error) {
								console.log (error);
							};
							navigator.serviceWorker.register (BASE_PATH + 'sw.js').then (reg).catch (err);
						}
						else {
							console.log ("The current browser doesn't support service workers");
						}
					};
					var service_worker_and_indexedDB_test = function () {
						if (hasattr (navigator, 'serviceWorker') && hasattr (window, 'indexedDB') && (location.hostname == 'localhost' || location.hostname == '127.0.0.1' || location.protocol == 'https:')) {
							return true;
						}
						else {
							return false;
						}
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.install_service_worker = install_service_worker;
						__all__.service_worker_and_indexedDB_test = service_worker_and_indexedDB_test;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'page', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'page';
					var Page = __class__ ('Page', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, id, page) {
							self.id = id;
							self.page = page;
						});},
						get set_href () {return __get__ (this, function (self, href) {
							self.page.attr ('_href', href);
						});},
						get get_href () {return __get__ (this, function (self) {
							return self.page.attr ('_href');
						});}
					});
					__pragma__ ('<all>')
						__all__.Page = Page;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'popup', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'popup';
					var can_popup = __init__ (__world__.tools).can_popup;
					var corect_href = __init__ (__world__.tools).corect_href;
					var ajax_load = __init__ (__world__.tools).ajax_load;
					var ajax_get = __init__ (__world__.tools).ajax_get;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_submit = __init__ (__world__.tools).ajax_submit;
					var handle_class_click = __init__ (__world__.tools).handle_class_click;
					var mount_html = __init__ (__world__.tools).mount_html;
					var get_table_type = __init__ (__world__.tools).get_table_type;
					var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
					var remove_page_from_href = __init__ (__world__.tools).remove_page_from_href;
					var datatable_refresh = __init__ (__world__.tbl).datatable_refresh;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var init_table = __init__ (__world__.tbl).init_table;
					var get_menu = __init__ (__world__.tabmenu).get_menu;
					var refresh_fragment = function (data_item_to_refresh, fun, only_table, data, remove_pagination) {
						if (typeof fun == 'undefined' || (fun != null && fun .hasOwnProperty ("__kwargtrans__"))) {;
							var fun = null;
						};
						if (typeof only_table == 'undefined' || (only_table != null && only_table .hasOwnProperty ("__kwargtrans__"))) {;
							var only_table = false;
						};
						if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
							var data = null;
						};
						if (typeof remove_pagination == 'undefined' || (remove_pagination != null && remove_pagination .hasOwnProperty ("__kwargtrans__"))) {;
							var remove_pagination = false;
						};
						var only_table_href = false;
						var refr_block = data_item_to_refresh.closest ('.refr_object');
						if (refr_block.hasClass ('refr_target')) {
							var target = refr_block;
						}
						else {
							var target = refr_block.find ('.refr_target');
							if (target.length > 1) {
								var target = jQuery (target [0]);
							}
						}
						if (only_table) {
							var datatable = target.find ('table[name=tabsort].datatable');
							if (datatable.length > 0) {
								datatable_refresh (datatable);
								target.find ('.inline_dialog').remove ();
								if (fun) {
									fun ();
								}
								return true;
							}
							var datatable = target.find ('table[name=tabsort].tabsort');
							if (datatable.length > 0) {
								var only_table_href = true;
								target.find ('.inline_dialog').remove ();
								var target = datatable.closest ('div.tableframe');
							}
							else {
								return false;
							}
						}
						if (data) {
							mount_html (target, data);
							if (fun) {
								fun ();
							}
						}
						else {
							if (refr_block.hasClass ('refr_source')) {
								var src = refr_block;
							}
							else {
								var src = refr_block.find ('.refr_source');
							}
							if (src.length > 0) {
								var src = jQuery (src [0]);
								var href = src.attr ('href');
								if (remove_pagination) {
									var href = remove_page_from_href (href);
								}
								if (src.prop ('tagName') == 'FORM') {
									var _refr2 = function (data) {
										mount_html (target, data);
										if (fun) {
											fun ();
										}
									};
									ajax_post (corect_href (href, only_table_href), src.serialize (), _refr2);
								}
								else {
									var _on_load = function (responseText) {
										if (fun) {
											fun ();
										}
									};
									ajax_load (target, corect_href (href, only_table_href), _on_load);
								}
							}
							else if (fun) {
								fun ();
							}
						}
						return true;
					};
					var on_popup_inline = function (url, elem, e) {
						var jelem = jQuery (elem);
						if (jelem.hasClass ('edit')) {
							return on_popup_edit_new (url, elem, e);
						}
						if (jelem.hasClass ('delete')) {
							return on_popup_delete (url, elem, e);
						}
						if (jelem.hasClass ('info')) {
							return on_popup_delete (url, elem, e);
						}
						jelem.attr ('data-style', 'zoom-out');
						jelem.attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery ('body').addClass ('shown_inline_dialog');
						jelem.closest ('table').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<tr class='refr_source refr_object inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'><td colspan='20'>") + INLINE_TABLE_HTML.py_replace ('{{title}}', elem.getAttribute ('title'))) + '</td></tr>');
						new_fragment.insertAfter (jQuery (elem).closest ('tr'));
						var elem2 = new_fragment.find ('.refr_target');
						var _on_load = function (responseText, status, response) {
							new_fragment.removeClass ('hide');
							if (status != 'error') {
								_dialog_loaded (false, elem2);
								on_dialog_load ();
							}
							if (window.WAIT_ICON) {
								window.WAIT_ICON.stop ();
								window.WAIT_ICON = null;
							}
						};
						ajax_load (elem2, href2, _on_load);
						return false;
					};
					var on_popup_in_form = function (elem) {
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery ('body').addClass ('shown_inline_dialog');
						jQuery (elem).closest ('div.Dialog').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<div class='refr_source refr_object inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'>") + INLINE_TABLE_HTML.py_replace ('{{title}}', elem.getAttribute ('title'))) + '</div>');
						new_fragment.insertAfter (jQuery (elem).closest ('div.form-group'));
						var elem2 = new_fragment.find ('.refr_target');
						var _on_load = function (responseText, status, response) {
							jQuery ('#IDIAL_' + id).hide ();
							jQuery ('#IDIAL_' + id).removeClass ('hide');
							jQuery ('#IDIAL_' + id).show ('slow');
							if (status != 'error') {
								_dialog_loaded (false, elem2);
								on_dialog_load ();
							}
							if (window.WAIT_ICON) {
								window.WAIT_ICON.stop ();
								window.WAIT_ICON = null;
							}
						};
						ajax_load (elem2, href2, _on_load);
						return false;
					};
					var on_popup_edit_new = function (url, elem, e) {
						if (e) {
							var target = jQuery (e.currentTarget).attr ('target');
						}
						else {
							var target = 'popup';
						}
						if (url) {
							var href2 = corect_href (url);
						}
						else {
							var href2 = corect_href (jQuery (elem).attr ('href'));
						}
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (can_popup () && !(target == 'inline') && !(jQuery (elem).hasClass ('inline')) && !(jQuery (elem).attr ('name') && __in__ ('_inline', jQuery (elem).attr ('name')))) {
							jQuery ('#ModalLabel').html (jQuery (elem).attr ('title'));
							var elem2 = jQuery ('div.dialog-data');
							elem2.closest ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load = function (responseText, status, response) {
								_dialog_loaded (true, elem2);
								on_dialog_load ();
							};
							ajax_load (elem2, href2, _on_load);
						}
						else {
							jQuery ('body').addClass ('shown_inline_dialog');
							if (window.WAIT_ICON) {
								window.WAIT_ICON.start ();
							}
							if (jQuery (elem).hasClass ('new-row')) {
								var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog tr hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
								var new_position = jQuery (elem).closest ('.refr_object').find ('div.new_row');
								if (new_position.length > 0) {
									elem2.insertAfter (jQuery (new_position [0]));
								}
								else {
									elem2.insertAfter (jQuery (elem).closest ('div.tr'));
								}
							}
							else {
								var in_table = false;
								var __iterable0__ = list ([jQuery (elem).parent (), jQuery (elem).parent ().parent ()]);
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var obj = __iterable0__ [__index0__];
									var __iterable1__ = list (['td_action', 'td_information']);
									for (var __index1__ = 0; __index1__ < len (__iterable1__); __index1__++) {
										var c = __iterable1__ [__index1__];
										if (obj.hasClass (c)) {
											var in_table = true;
											break;
										}
									}
								}
								if (in_table) {
									var elem2 = jQuery ((sprintf ("<tr class='refr_source refr_object inline_dialog hide' href='%s'><td colspan='20'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</td></tr>');
									elem2.insertAfter (jQuery (elem).closest ('tr'));
								}
								else {
									var test = jQuery (elem).closest ('form');
									if (test.length > 0) {
										var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
										elem2.insertAfter (jQuery (elem).closest ('div.form-group'));
									}
									else {
										var elem2 = jQuery ((sprintf ("<div class='refr_source refr_object inline_dialog tr hide' href='%s'>", href2) + INLINE_DIALOG_UPDATE_HTML) + '</div>');
										var new_position = jQuery (elem).closest ('.refr_object').find ('div.new_row');
										if (new_position.length > 0) {
											elem2.insertAfter (jQuery (new_position [0]));
										}
										else {
											elem2.insertAfter (jQuery (elem).closest ('div.tr'));
										}
									}
								}
							}
							mount_html (elem2.find ('.modal-title'), jQuery (elem).attr ('title'), false, false);
							elem2.attr ('related-object', jQuery (elem).uid ());
							var elem3 = elem2.find ('div.dialog-data-inner');
							var _on_load2 = function (responseText, status, response) {
								elem2.hide ();
								elem2.removeClass ('hide');
								elem2.show ('slow');
								if (status != 'error') {
									_dialog_loaded (false, elem3);
									on_dialog_load ();
								}
								if (window.WAIT_ICON) {
									window.WAIT_ICON.stop ();
									window.WAIT_ICON = null;
								}
							};
							ajax_load (elem3, href2, _on_load2);
						}
						return false;
					};
					window.on_popup_edit_new = on_popup_edit_new;
					var on_popup_info = function (url, elem, e) {
						if (can_popup ()) {
							var _on_load = function (responseText, status, response) {
								jQuery ('div.dialog-form-info').modal ();
							};
							ajax_load (jQuery ('div.dialog-data-info'), jQuery (elem).attr ('href'), _on_load);
						}
						else {
							jQuery ('.inline_dialog').remove ();
							jQuery (("<tr class='refr_object inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML) + '</td></tr>').insertAfter (jQuery (elem).parents ('tr'));
							var _on_load2 = function (responseText, status, response) {
								// pass;
							};
							ajax_load (jQuery ('div.dialog-data-inner'), jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_popup_delete = function (url, elem, e) {
						if (can_popup ()) {
							jQuery ('div.dialog-data-delete').closest ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load = function (responseText, status, response) {
								jQuery ('div.dialog-form-delete').modal ();
								jQuery ('div.dialog-form-delete').fadeTo ('fast', 1);
							};
							ajax_load (jQuery ('div.dialog-data-delete'), jQuery (elem).attr ('href'), _on_load);
						}
						else {
							jQuery ('.inline_dialog').remove ();
							var elem2 = jQuery (("<tr class='refr_object inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML) + '</td></tr>');
							elem2.insertAfter (jQuery (elem).parents ('tr'));
							elem2.find ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load2 = function () {
								// pass;
							};
							ajax_load (jQuery ('div.dialog-data-inner'), jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_dialog_load = function () {
						// pass;
					};
					var _dialog_loaded = function (is_modal, elem) {
						var obj = elem.closest ('.refr_object');
						if (obj.length > 0) {
							if (obj [0].hasAttribute ('related-object')) {
								var btn = jQuery ('#' + obj.attr ('related-object'));
							}
							else {
								var btn = obj;
							}
							if (btn.hasClass ('no_cancel')) {
								obj.find ('.btn_cancel').hide ();
								obj.find ('.close').hide ();
							}
							else {
								obj.find ('.btn_cancel').show ();
								obj.find ('.close').show ();
							}
							if (btn.hasClass ('no_close')) {
								obj.find ('.close').hide ();
							}
							else {
								obj.find ('.close').show ();
							}
							if (btn.hasClass ('no_ok')) {
								obj.find ('.btn_ok').hide ();
							}
							else {
								obj.find ('.btn_ok').show ();
							}
						}
						if (is_modal) {
							jQuery ('div.dialog-form').fadeTo ('fast', 1);
							jQuery ('div.dialog-form').find ('.modal-dialog').removeClass ('modal-lg').removeClass ('modal-sm');
							var x = jQuery ('div.dialog-form').find ('div[name=modal-type-ref]');
							if (x.length > 0) {
								jQuery ('div.dialog-form').find ('.modal-dialog').addClass (x.attr ('class'));
							}
							jQuery ('div.dialog-form').modal ();
							jQuery ('div.dialog-form').drags (dict ({'handle': '.modal-header'}));
						}
					};
					var _refresh_win = function (responseText, ok_button) {
						var refr_obj = jQuery (ok_button).closest ('.refr_object');
						var popup_activator = jQuery ('#' + refr_obj.attr ('related-object'));
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							if (refr_obj.hasClass ('modal')) {
								if (jQuery ('div.dialog-form').hasClass ('show')) {
									var dialog = 'div.dialog-form';
								}
								else if (jQuery ('div.dialog-form-delete').hasClass ('show')) {
									var dialog = 'div.dialog-form-delete';
								}
								else {
									var dialog = 'div.dialog-form-info';
								}
								var hide_dialog_form = function () {
									jQuery (dialog).modal ('hide');
								};
								jQuery (dialog).fadeTo ('slow', 0.5);
								if (!(refresh_fragment (popup_activator, hide_dialog_form, true))) {
									refresh_fragment (popup_activator, hide_dialog_form, false);
								}
							}
							else {
								if (refr_obj.hasClass ('inline_dialog')) {
									var inline_dialog = refr_obj;
								}
								else {
									var inline_dialog = refr_obj.find ('.inline_dialog');
								}
								if (inline_dialog.length > 0) {
									inline_dialog.remove ();
								}
								if (!(refresh_fragment (popup_activator, null, true))) {
									return refresh_fragment (popup_activator, null, false);
								}
							}
						}
						else if (refr_obj.hasClass ('modal')) {
							mount_html (jQuery ('div.dialog-data'), responseText);
						}
						else {
							mount_html (ok_button.closest ('.refr_target'), responseText);
						}
					};
					var _refresh_win_and_ret = function (responseText, ok_button) {
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							var related_object = jQuery (ok_button).closest ('.refr_object').attr ('related-object');
							var popup_activator = jQuery ('#' + related_object);
							if (jQuery (ok_button).closest ('.refr_object').hasClass ('show')) {
								jQuery ('div.dialog-form').modal ('hide');
							}
							else {
								jQuery (ok_button).closest ('.refr_object').remove ();
							}
							if (popup_activator && popup_activator.data ('edit_ret_function')) {
								window.RET_CONTROL = popup_activator.data ('ret_control');
								window.EDIT_RET_FUNCTION = popup_activator.data ('edit_ret_function');
								var q = jQuery (('<div>' + responseText) + '</div>').find ('script');
								eval (q.text ());
							}
						}
						else {
							mount_html (jQuery ('div.dialog-data'), responseText);
						}
					};
					var _refresh_win_after_ok = function (responseText, ok_button) {
						var related_object = jQuery (ok_button).closest ('.refr_object').attr ('related-object');
						var popup_activator = jQuery ('#' + related_object);
						if (popup_activator && popup_activator.data ('edit_ret_function')) {
							window.EDIT_RET_FUNCTION = popup_activator.data ('edit_ret_function');
							window.EDIT_RET_FUNCTION (responseText, ok_button);
							window.EDIT_RET_FUNCTION = false;
						}
						else {
							_refresh_win (responseText, ok_button);
						}
					};
					var on_edit_ok = function (button, form) {
						if (form) {
							var f = form;
						}
						else {
							var f = jQuery (button).parent ().parent ().find ('form:first');
						}
						var _fun = function (data) {
							_refresh_win_after_ok (data, f);
						};
						if (f.length > 0) {
							ajax_submit (f, _fun);
						}
						else {
							_refresh_win ('RETURN_OK', jQuery (button));
						}
						return false;
					};
					window.on_edit_ok = on_edit_ok;
					var on_delete_ok = function (form) {
						var _on_data = function (data) {
							_refresh_win (data, form);
						};
						ajax_post (corect_href (form.attr ('action')), form.serialize (), _on_data);
						return false;
					};
					window.on_delete_ok = on_delete_ok;
					var on_cancel_inline = function (elem) {
						var refr = false;
						var inline_dialog = jQuery (elem).closest ('.inline_dialog');
						if (inline_dialog.length > 0) {
							var test = inline_dialog.find ('.refresh_after_close');
							if (test.length > 0) {
								var refr = true;
							}
						}
						jQuery ('body').removeClass ('shown_inline_dialog');
						if (refr) {
							_refresh_win ('RETURN_OK', inline_dialog.parent ());
						}
						else {
							inline_dialog.remove ();
							datatable_onresize ();
						}
					};
					window.on_cancel_inline = on_cancel_inline;
					var ret_ok = function (id, title) {
						var text = title;
						var ret_control = window.RET_CONTROL;
						if (ret_control.find (("option[value='" + id) + "']").length == 0) {
							ret_control.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
						}
						ret_control.val (id.toString ());
						ret_control.trigger ('change');
					};
					var on_get_tbl_value = function (url, elem, e) {
						on_popup_in_form (elem);
					};
					var on_new_tbl_value = function (url, elem, e) {
						window.EDIT_RET_FUNCTION = _refresh_win_and_ret;
						window.RET_CONTROL = jQuery (elem).closest ('.input-group').find ('.django-select2');
						jQuery (elem).data ('edit_ret_function', window.EDIT_RET_FUNCTION);
						jQuery (elem).data ('ret_control', window.RET_CONTROL);
						return on_popup_edit_new (url, elem, e);
					};
					var on_get_row = function (url, elem, e) {
						var id = jQuery (elem).attr ('data-id');
						var text = jQuery (elem).attr ('data-text');
						var ret_control = jQuery (elem).closest ('.refr_source').prev ('.form-group').find ('.django-select2');
						if (ret_control.find (("option[value='" + id) + "']").length == 0) {
							ret_control.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
						}
						ret_control.val (id.toString ());
						ret_control.trigger ('change');
						jQuery (elem).closest ('.refr_source').remove ();
					};
					var _init_subforms = function (elem) {
						var subforms = elem.find ('.subform_frame');
						var _load_subform = function (index, obj) {
							var content = jQuery (this).find ('.subform_content');
							if (content.length > 0) {
								var href = jQuery (this).attr ('href');
								var _finish = function () {
									// pass;
								};
								ajax_load (content, corect_href (href), _finish);
							}
						};
						subforms.each (_load_subform);
					};
					register_fragment_init_fun (_init_subforms);
					var refresh_current_object = function (url, elem, e) {
						var href = url;
						var href2 = corect_href (url);
						var target = 'refresh_obj';
						var src_obj = jQuery (elem);
						var refr_block = src_obj.closest ('.refr_object');
						if (refr_block.hasClass ('refr_source')) {
							var src = refr_block;
						}
						else {
							var src = refr_block.find ('.refr_source');
						}
						if (src.length > 0) {
							src.attr ('href', href2);
							src.attr ('action', href2);
						}
						var _on_data = function (data) {
							if (data && __in__ ('_parent_refr', data) || __in__ (target, tuple (['refresh_obj', 'refresh_page']))) {
								if (target == 'refresh_obj') {
									if (__in__ ('only_table', href)) {
										if (!(refresh_fragment (src_obj, null, true, data))) {
											refresh_fragment (src_obj, null, false, data);
										}
									}
									else {
										refresh_fragment (src_obj, null, false, data);
									}
								}
								else {
									refresh_fragment (src_obj, null, false, data);
								}
							}
							else {
								if (window.APPLICATION_TEMPLATE == 'modern') {
									mount_html (window.ACTIVE_PAGE.page, data);
									window.ACTIVE_PAGE.set_href (href);
								}
								else {
									mount_html (jQuery ('#body_body'), data);
								}
								window.ACTIVE_PAGE.set_href (href);
								get_menu ().get_active_item ().url = href;
								if (window.PUSH_STATE) {
									history_push_state ('title', href);
								}
							}
						};
						if (src_obj.hasClass ('page-link')) {
							ajax_submit (src, _on_data);
						}
						else {
							ajax_get (href2, _on_data);
						}
					};
					var refresh_current_page = function (url, elem, e) {
						// pass;
					};
					var refresh_current_app = function (url, elem, e) {
						// pass;
					};
					var _none = function () {
						// pass;
					};
					var only_get = function (url, elem, e) {
						var href = url;
						var href2 = corect_href (url);
						var target = 'refresh_obj';
						var src_obj = jQuery (elem);
						var refr_block = src_obj.closest ('.refr_object');
						if (refr_block.hasClass ('refr_source')) {
							var src = refr_block;
						}
						else {
							var src = refr_block.find ('.refr_source');
						}
						if (src.length > 0) {
							src.attr ('href', href2);
							src.attr ('action', href2);
						}
						var _on_data = function (data) {
							if (data && __in__ ('_parent_refr', data) && __in__ ('YES', data) || __in__ ('OK', data)) {
								if (!(refresh_fragment (jQuery (elem), null, true))) {
									return refresh_fragment (jQuery (elem), null, false);
								}
							}
						};
						if (src_obj.hasClass ('page-link')) {
							ajax_submit (src, _on_data);
						}
						else {
							ajax_get (href2, _on_data);
						}
					};
					var popup_min_max = function (elm, max) {
						if (typeof max == 'undefined' || (max != null && max .hasOwnProperty ("__kwargtrans__"))) {;
							var max = true;
						};
						var elem = jQuery (elm);
						if (elem.hasClass ('modal-dialog')) {
							var popup = elem;
						}
						else {
							var popup = elem.closest ('.modal-dialog');
						}
						if (popup.length > 0) {
							var minimize = popup.find ('.minimize');
							var maximize = popup.find ('.maximize');
							if (minimize.length > 0) {
								if (max) {
									minimize.show ();
								}
								else {
									minimize.hide ();
								}
							}
							if (maximize.length > 0) {
								if (max) {
									maximize.hide ();
								}
								else {
									maximize.show ();
								}
							}
							if (max) {
								popup.addClass ('modal-fullscreen');
								popup.addClass ('modal-open');
							}
							else {
								popup.removeClass ('modal-fullscreen');
								popup.removeClass ('modal-open');
							}
							jQuery (window).trigger ('resize');
						}
					};
					var popup_minimize = function (elem) {
						return popup_min_max (elem, false);
					};
					window.popup_minimize = popup_minimize;
					var popup_maximize = function (elem) {
						return popup_min_max (elem, true);
					};
					window.popup_maximize = popup_maximize;
					jQuery.fn.modal.Constructor.prototype.enforceFocus = _none;
					__pragma__ ('<use>' +
						'tabmenu' +
						'tbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__._dialog_loaded = _dialog_loaded;
						__all__._init_subforms = _init_subforms;
						__all__._none = _none;
						__all__._refresh_win = _refresh_win;
						__all__._refresh_win_after_ok = _refresh_win_after_ok;
						__all__._refresh_win_and_ret = _refresh_win_and_ret;
						__all__.ajax_get = ajax_get;
						__all__.ajax_load = ajax_load;
						__all__.ajax_post = ajax_post;
						__all__.ajax_submit = ajax_submit;
						__all__.can_popup = can_popup;
						__all__.corect_href = corect_href;
						__all__.datatable_onresize = datatable_onresize;
						__all__.datatable_refresh = datatable_refresh;
						__all__.get_menu = get_menu;
						__all__.get_table_type = get_table_type;
						__all__.handle_class_click = handle_class_click;
						__all__.init_table = init_table;
						__all__.mount_html = mount_html;
						__all__.on_cancel_inline = on_cancel_inline;
						__all__.on_delete_ok = on_delete_ok;
						__all__.on_dialog_load = on_dialog_load;
						__all__.on_edit_ok = on_edit_ok;
						__all__.on_get_row = on_get_row;
						__all__.on_get_tbl_value = on_get_tbl_value;
						__all__.on_new_tbl_value = on_new_tbl_value;
						__all__.on_popup_delete = on_popup_delete;
						__all__.on_popup_edit_new = on_popup_edit_new;
						__all__.on_popup_in_form = on_popup_in_form;
						__all__.on_popup_info = on_popup_info;
						__all__.on_popup_inline = on_popup_inline;
						__all__.only_get = only_get;
						__all__.popup_maximize = popup_maximize;
						__all__.popup_min_max = popup_min_max;
						__all__.popup_minimize = popup_minimize;
						__all__.refresh_current_app = refresh_current_app;
						__all__.refresh_current_object = refresh_current_object;
						__all__.refresh_current_page = refresh_current_page;
						__all__.refresh_fragment = refresh_fragment;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
						__all__.remove_page_from_href = remove_page_from_href;
						__all__.ret_ok = ret_ok;
					__pragma__ ('</all>')
				}
			}
		}
	);
	__nest__ (
		__all__,
		'tabmenu', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tabmenu';
					var Page = __init__ (__world__.page).Page;
					var TabMenuItem = __init__ (__world__.tabmenuitem).TabMenuItem;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var history_push_state = __init__ (__world__.tools).history_push_state;
					var mount_html = __init__ (__world__.tools).mount_html;
					var TabMenu = __class__ ('TabMenu', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.id = 0;
							self.titles = dict ({});
							self.active_item = null;
						});},
						get get_active_item () {return __get__ (this, function (self) {
							return self.active_item;
						});},
						get is_open () {return __get__ (this, function (self, title) {
							if (self.titles && __in__ (title, self.titles) && self.titles [title]) {
								return true;
							}
							else {
								return false;
							}
						});},
						get activate () {return __get__ (this, function (self, title, push_state) {
							if (typeof push_state == 'undefined' || (push_state != null && push_state .hasOwnProperty ("__kwargtrans__"))) {;
								var push_state = true;
							};
							var menu_item = self.titles [title];
							jQuery (sprintf ('#li_%s a', menu_item.id)).tab ('show');
							if (push_state && window.PUSH_STATE) {
								history_push_state (menu_item.title, menu_item.url);
							}
							datatable_onresize ();
						});},
						get new_page () {return __get__ (this, function (self, title_alternate, data, href) {
							var _id = 'tab' + self.id;
							var tmp = jQuery (data).find ('header').find ('title').text ();
							var title = jQuery.trim (tmp);
							if (!(title)) {
								var title = title_alternate;
							}
							var title2 = jQuery.trim (title);
							var menu_item = TabMenuItem (_id, title2, href, data);
							self.titles [title2] = menu_item;
							var menu_pos = vsprintf ("<li id='li_%s' class ='nav-item'><a href='#%s' class='nav-link bg-info' data-toggle='tab' role='tab' title='%s'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-outline-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", list ([_id, _id, title2, title2, _id]));
							var append_left = jQuery ('#tabs2').hasClass ('append-left');
							if (append_left) {
								jQuery ('#tabs2').prepend (menu_pos);
							}
							else {
								jQuery ('#tabs2').append (menu_pos);
							}
							jQuery ('#tabs2_content').append (sprintf ("<div class='tab-pane container-fluid refr_target refr_object win-content page' id='%s'></div>", _id));
							window.ACTIVE_PAGE = Page (_id, jQuery ('#' + _id));
							self.active_item = menu_item;
							if (window.PUSH_STATE) {
								history_push_state (title2, href);
							}
							var _on_show_tab = function (e) {
								window.ACTIVE_PAGE = Page (_id, jQuery ('#' + _id), menu_item);
								var menu = get_menu ();
								menu_item = menu.titles [jQuery.trim (e.target.text)];
								self.active_item = menu_item;
								if (window.PUSH_STATE) {
									history_push_state (menu_item.title, menu_item.url);
								}
							};
							if (append_left) {
								jQuery ('#tabs2 a:first').on ('shown.bs.tab', _on_show_tab);
								jQuery ('#tabs2 a:first').tab ('show');
							}
							else {
								jQuery ('#tabs2 a:last').on ('shown.bs.tab', _on_show_tab);
								jQuery ('#tabs2 a:last').tab ('show');
							}
							mount_html (jQuery ('#' + _id), data);
							var _on_button_click = function (event) {
								get_menu ().remove_page (jQuery (this).attr ('id').py_replace ('button_', ''));
							};
							jQuery (sprintf ('#button_%s', _id)).click (_on_button_click);
							var scripts = jQuery (('#' + _id) + ' script');
							var _local_fun = function (index, element) {
								eval (this.innerHTML);
							};
							scripts.each (_local_fun);
							self.id++;
							return _id;
						});},
						get remove_page () {return __get__ (this, function (self, id) {
							var _on_remove = function (index, value) {
								value.on_remove ();
							};
							jQuery.each (jQuery ('#' + id).find ('.call_on_remove'), _on_remove);
							var _local_fun = function (index, value) {
								if (value && value.id == id) {
									self.titles [index] = null;
								}
							};
							jQuery.each (self.titles, _local_fun);
							jQuery (sprintf ('#li_%s', id)).remove ();
							jQuery (sprintf ('#%s', id)).remove ();
							var last_a = jQuery ('#tabs2 a:last');
							if (last_a.length > 0) {
								last_a.tab ('show');
							}
							else {
								window.ACTIVE_PAGE = null;
								if (window.PUSH_STATE) {
									history_push_state ('', window.BASE_PATH);
								}
								if (jQuery ('#wiki_start').find ('.content').length == 0) {
									window.init_start_wiki_page ();
								}
								jQuery ('#wiki_start').show ();
							}
						});}
					});
					var get_menu = function () {
						if (!(window.MENU)) {
							window.MENU = TabMenu ();
						}
						return window.MENU;
					};
					__pragma__ ('<use>' +
						'page' +
						'tabmenuitem' +
						'tbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.Page = Page;
						__all__.TabMenu = TabMenu;
						__all__.TabMenuItem = TabMenuItem;
						__all__.__name__ = __name__;
						__all__.datatable_onresize = datatable_onresize;
						__all__.get_menu = get_menu;
						__all__.history_push_state = history_push_state;
						__all__.mount_html = mount_html;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'tabmenuitem', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tabmenuitem';
					var TabMenuItem = __class__ ('TabMenuItem', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, id, title, url, data) {
							if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
								var data = null;
							};
							self.id = id;
							self.title = jQuery.trim (title);
							self.url = url;
							self.data = data;
						});}
					});
					__pragma__ ('<all>')
						__all__.TabMenuItem = TabMenuItem;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'tbl', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tbl';
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
					var get_table_type = __init__ (__world__.tools).get_table_type;
					var load_js = __init__ (__world__.tools).load_js;
					var mount_html = __init__ (__world__.tools).mount_html;
					var datetable_set_height = function () {
						if (jQuery (this).hasClass ('table_get')) {
							return ;
						}
						if (!(jQuery (this).is (':visible'))) {
							return ;
						}
						var elem = jQuery (this).closest ('.tabsort_panel');
						var table_offset = elem.offset ().top;
						var dy_win = jQuery (window).height ();
						var dy = dy_win - table_offset;
						if (dy < 200) {
							var dy = 200;
						}
						var panel = elem.find ('.fixed-table-toolbar');
						if (!(panel.is (':visible'))) {
							dy += panel.height () - 15;
						}
						jQuery (this).bootstrapTable ('resetView', dict ({'height': dy - 5}));
					};
					var datatable_refresh = function (table) {
						table.bootstrapTable ('refresh');
					};
					var _rowStyle = function (value, row, index) {
						var x = jQuery (('<div>' + value ['cid']) + '</div>').find ('div.td_information');
						if (x.length > 0) {
							var c = x.attr ('class').py_replace ('td_information', '');
							if (c.length > 0) {
								return dict ({'classes': c});
							}
						}
						return dict ({});
					};
					var prepare_datatable = function (table) {
						var _local_fun = function (index) {
							var td = jQuery (this).parent ();
							var tr = td.parent ();
							var l = tr.find ('td').length;
							tr.find ('td:gt(0)').remove ();
							td.attr ('colspan', l);
						};
						table.find ('div.second_row').each (_local_fun);
					};
					var datatable_ajax = function (params) {
						var url = params ['url'];
						var success = params ['success'];
						if (__in__ ('form', dict (params ['data']))) {
							var form = params ['data'] ['form'];
							delete params ['data'] ['form'];
							var d = jQuery.param (params ['data']);
							url += '?' + d;
							var _on_post_data = function (data) {
								var d2 = JSON.parse (data);
								success (d2);
							};
							ajax_post (url, form, _on_post_data);
						}
						else {
							var d = jQuery.param (params ['data']);
							url += '?' + d;
							var _on_get_data = function (data) {
								var d2 = JSON.parse (data);
								success (d2);
							};
							ajax_get (url, _on_get_data);
						}
					};
					var init_table = function (table, table_type) {
						if (table_type == 'datatable') {
							var onLoadSuccess = function (data) {
								prepare_datatable (table);
								var _pagination = function () {
									jQuery (table).closest ('.fixed-table-container').find ('.fixed-table-pagination ul.pagination a').addClass ('page-link');
									datatable_onresize ();
								};
								setTimeout (_pagination, 0);
								return false;
							};
							var queryParams = function (p) {
								var refr_block = jQuery (table).closest ('.refr_object');
								var src = refr_block.find ('.refr_source');
								if (src.length > 0 && src.prop ('tagName') == 'FORM') {
									p ['form'] = src.serialize ();
								}
								return p;
							};
							if (table.hasClass ('table_get')) {
								table.bootstrapTable (dict ({'onLoadSuccess': onLoadSuccess, 'height': 350, 'rowStyle': _rowStyle, 'queryParams': queryParams, 'ajax': datatable_ajax}));
							}
							else {
								table.bootstrapTable (dict ({'onLoadSuccess': onLoadSuccess, 'rowStyle': _rowStyle, 'queryParams': queryParams, 'ajax': datatable_ajax}));
							}
							var table_panel = jQuery (table).closest ('.content');
							var btn = table_panel.find ('.tabsort-toolbar-expand');
							if (btn) {
								var _handle_toolbar_expand = function (elem) {
									var panel = table_panel.find ('.fixed-table-toolbar');
									if (jQuery (this).hasClass ('active')) {
										panel.show ();
										datatable_onresize ();
									}
									else {
										panel.hide ();
										datatable_onresize ();
									}
								};
								table_panel.on ('click', '.tabsort-toolbar-expand', _handle_toolbar_expand);
								if (btn.hasClass ('active')) {
									var panel = table_panel.find ('.fixed-table-toolbar');
									panel.hide ();
									datatable_onresize ();
								}
							}
						}
					};
					var content_set_height = function () {
						if (!(jQuery (this).is (':visible'))) {
							return ;
						}
						if (jQuery (this).closest ('.tabsort').length > 0) {
							return ;
						}
						if (jQuery (this).closest ('#dialog-form-modal').length > 0) {
							return ;
						}
						var content_offset = jQuery (this).offset ().top;
						var dy_win = jQuery (window).height ();
						var dy = (dy_win - content_offset) - 30;
						if (dy < 200) {
							var dy = 200;
						}
						jQuery (this).height (dy);
					};
					var datatable_onresize = function () {
						jQuery ('.datatable:not(.table_get)').each (datetable_set_height);
						jQuery ('.content').each (content_set_height);
					};
					window.datatable_onresize = datatable_onresize;
					var _on_fragment_init = function (elem) {
						datatable_onresize ();
						var table_type = get_table_type (elem);
						var tbl = elem.find ('.tabsort');
						if (tbl.length > 0) {
							init_table (tbl, table_type);
						}
					};
					register_fragment_init_fun (_on_fragment_init);
					__pragma__ ('<use>' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__._on_fragment_init = _on_fragment_init;
						__all__._rowStyle = _rowStyle;
						__all__.ajax_post = ajax_post;
						__all__.content_set_height = content_set_height;
						__all__.datatable_ajax = datatable_ajax;
						__all__.datatable_onresize = datatable_onresize;
						__all__.datatable_refresh = datatable_refresh;
						__all__.datetable_set_height = datetable_set_height;
						__all__.get_table_type = get_table_type;
						__all__.init_table = init_table;
						__all__.load_js = load_js;
						__all__.mount_html = mount_html;
						__all__.prepare_datatable = prepare_datatable;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'tools', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'tools';
					var LOADED_FILES = dict ({});
					var FIRST_INIT = true;
					var FRAGMENT_INIT_FUN = list ([]);
					var register_fragment_init_fun = function (fun) {
						FRAGMENT_INIT_FUN.append (fun);
					};
					var fragment_init = function (elem) {
						if (typeof elem == 'undefined' || (elem != null && elem .hasOwnProperty ("__kwargtrans__"))) {;
							var elem = null;
						};
						if (elem) {
							var elem2 = elem;
						}
						else {
							var elem2 = window.ACTIVE_PAGE.page;
						}
						var format = dict ({'singleDatePicker': true, 'showDropdowns': true, 'buttonClasses': 'btn', 'applyClass': 'btn-success align-top', 'cancelClass': 'btn-danger btn-sm align-top', 'timePicker24Hour': true, 'autoApply': true, 'locale': dict ({'format': 'YYYY-MM-DD', 'separator': '-', 'applyLabel': '&nbsp; OK &nbsp;', 'cancelLabel': "<i class='fa fa-close'></i>"})});
						var d = elem2.find ('div.form-group .datefield input');
						d.daterangepicker (format);
						format ['locale'] ['format'] = 'YYYY-MM-DD HH:mm';
						format ['timePicker'] = true;
						format ['timePickerIncrement'] = 30;
						var d = elem2.find ('div.form-group .datetimefield input');
						d.daterangepicker (format);
						jQuery ('.selectpicker').selectpicker ();
						var _on_blur = function (e) {
							if (e ['type'] == 'focus' || this.value.length > 0) {
								var test = true;
							}
							else {
								var test = false;
							}
							jQuery (this).parents ('.form-group').toggleClass ('focused', test);
						};
						elem2.find ('.label-floating .form-control').on ('focus blur', _on_blur).trigger ('blur');
						var load_inline_frame = function () {
							var frame = jQuery (this);
							frame.append (INLINE_FRAME_HTML);
							var obj2 = frame.find ('div.frame-data-inner');
							if (obj2.length > 0) {
								var url = frame.attr ('href');
								var complete = function (txt) {
									// pass;
								};
								ajax_load (obj2, url, complete);
							}
						};
						elem2.find ('.inline_frame').each (load_inline_frame);
						elem2.find ('.django-select2:not(.select2-full-width)').djangoSelect2 (dict ({'width': 'calc(100% - 48px)'}));
						elem2.find ('.django-select2.select2-full-width').djangoSelect2 (dict ({'width': 'calc(100%)'}));
						var init_select2_ctrl = function () {
							var sel2 = jQuery (this);
							var src = sel2.closest ('.input-group');
							if (src.length == 1) {
								if (src [0].hasAttribute ('item_id')) {
									var id = src.attr ('item_id');
									if (id) {
										var text = src.attr ('item_str');
										sel2.append (jQuery ('<option>', dict ({'value': id, 'text': text})));
										sel2.val (id.toString ());
										sel2.trigger ('change');
									}
								}
							}
						};
						elem2.find ('.django-select2').each (init_select2_ctrl);
						if (window.BASE_FRAGMENT_INIT) {
							window.BASE_FRAGMENT_INIT ();
						}
						var __iterable0__ = FRAGMENT_INIT_FUN;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var fun = __iterable0__ [__index0__];
							fun (elem2);
						}
					};
					var evalJSFromHtml = function (html) {
						var newElement = document.createElement ('div');
						newElement.innerHTML = html;
						var scripts = newElement.getElementsByTagName ('script');
						var eval_fun = function (id, value) {
							eval (value.innerHTML);
						};
						jQuery.each (scripts, eval_fun);
					};
					var evalCSSFromHtml = function (html, elem) {
						var newElement = document.createElement ('div');
						newElement.innerHTML = html;
						var css = newElement.getElementsByTagName ('style');
						while (css.length > 0) {
							var style = css.py_pop ();
							style.attr ('scoped', 'scoped');
							elem.append (style);
						}
					};
					var MOUNT_INIT_FUN = list ([]);
					var register_mount_fun = function (fun) {
						MOUNT_INIT_FUN.append (fun);
					};
					var mount_html = function (elem, html_txt, run_fragment_init, component_init) {
						if (typeof run_fragment_init == 'undefined' || (run_fragment_init != null && run_fragment_init .hasOwnProperty ("__kwargtrans__"))) {;
							var run_fragment_init = true;
						};
						if (typeof component_init == 'undefined' || (component_init != null && component_init .hasOwnProperty ("__kwargtrans__"))) {;
							var component_init = true;
						};
						if (component_init && window.COMPONENT_INIT && len (window.COMPONENT_INIT) > 0) {
							try {
								elem.empty ();
								var res = Vue.compile (('<div>' + html_txt) + '</div>');
								if (elem && elem.length > 0) {
									var vm = new Vue (dict ({'render': res.render, 'staticRenderFns': res.staticRenderFns}));
									var component = vm.$mount ();
									var _append = function (index, value) {
										if (value) {
											elem [0].appendChild (value);
										}
									};
									jQuery.each (component.$el.childNodes, _append);
									evalJSFromHtml (html_txt);
									evalCSSFromHtml (html_txt, elem);
								}
							}
							catch (__except0__) {
								elem.html (html_txt);
							}
						}
						else {
							elem.html (html_txt);
						}
						if (run_fragment_init) {
							fragment_init (elem);
						}
						if (MOUNT_INIT_FUN) {
							var __iterable0__ = MOUNT_INIT_FUN;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var fun = __iterable0__ [__index0__];
								fun (elem);
							}
						}
						if (elem.hasClass ('refr_replace')) {
							var elem_tmp = elem.contents ();
							elem.replaceWith (elem_tmp);
						}
					};
					var save_as = function (blob, file_name) {
						var url = window.URL.createObjectURL (blob);
						var anchor_elem = document.createElement ('a');
						anchor_elem.style = 'display: none';
						anchor_elem.href = url;
						anchor_elem.download = file_name;
						document.body.appendChild (anchor_elem);
						anchor_elem.click ();
						document.body.removeChild (anchor_elem);
						var _ = function () {
							window.URL.revokeObjectURL (url);
						};
						setTimeout (_, 1000);
					};
					var download_binary_file = function (buf, content_disposition) {
						var file_name = 'temp.dat';
						var var_list = content_disposition.py_split (';');
						var __iterable0__ = var_list;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var pos = __iterable0__ [__index0__];
							if (__in__ ('filename', pos)) {
								var file_name = pos.py_split ('=') [1];
								break;
							}
						}
						save_as (buf, file_name);
					};
					var ajax_get = function (url, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						var process_blob = false;
						try {
							req.responseType = 'blob';
							var process_blob = true;
						}
						catch (__except0__) {
							// pass;
						}
						var _onload = function () {
							if (process_blob) {
								var disp = req.getResponseHeader ('Content-Disposition');
								if (disp && __in__ ('attachment', disp)) {
									download_binary_file (req.response, disp);
									complete (null);
								}
								else {
									var reader = new FileReader ();
									var _on_reader_load = function () {
										if (req.status != 200 && req.status != 0) {
											console.log (reader.result);
											window.open ().document.write (reader.result);
											complete ('Error - details on new page');
										}
										else {
											complete (reader.result);
										}
									};
									reader.onload = _on_reader_load;
									reader.readAsText (req.response);
								}
							}
							else if (req.status != 200 && req.status != 0) {
								console.log (req.response);
								window.open ().document.write (req.response);
								complete ('Error - details on new page');
							}
							else {
								complete (req.response);
							}
						};
						req.onload = _onload;
						req.open ('GET', url, true);
						req.send (null);
					};
					window.ajax_get = ajax_get;
					var ajax_load = function (elem, url, complete) {
						var _onload = function (responseText) {
							mount_html (elem, responseText);
							complete (responseText);
						};
						ajax_get (url, _onload);
					};
					window.ajax_load = ajax_load;
					var _req_post = function (req, url, data, complete, content_type) {
						var process_blob = false;
						try {
							req.responseType = 'blob';
							var process_blob = true;
						}
						catch (__except0__) {
							// pass;
						}
						var _onload = function () {
							if (process_blob) {
								var disp = req.getResponseHeader ('Content-Disposition');
								if (disp && __in__ ('attachment', disp)) {
									download_binary_file (req.response, disp);
									complete (null);
								}
								else {
									var reader = new FileReader ();
									var _on_reader_load = function () {
										if (req.status != 200 && req.status != 0) {
											console.log (reader.result);
											window.open ().document.write (reader.result);
											complete ('Error - details on new page');
										}
										complete (reader.result);
									};
									reader.onload = _on_reader_load;
									reader.readAsText (req.response);
								}
							}
							else {
								if (req.status != 200 && req.status != 0) {
									console.log (req.response);
									window.open ().document.write (req.response);
									complete ('Error - details on new page');
								}
								complete (req.response);
							}
						};
						req.onload = _onload;
						req.open ('POST', url, true);
						req.setRequestHeader ('X-CSRFToken', Cookies.get ('csrftoken'));
						if (content_type) {
							// pass;
						}
						else {
							req.setRequestHeader ('Content-type', 'application/x-www-form-urlencoded');
						}
						if (data.length) {
							req.setRequestHeader ('Content-length', data.length);
						}
						req.send (data);
					};
					var ajax_post = function (url, data, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						_req_post (req, url, data, complete);
					};
					window.ajax_post = ajax_post;
					var ajax_json = function (url, data, complete, process_req) {
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var _complete = function (data_in) {
							var _data = JSON.parse (data_in);
							complete (_data);
						};
						var data2 = JSON.stringify (data);
						ajax_post (url, data2, _complete, process_req);
					};
					window.ajax_json = ajax_json;
					var ajax_submit = function (form, complete, data_filter, process_req) {
						if (typeof data_filter == 'undefined' || (data_filter != null && data_filter .hasOwnProperty ("__kwargtrans__"))) {;
							var data_filter = null;
						};
						if (typeof process_req == 'undefined' || (process_req != null && process_req .hasOwnProperty ("__kwargtrans__"))) {;
							var process_req = null;
						};
						var content_type = null;
						var req = new XMLHttpRequest ();
						if (process_req) {
							process_req (req);
						}
						if (form.find ("[type='file']").length > 0) {
							var data = new FormData (form [0]);
							if (data_filter) {
								var data = data_filter (data);
							}
							var content_type = 'multipart/form-data; boundary=...';
							if (!(form.find ('#progress').length == 1)) {
								form.find ('div.inline-form-body').append ("<div class='progress progress-striped active'><div id='progress' class='progress-bar' role='progressbar' style='width: 0%;'></div></div>");
							}
							else {
								jQuery ('#progress').width ('0%');
							}
							var _progressHandlingFunction = function (e) {
								if (e.lengthComputable) {
									jQuery ('#progress').width (('' + parseInt ((100 * e.loaded) / e.total)) + '%');
								}
							};
							req.upload.addEventListener ('progress', _progressHandlingFunction, false);
						}
						else {
							var data = form.serialize ();
							if (data_filter) {
								var data = data_filter (data);
							}
						}
						_req_post (req, corect_href (form.attr ('action')), data, complete, content_type);
					};
					window.ajax_submit = ajax_submit;
					var get_page = function (elem) {
						if (elem.hasClass ('.tab-pane')) {
							return elem;
						}
						else {
							return elem.closest ('.tab-pane');
						}
					};
					var get_table_type = function (elem) {
						var tabsort = elem.find ('.tabsort');
						if (tabsort.length == 0) {
							var tabsort = get_page (elem).find ('.tabsort');
						}
						if (tabsort.length > 0) {
							var ret = tabsort.attr ('table_type');
							if (ret) {
								return ret;
							}
						}
						return '';
					};
					var can_popup = function () {
						if (jQuery ('.modal-open').length > 0) {
							return false;
						}
						else {
							return true;
						}
					};
					var corect_href = function (href, only_table) {
						if (typeof only_table == 'undefined' || (only_table != null && only_table .hasOwnProperty ("__kwargtrans__"))) {;
							var only_table = false;
						};
						if (only_table) {
							if (__in__ ('only_table', href)) {
								return href;
							}
						}
						else if (__in__ ('only_content', href)) {
							return href;
						}
						if (only_table) {
							if (__in__ ('?', href)) {
								return href + '&only_table=1';
							}
							else {
								return href + '?only_table=1';
							}
						}
						else if (__in__ ('?', href)) {
							return href + '&only_content=1';
						}
						else {
							return href + '?only_content=1';
						}
					};
					var remove_page_from_href = function (href) {
						var x = href.py_split ('?');
						if (len (x) > 1) {
							var x2 = x [1].py_split ('&');
							if (len (x2) > 1) {
								var x3 = list ([]);
								var __iterable0__ = x2;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var pos = __iterable0__ [__index0__];
									if (!(__in__ ('page=', pos))) {
										x3.append (pos);
									}
								}
								return (x [0] + '?') + ''.join (x3);
							}
							else if (__in__ ('page=', x2 [0])) {
								return x2;
							}
							else {
								return href;
							}
						}
						return href;
					};
					var load_css = function (path) {
						if (!(LOADED_FILES && __in__ (path, LOADED_FILES))) {
							LOADED_FILES [path] = null;
							var req = new XMLHttpRequest ();
							var _onload = function () {
								jQuery ('<style type="text/css"></style>').html (req.responseText).appendTo ('head');
							};
							req.onload = _onload;
							req.open ('GET', path, true);
							req.send ('');
						}
					};
					window.load_css = load_css;
					var on_load_js = function (path) {
						if (LOADED_FILES && __in__ (path, LOADED_FILES)) {
							var functions = LOADED_FILES [path];
							if (functions) {
								var __iterable0__ = functions;
								for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
									var fun = __iterable0__ [__index0__];
									fun ();
								}
							}
							LOADED_FILES [path] = null;
						}
					};
					var load_js = function (path, fun) {
						if (LOADED_FILES && __in__ (path, LOADED_FILES)) {
							if (LOADED_FILES [path]) {
								LOADED_FILES [path].push (fun);
							}
							else {
								fun ();
							}
						}
						else {
							LOADED_FILES [path] = list ([fun]);
							var req = new XMLHttpRequest ();
							var _onload = function () {
								var script = document.createElement ('script');
								script.text = req.responseText;
								document.head.appendChild (script).parentNode.removeChild (script);
								on_load_js (path);
							};
							req.onload = _onload;
							req.open ('GET', path, true);
							req.send ('');
						}
					};
					window.load_js = load_js;
					var load_many_js = function (paths, fun) {
						var counter = 1;
						var _fun = function () {
							counter = counter - 1;
							if (counter == 0) {
								fun ();
							}
						};
						var __iterable0__ = paths.py_split (';');
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var path = __iterable0__ [__index0__];
							if (path.length > 0) {
								var counter = counter + 1;
								load_js (path, _fun);
							}
						}
						_fun ();
					};
					window.load_many_js = load_many_js;
					var history_push_state = function (title, url, data) {
						if (typeof data == 'undefined' || (data != null && data .hasOwnProperty ("__kwargtrans__"))) {;
							var data = null;
						};
						var url2 = url.py_split ('?') [0];
						if (data) {
							var data2 = list ([LZString.compress (data [0]), data [1]]);
						}
						else {
							var data2 = title;
						}
						window.history.pushState (data2, title, url2);
					};
					window.history_push_state = history_push_state;
					var animate_combo = function (button, obj1, obj2, obj1_style_off, obj1_style_on, obj2_style_off, obj2_style_on, speed, end) {
						if (typeof end == 'undefined' || (end != null && end .hasOwnProperty ("__kwargtrans__"))) {;
							var end = null;
						};
						if (end) {
							var end2 = end;
						}
						else {
							var end2 = function () {
								// pass;
							};
						}
						var _animate = function () {
							if (button.hasClass ('on')) {
								button.removeClass ('on');
								obj1.animate (obj1_style_off, speed);
								obj2.animate (obj2_style_off, speed, 'swing', end2);
							}
							else {
								button.addClass ('on');
								obj1.animate (obj1_style_on, speed);
								obj2.animate (obj2_style_on, speed, 'swing', end2);
							}
						};
						button.click (_animate);
					};
					window.animate_combo = animate_combo;
					window.icons = dict ({'time': 'fa fa-clock-o', 'date': 'fa fa-calendar', 'up': 'fa fa-chevron-up', 'down': 'fa fa-chevron-down', 'previous': 'fa fa-chevron-left', 'next': 'fa fa-chevron-right', 'today': 'fa fa-calendar-check-o', 'clear': 'fa fa-trash', 'close': 'fa fa-times', 'paginationSwitchDown': 'fa-chevron-down', 'paginationSwitchUp': 'fa-chevron-up', 'refresh': 'fa-refresh', 'toggle': 'fa-list-alt', 'columns': 'fa-th', 'detailOpen': 'fa-plus', 'detailClose': 'fa-minus'});
					var get_and_run_script = function (url, elem, e) {
						var _on_load_js = function (html_text) {
							var object = jQuery (elem);
							var x = jQuery (html_text).html ();
							if (x) {
								eval (x);
							}
							var object = null;
						};
						ajax_get (url, _on_load_js);
					};
					__pragma__ ('<all>')
						__all__.FIRST_INIT = FIRST_INIT;
						__all__.FRAGMENT_INIT_FUN = FRAGMENT_INIT_FUN;
						__all__.LOADED_FILES = LOADED_FILES;
						__all__.MOUNT_INIT_FUN = MOUNT_INIT_FUN;
						__all__.__name__ = __name__;
						__all__._req_post = _req_post;
						__all__.ajax_get = ajax_get;
						__all__.ajax_json = ajax_json;
						__all__.ajax_load = ajax_load;
						__all__.ajax_post = ajax_post;
						__all__.ajax_submit = ajax_submit;
						__all__.animate_combo = animate_combo;
						__all__.can_popup = can_popup;
						__all__.corect_href = corect_href;
						__all__.download_binary_file = download_binary_file;
						__all__.evalCSSFromHtml = evalCSSFromHtml;
						__all__.evalJSFromHtml = evalJSFromHtml;
						__all__.fragment_init = fragment_init;
						__all__.get_and_run_script = get_and_run_script;
						__all__.get_page = get_page;
						__all__.get_table_type = get_table_type;
						__all__.history_push_state = history_push_state;
						__all__.load_css = load_css;
						__all__.load_js = load_js;
						__all__.load_many_js = load_many_js;
						__all__.mount_html = mount_html;
						__all__.on_load_js = on_load_js;
						__all__.register_fragment_init_fun = register_fragment_init_fun;
						__all__.register_mount_fun = register_mount_fun;
						__all__.remove_page_from_href = remove_page_from_href;
						__all__.save_as = save_as;
					__pragma__ ('</all>')
				}
			}
		}
	);

	__nest__ (
		__all__,
		'widget', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'widget';
					var humanFileSize = function (bytes, si) {
						if (si) {
							var thresh = 1000;
						}
						else {
							var thresh = 1024;
						}
						if (Math.abs (bytes) < thresh) {
							return tuple ([bytes + ' B', 0]);
						}
						if (si) {
							var units = list (['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']);
						}
						else {
							var units = list (['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']);
						}
						var u = -(1);
						while (true) {
							bytes /= thresh;
							u++;
							if (!(Math.abs (bytes) >= thresh && u < units.length - 1)) {
								break;
							}
						}
						return tuple ([(bytes.toFixed (1) + ' ') + units [u], u + 1]);
					};
					var img_field = function (elem) {
						var txt = jQuery (elem).val ().py_replace (new RegExp ('^.*[\\\\ /]'), '');
						jQuery (elem).closest ('label').find ('.upload').html (txt);
						if (elem.files && elem.files [0]) {
							var file_name = elem.files [0].name;
							var ext = list (['.jpeg', '.jpg', '.svg', '.gif', '.png']);
							var test = false;
							var __iterable0__ = ext;
							for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
								var pos = __iterable0__ [__index0__];
								if (__in__ (pos, file_name.lower ())) {
									var test = true;
									break;
								}
							}
							if (test) {
								var reader = new FileReader ();
								var _onload = function (e) {
									var x = jQuery (elem).closest ('label').find ('.img');
									if (x.length > 0) {
										x.remove ();
									}
									var img = jQuery ("<img class='img' />");
									img.insertAfter (jQuery (elem).closest ('label').find ('input'));
									img.attr ('src', e.target.result);
								};
								reader.onload = _onload;
								reader.readAsDataURL (elem.files [0]);
							}
							else {
								var x = jQuery (elem).closest ('label').find ('.img');
								if (x.length > 0) {
									x.remove ();
								}
								var __left0__ = humanFileSize (elem.files [0].size, true);
								var size = __left0__ [0];
								var level = __left0__ [1];
								var ext = ((((elem.files [0].type + "<br><span class='size_level_") + level) + "'>") + size) + '</span>';
								var img = jQuery ("<p class='img' />");
								img.insertAfter (jQuery (elem).closest ('label').find ('input'));
								img.html (ext);
							}
						}
					};
					window.img_field = img_field;
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.humanFileSize = humanFileSize;
						__all__.img_field = img_field;
					__pragma__ ('</all>')
				}
			}
		}
	);

	(function () {
		var __name__ = '__main__';
		var Page = __init__ (__world__.page).Page;
		var TabMenuItem = __init__ (__world__.tabmenuitem).TabMenuItem;
		var get_menu = __init__ (__world__.tabmenu).get_menu;
		var on_get_tbl_value = __init__ (__world__.popup).on_get_tbl_value;
		var on_new_tbl_value = __init__ (__world__.popup).on_new_tbl_value;
		var on_get_row = __init__ (__world__.popup).on_get_row;
		var on_popup_edit_new = __init__ (__world__.popup).on_popup_edit_new;
		var on_popup_inline = __init__ (__world__.popup).on_popup_inline;
		var on_popup_info = __init__ (__world__.popup).on_popup_info;
		var on_popup_delete = __init__ (__world__.popup).on_popup_delete;
		var on_cancel_inline = __init__ (__world__.popup).on_cancel_inline;
		var refresh_fragment = __init__ (__world__.popup).refresh_fragment;
		var on_edit_ok = __init__ (__world__.popup).on_edit_ok;
		var on_delete_ok = __init__ (__world__.popup).on_delete_ok;
		var ret_ok = __init__ (__world__.popup).ret_ok;
		var refresh_current_object = __init__ (__world__.popup).refresh_current_object;
		var refresh_current_page = __init__ (__world__.popup).refresh_current_page;
		var refresh_current_app = __init__ (__world__.popup).refresh_current_app;
		var only_get = __init__ (__world__.popup).only_get;
		var init_table = __init__ (__world__.tbl).init_table;
		var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
		var can_popup = __init__ (__world__.tools).can_popup;
		var corect_href = __init__ (__world__.tools).corect_href;
		var get_table_type = __init__ (__world__.tools).get_table_type;
		var handle_class_click = __init__ (__world__.tools).handle_class_click;
		var ajax_get = __init__ (__world__.tools).ajax_get;
		var ajax_post = __init__ (__world__.tools).ajax_post;
		var ajax_load = __init__ (__world__.tools).ajax_load;
		var ajax_submit = __init__ (__world__.tools).ajax_submit;
		var load_css = __init__ (__world__.tools).load_css;
		var load_js = __init__ (__world__.tools).load_js;
		var load_many_js = __init__ (__world__.tools).load_many_js;
		var history_push_state = __init__ (__world__.tools).history_push_state;
		var mount_html = __init__ (__world__.tools).mount_html;
		var register_fragment_init_fun = __init__ (__world__.tools).register_fragment_init_fun;
		var register_mount_fun = __init__ (__world__.tools).register_mount_fun;
		var remove_page_from_href = __init__ (__world__.tools).remove_page_from_href;
		var get_and_run_script = __init__ (__world__.tools).get_and_run_script;
		var service_worker_and_indexedDB_test = __init__ (__world__.offline).service_worker_and_indexedDB_test;
		var install_service_worker = __init__ (__world__.offline).install_service_worker;
		var sync_and_run = __init__ (__world__.db).sync_and_run;
		var img_field = __init__ (__world__.widget).img_field;
		var process_on_click = __init__ (__world__.click_process).process_on_click;
		window.PS = null;
		window.MOUNTED_COMPONENTS = 0;
		var app_init = function (prj_name, application_template, menu_id, lang, base_path, base_fragment_init, component_init, offline_support, start_page, gen_time) {
			moment.locale (lang);
			window.ACTIVE_PAGE = null;
			window.PRJ_NAME = prj_name;
			window.APPLICATION_TEMPLATE = application_template;
			window.MENU = null;
			window.PUSH_STATE = true;
			if (base_path) {
				window.BASE_PATH = base_path;
			}
			else {
				window.BASE_PATH = '';
			}
			window.WAIT_ICON = null;
			window.WAIT_ICON2 = false;
			window.MENU_ID = 0;
			window.BASE_FRAGMENT_INIT = base_fragment_init;
			window.COUNTER = 1;
			window.EDIT_RET_FUNCTION = null;
			window.RET_CONTROL = null;
			window.COMPONENT_INIT = component_init;
			window.LANG = lang;
			window.GEN_TIME = gen_time;
			if (offline_support) {
				if (navigator.onLine && service_worker_and_indexedDB_test ()) {
					install_service_worker ();
				}
			}
			var _on_sync = function (status) {
				if (status == 'OK-refresh') {
					location.reload ();
				}
			};
			sync_and_run ('sys', _on_sync);
			jQuery (window).resize (datatable_onresize);
			var _on_submit = function (e) {
				var self = jQuery (this);
				if (jQuery (this).hasClass ('DialogForm')) {
					e.preventDefault ();
					on_edit_ok (false, jQuery (this));
					return ;
				}
				if (jQuery (this).attr ('target') == '_blank') {
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				if (jQuery (this).attr ('target') == '_self') {
					return true;
				}
				if (jQuery (this).attr ('target') == 'refresh_obj') {
					if (refresh_fragment (jQuery (this), null, true, null, true)) {
						return false;
					}
				}
				var data = jQuery (this).serialize ();
				if (data && __in__ ('pdf=on', data)) {
					jQuery (this).attr ('target', '_blank');
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				if (data && __in__ ('odf=on', data)) {
					jQuery (this).attr ('target', '_blank');
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				e.preventDefault ();
				var submit_button = jQuery (this).find ('button[type="submit"]');
				if (submit_button.length > 0) {
					submit_button.attr ('data-style', 'zoom-out');
					submit_button.attr ('data-spinner-color', '#FF0000');
					window.WAIT_ICON = Ladda.create (submit_button [0]);
					window.WAIT_ICON.start ();
				}
				else {
					window.WAIT_ICON2 = true;
					jQuery ('#loading-indicator').show ();
				}
				var href = jQuery (this).attr ('action');
				if (href) {
					jQuery (this).attr ('action', corect_href (remove_page_from_href (href)));
				}
				var _on_submit2 = function (data) {
					if (window.ACTIVE_PAGE) {
						mount_html (window.ACTIVE_PAGE.page, data);
					}
					else {
						_on_menu_href (self, self.attr ('title'), null, data);
					}
					if (window.WAIT_ICON) {
						window.WAIT_ICON.stop ();
					}
					if (window.WAIT_ICON2) {
						jQuery ('#loading-indicator').hide ();
						window.WAIT_ICON2 = false;
					}
				};
				ajax_submit (jQuery (this), _on_submit2);
			};
			jQuery ('#tabs2_content').on ('submit', 'form', _on_submit);
			jQuery ('#dialog-form-modal').on ('submit', 'form', _on_submit);
			jQuery ('#search').on ('submit', 'form', _on_submit);
			if (jQuery ('#menu').length > 0) {
				window.PS = new PerfectScrollbar ('#menu');
				var _on_resize = function () {
					window.PS.update ();
				};
				jQuery (window).resize (_on_resize);
			}
			var _on_key = function (e) {
				if (e.which == 13) {
					var elem = jQuery (e.target);
					if (elem.prop ('tagName') != 'TEXTAREA') {
						var form = elem.closest ('form');
						if (form.length > 0) {
							if (form.hasClass ('DialogForm')) {
								e.preventDefault ();
								on_edit_ok (false, form);
								return ;
							}
						}
					}
				}
			};
			jQuery (document).keypress (_on_key);
			process_on_click (EVENT_TAB);
			if (can_popup ()) {
				var _local_fun = function () {
					if (window.APPLICATION_TEMPLATE != 'traditional') {
						var pos = jQuery ('.menu-href.btn-warning');
						if (pos.length > 0) {
							var elem = jQuery ('#a_' + pos.closest ('div.tab-pane').attr ('id'));
							elem.tab ('show');
						}
						else {
							var elem = jQuery ('.first_pos');
							elem.tab ('show');
						}
					}
					else {
						var id = int (menu_id) + 1;
						var elem = jQuery (('#tabs a:eq(' + id) + ')');
						elem.tab ('show');
					}
					var _on_menu_click = function (e) {
						if (window.APPLICATION_TEMPLATE != 'traditional') {
							e.preventDefault ();
							var toggler = jQuery ('#topmenu').find ('.navbar-toggler');
							if (toggler && toggler.is (':visible')) {
								var obj = this;
								var _on_collapse = function () {
									_on_menu_href (obj);
									jQuery ('#navbar-ex1-collapse').off ('hidden.bs.collapse', _on_collapse);
								};
								jQuery ('#navbar-ex1-collapse').on ('hidden.bs.collapse', _on_collapse);
								jQuery ('#navbar-ex1-collapse').collapse ('hide');
							}
							else {
								_on_menu_href (this);
							}
						}
					};
					jQuery ('body').on ('click', 'a.menu-href', _on_menu_click);
					var _on_logout_click = function () {
						window.location = jQuery (this).attr ('action');
					};
					jQuery ('#logout').on ('click', _on_logout_click);
					var _on_sysmenu_click = function () {
						window.location = jQuery (this).attr ('action');
					};
					jQuery ('.system_menu').on ('click', _on_sysmenu_click);
					var _on_tabs_click = function (e) {
						e.preventDefault ();
						jQuery (this).tab ('show');
					};
					jQuery ('#tabs a').click (_on_tabs_click);
					var _on_resize = function (e) {
						datatable_onresize ();
					};
					jQuery ('#tabs2').on ('shown.bs.tab', _on_resize);
					var _on_timeout = function (e) {
						window.setTimeout (datatable_onresize, 300);
					};
					jQuery ('body').on ('expanded.pushMenu collapsed.pushMenu', _on_timeout);
				};
				jQuery (_local_fun);
			}
			var _init_start_wiki_page = function () {
				if (start_page && start_page != 'None' && window.location.pathname == base_path) {
					var _on_load = function (responseText, status, response) {
						// pass;
					};
					ajax_load (jQuery ('#wiki_start'), (base_path + start_page) + '?only_content&schtml=1', _on_load);
				}
			};
			window.init_start_wiki_page = _init_start_wiki_page;
			_init_start_wiki_page ();
		};
		var _on_menu_href = function (elem, title, url, txt) {
			if (typeof title == 'undefined' || (title != null && title .hasOwnProperty ("__kwargtrans__"))) {;
				var title = null;
			};
			if (typeof url == 'undefined' || (url != null && url .hasOwnProperty ("__kwargtrans__"))) {;
				var url = null;
			};
			if (typeof txt == 'undefined' || (txt != null && txt .hasOwnProperty ("__kwargtrans__"))) {;
				var txt = null;
			};
			if (window.APPLICATION_TEMPLATE != 'traditional') {
				if (!(title)) {
					var title = jQuery.trim (jQuery (elem).text ());
				}
				if (txt) {
					var value = jQuery (('<div>' + txt) + '</div>').find ('head').find ('title').text ();
					if (value) {
						var title = value;
					}
				}
				var menu = get_menu ();
				var classname = jQuery (elem).attr ('class');
				if (classname && __in__ ('btn', classname)) {
					if (window.WAIT_ICON) {
						window.WAIT_ICON.stop ();
					}
					jQuery (elem).attr ('data-style', 'zoom-out');
					jQuery (elem).attr ('data-spinner-color', '#FF0000');
					window.WAIT_ICON = Ladda.create (elem);
				}
				else {
					window.WAIT_ICON = null;
				}
				if (window.APPLICATION_TEMPLATE == 'modern' && menu.is_open (title)) {
					menu.activate (title);
				}
				else {
					if (url) {
						var href = url;
					}
					else {
						var href = jQuery (elem).attr ('href');
					}
					var href2 = corect_href (href);
					var _on_new_win = function (data) {
						jQuery ('#wiki_start').hide ();
						if (window.APPLICATION_TEMPLATE == 'modern') {
							var id = menu.new_page (title, data, href2);
						}
						else {
							mount_html (jQuery ('#body_body'), data);
							window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
							window.ACTIVE_PAGE.set_href (href2);
							if (window.PUSH_STATE) {
								var id = jQuery (elem).attr ('id');
								if (!(id)) {
									var id = 'menu_id_' + window.MENU_ID;
									window.MENU_ID = window.MENU_ID + 1;
									jQuery (elem).attr ('id', id);
								}
								history_push_state (title, href, list ([data, id]));
							}
						}
						if (window.WAIT_ICON) {
							window.WAIT_ICON.stop ();
							window.WAIT_ICON = null;
						}
						if (window.WAIT_ICON2) {
							jQuery ('#loading-indicator').hide ();
							window.WAIT_ICON2 = false;
						}
					};
					if (window.APPLICATION_TEMPLATE == 'standard' && classname && __in__ ('btn', classname)) {
						jQuery ('a.menu-href').removeClass ('btn-warning');
						jQuery (elem).addClass ('btn-warning');
					}
					if (txt) {
						_on_new_win (txt);
					}
					else {
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						else {
							window.WAIT_ICON2 = true;
							jQuery ('#loading-indicator').show ();
						}
						ajax_get (href2, _on_new_win);
						jQuery ('.navbar-ex1-collapse').collapse ('hide');
					}
				}
				jQuery ('.auto-hide').trigger ('click');
				return false;
			}
		};
		var _on_error = function (request, settings) {
			if (window.WAIT_ICON) {
				window.WAIT_ICON.stop ();
				window.WAIT_ICON = null;
			}
			if (window.WAIT_ICON2) {
				jQuery ('#loading-indicator').hide ();
				window.WAIT_ICON2 = false;
			}
			if (settings.status == 200) {
				return ;
			}
			if (settings.responseText) {
				var start = settings.responseText.indexOf ('<body>');
				var end = settings.responseText.lastIndexOf ('</body>');
				if (start > 0 && end > 0) {
					mount_html (jQuery ('#dialog-data-error'), settings.responseText.substring (start + 6, end - 1));
					jQuery ('#dialog-form-error').modal ();
				}
				else {
					mount_html (jQuery ('#dialog-data-error'), settings.responseText);
					jQuery ('#dialog-form-error').modal ();
				}
			}
		};
		var jquery_ready = function () {
			jQuery (document).ajaxError (_on_error);
			var _on_hide = function (e) {
				mount_html (jQuery (this).find ('div.dialog-data'), "<div class='alert alert-info' role='alert'>Sending data - please wait</div>", false, false);
			};
			jQuery ('div.dialog-form').on ('hide.bs.modal', _on_hide);
			var _local_fun = function () {
				console.log ('collapsed');
			};
			jQuery ('.navbar-ex1-collapse').on ('hidden.bs.collapse', _local_fun);
			if (window.APPLICATION_TEMPLATE == 'traditional') {
				window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
			}
			else if (window.APPLICATION_TEMPLATE == 'modern') {
				var txt = jQuery ('.page').html ();
				var txt2 = jQuery.trim (txt);
				if (txt2) {
					var txt = jQuery.trim (jQuery ('.page') [0].outerHTML);
					jQuery ('.page').remove ();
					var menu = get_menu ();
					menu.new_page (jQuery ('title').text (), txt, window.location.href);
				}
			}
			else {
				window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
				if (window.APPLICATION_TEMPLATE == 'to_print') {
					new Vue (dict ({'el': '#body_body'}));
				}
			}
		};
		var on_new_tab = function (url, elem, e) {
			var title = jQuery (e.currentTarget).attr ('title');
			var url2 = url.py_split ('?') [0];
			if (!(title)) {
				if (len (url2) > 16) {
					var title = '...' + url2.__getslice__ (-(13), null, 1);
				}
				else {
					var title = url2;
				}
			}
			return _on_menu_href (elem, title, url);
		};
		var EVENT_TAB = list ([tuple (['*', 'get_tbl_value', true, false, on_get_tbl_value]), tuple (['*', 'new_tbl_value', true, false, on_new_tbl_value]), tuple (['*', 'get_row', true, false, on_get_row]), tuple (['popup_edit', '*', true, false, on_popup_edit_new]), tuple (['popup_info', '*', true, false, on_popup_info]), tuple (['popup_delete', '*', true, false, on_popup_delete]), tuple (['inline', '*', true, false, on_popup_inline]), tuple (['_top', '*', true, false, on_new_tab]), tuple (['_top2', '*', true, false, on_new_tab]), tuple (['refresh_obj', '*', true, false, refresh_current_object]), tuple (['refresh_page', '*', true, false, refresh_current_page]), tuple (['refresh_app', '*', false, false, refresh_current_app]), tuple (['run_script', '*', false, false, get_and_run_script]), tuple (['null', '*', false, false, only_get])]);
		var standard_on_data = function (src_obj, href) {
			var _standard_on_data = function (data) {
				if (data && __in__ ('_parent_refr', data)) {
					refresh_fragment (src_obj);
				}
				else {
					if (window.APPLICATION_TEMPLATE == 'modern') {
						mount_html (window.ACTIVE_PAGE.page, data);
						window.ACTIVE_PAGE.set_href (href);
					}
					else {
						mount_html (jQuery ('#body_body'), data);
					}
					window.ACTIVE_PAGE.set_href (href);
					get_menu ().get_active_item ().url = href;
					if (window.PUSH_STATE) {
						history_push_state ('title', href);
					}
				}
			};
			return _standard_on_data;
		};
		window.standard_on_data = standard_on_data;
		var _on_popstate = function (e) {
			if (e.state) {
				window.PUSH_STATE = false;
				if (window.APPLICATION_TEMPLATE == 'modern') {
					var menu = get_menu ().activate (e.state, false);
				}
				else {
					var x = e.state;
					mount_html (jQuery ('#body_body'), LZString.decompress (x [0]));
					window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
					window.ACTIVE_PAGE.set_href (document.location);
					if (window.APPLICATION_TEMPLATE == 'standard') {
						jQuery ('a.menu-href').removeClass ('btn-warning');
						jQuery ('#' + x [1]).addClass ('btn-warning');
					}
				}
				window.PUSH_STATE = true;
			}
			else if (window.APPLICATION_TEMPLATE == 'modern') {
				// pass;
			}
			else {
				mount_html (jQuery ('#body_body'), '', false, false);
				window.ACTIVE_PAGE = null;
				if (window.APPLICATION_TEMPLATE == 'standard') {
					jQuery ('a.menu-href').removeClass ('btn-warning');
				}
			}
		};
		window.addEventListener ('popstate', _on_popstate, false);
		__pragma__ ('<use>' +
			'click_process' +
			'db' +
			'offline' +
			'page' +
			'popup' +
			'tabmenu' +
			'tabmenuitem' +
			'tbl' +
			'tools' +
			'widget' +
		'</use>')
		__pragma__ ('<all>')
			__all__.EVENT_TAB = EVENT_TAB;
			__all__.Page = Page;
			__all__.TabMenuItem = TabMenuItem;
			__all__.__name__ = __name__;
			__all__._on_error = _on_error;
			__all__._on_menu_href = _on_menu_href;
			__all__._on_popstate = _on_popstate;
			__all__.ajax_get = ajax_get;
			__all__.ajax_load = ajax_load;
			__all__.ajax_post = ajax_post;
			__all__.ajax_submit = ajax_submit;
			__all__.app_init = app_init;
			__all__.can_popup = can_popup;
			__all__.corect_href = corect_href;
			__all__.datatable_onresize = datatable_onresize;
			__all__.get_and_run_script = get_and_run_script;
			__all__.get_menu = get_menu;
			__all__.get_table_type = get_table_type;
			__all__.handle_class_click = handle_class_click;
			__all__.history_push_state = history_push_state;
			__all__.img_field = img_field;
			__all__.init_table = init_table;
			__all__.install_service_worker = install_service_worker;
			__all__.jquery_ready = jquery_ready;
			__all__.load_css = load_css;
			__all__.load_js = load_js;
			__all__.load_many_js = load_many_js;
			__all__.mount_html = mount_html;
			__all__.on_cancel_inline = on_cancel_inline;
			__all__.on_delete_ok = on_delete_ok;
			__all__.on_edit_ok = on_edit_ok;
			__all__.on_get_row = on_get_row;
			__all__.on_get_tbl_value = on_get_tbl_value;
			__all__.on_new_tab = on_new_tab;
			__all__.on_new_tbl_value = on_new_tbl_value;
			__all__.on_popup_delete = on_popup_delete;
			__all__.on_popup_edit_new = on_popup_edit_new;
			__all__.on_popup_info = on_popup_info;
			__all__.on_popup_inline = on_popup_inline;
			__all__.only_get = only_get;
			__all__.process_on_click = process_on_click;
			__all__.refresh_current_app = refresh_current_app;
			__all__.refresh_current_object = refresh_current_object;
			__all__.refresh_current_page = refresh_current_page;
			__all__.refresh_fragment = refresh_fragment;
			__all__.register_fragment_init_fun = register_fragment_init_fun;
			__all__.register_mount_fun = register_mount_fun;
			__all__.remove_page_from_href = remove_page_from_href;
			__all__.ret_ok = ret_ok;
			__all__.service_worker_and_indexedDB_test = service_worker_and_indexedDB_test;
			__all__.standard_on_data = standard_on_data;
			__all__.sync_and_run = sync_and_run;
		__pragma__ ('</all>')
	}) ();

    return __all__;
}
window ['pytigon'] = pytigon ();
