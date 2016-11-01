"use strict";
// Transcrypt'ed from Python, 2016-10-31 20:43:15

	var __all__ = {};
	var __world__ = __all__;
	
	// Nested object creator, part of the nesting may already exist and have attributes
	var __nest__ = function (headObject, tailNames, value) {
		// In some cases this will be a global object, e.g. 'window'
		var current = headObject;
		
		if (tailNames != '') {	// Split on empty string doesn't give empty list
			// Find the last already created object in tailNames
			var tailChain = tailNames.split ('.');
			var firstNewIndex = tailChain.length;
			for (var index = 0; index < tailChain.length; index++) {
				if (!current.hasOwnProperty (tailChain [index])) {
					firstNewIndex = index;
					break;
				}
				current = current [tailChain [index]];
			}
			
			// Create the rest of the objects, if any
			for (var index = firstNewIndex; index < tailChain.length; index++) {
				current [tailChain [index]] = {};
				current = current [tailChain [index]];
			}
		}
		
		// Insert it new attributes, it may have been created earlier and have other attributes
		for (var attrib in value) {
			current [attrib] = value [attrib];			
		}		
	};
	__all__.__nest__ = __nest__;
	
	// Initialize module if not yet done and return its globals
	var __init__ = function (module) {
		if (!module.__inited__) {
			module.__all__.__init__ (module.__all__);
			module.__inited__ = true;
		}
		return module.__all__;
	};
	__all__.__init__ = __init__;
	
	// Since we want to assign functions, a = b.f should make b.f produce a bound function
	// So __get__ should be called by a property rather then a function
	// Factory __get__ creates one of three curried functions for func
	// Which one is produced depends on what's to the left of the dot of the corresponding JavaScript property
	var __get__ = function (self, func, quotedFuncName) {
		if (self) {
			if (self.hasOwnProperty ('__class__') || typeof self == 'string' || self instanceof String) {			// Object before the dot
				if (quotedFuncName) {									// Memoize call since fcall is on, by installing bound function in instance
					Object.defineProperty (self, quotedFuncName, {		// Will override the non-own property, next time it will be called directly
						value: function () {							// So next time just call curry function that calls function
							var args = [] .slice.apply (arguments);
							return func.apply (null, [self] .concat (args));
						},				
						writable: true,
						enumerable: true,
						configurable: true
					});
				}
				return function () {									// Return bound function, code dupplication for efficiency if no memoizing
					var args = [] .slice.apply (arguments);				// So multilayer search prototype, apply __get__, call curry func that calls func
					return func.apply (null, [self] .concat (args));
				};
			}
			else {														// Class before the dot
				return func;											// Return static method
			}
		}
		else {															// Nothing before the dot
			return func;												// Return free function
		}
	}
	__all__.__get__ = __get__;
			
	// Class creator function
	var __class__ = function (name, bases, extra) {
		// Create class functor
		var cls = function () {
			var args = [] .slice.apply (arguments);
			return cls.__new__ (args);
		};
		
		// Copy methods, properties and static attributes from base classes to new class object
		for (var index = bases.length - 1; index >= 0; index--) {	// Reversed order, since class vars of first base should win
			var base = bases [index];
			for (var attrib in base) {
				var descrip = Object.getOwnPropertyDescriptor (base, attrib);
				Object.defineProperty (cls, attrib, descrip);
			}
		}
		
		// Add class specific attributes to class object
		cls.__name__ = name;
		cls.__bases__ = bases;
		
		// Add own methods, properties and static attributes to class object
		for (var attrib in extra) {
			var descrip = Object.getOwnPropertyDescriptor (extra, attrib);
			Object.defineProperty (cls, attrib, descrip);
		}
				
		// Return class object
		return cls;
	};
	__all__.__class__ = __class__;
	
	// Create mother of all classes		
	var object = __all__.__class__ ('object', [], {
		__init__: function (self) {},
			
		__name__: 'object',
		__bases__: [],
			
		// Object creator function is inherited by all classes (so in principle it could be made global)
		__new__: function (args) {	// Args are just the constructor args		
			// In JavaScript the Python class is the prototype of the Python object
			// In this way methods and static attributes will be available both with a class and an object before the dot
			// The descriptor produced by __get__ will return the right method flavor
			var instance = Object.create (this, {__class__: {value: this, enumerable: true}});
			
			// Call constructor
			this.__init__.apply (null, [instance] .concat (args));
			
			// Return instance			
			return instance;
		}	
	});
	__all__.object = object;
	
	// Define __pragma__ to preserve '<all>' and '</all>', since it's never generated as a function, must be done early, so here
	var __pragma__ = function () {};
	__all__.__pragma__ = __pragma__;
	__nest__ (
		__all__,
		'org.transcrypt.__base__', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __Envir__ = __class__ ('__Envir__', [object], {
						get __init__ () {return __get__ (this, function (self) {
							self.transpiler_name = 'transcrypt';
							self.transpiler_version = '3.5.222';
							self.target_subdir = '__javascript__';
						});}
					});
					var __envir__ = __Envir__ ();
					__pragma__ ('<all>')
						__all__.__Envir__ = __Envir__;
						__all__.__envir__ = __envir__;
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
					var Exception = __class__ ('Exception', [object], {
						get __init__ () {return __get__ (this, function (self) {
							var args = tuple ([].slice.apply (arguments).slice (1));
							self.args = args;
						});},
						get __repr__ () {return __get__ (this, function (self) {
							if (len (self.args)) {
								return '{}{}'.format (self.__class__.__name__, repr (tuple (self.args)));
							}
							else {
								return '{}()'.format (self.__class__.__name__);
							}
						});},
						get __str__ () {return __get__ (this, function (self) {
							if (len (self.args) > 1) {
								return str (tuple (self.args));
							}
							else {
								if (len (self.args)) {
									return str (self.args [0]);
								}
								else {
									return '';
								}
							}
						});}
					});
					var StopIteration = __class__ ('StopIteration', [object], {
						get __init__ () {return __get__ (this, function (self) {
							Exception.__init__ (self, 'Iterator exhausted');
						});}
					});
					var ValueError = __class__ ('ValueError', [Exception], {
					});
					var AssertionError = __class__ ('AssertionError', [Exception], {
					});
					var __sort__ = function (iterable, key, reverse) {
						if (typeof key == 'undefined' || (key != null && key .__class__ == __kwargdict__)) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .__class__ == __kwargdict__)) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
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
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
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
								return key (a) > key (b);
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
						if (typeof key == 'undefined' || (key != null && key .__class__ == __kwargdict__)) {;
							var key = null;
						};
						if (typeof reverse == 'undefined' || (reverse != null && reverse .__class__ == __kwargdict__)) {;
							var reverse = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
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
						if (type (iterable) == dict) {
							var result = copy (iterable.keys ());
						}
						else {
							var result = copy (iterable);
						}
						__sort__ (result, key, reverse);
						return result;
					};
					var map = function (func, iterable) {
						return function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
								var item = __iterable0__ [__index0__];
								__accu0__.append (func (item));
							}
							return __accu0__;
						} ();
					};
					var filter = function (func, iterable) {
						return function () {
							var __accu0__ = [];
							var __iterable0__ = iterable;
							for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
								var item = __iterable0__ [__index0__];
								if (func (item)) {
									__accu0__.append (item);
								}
							}
							return __accu0__;
						} ();
					};
					var __Terminal__ = __class__ ('__Terminal__', [object], {
						get __init__ () {return __get__ (this, function (self) {
							try {
								self.element = document.getElementById ('__terminal__');
							}
							catch (__except0__) {
								self.element = null;
							}
							if (self.element) {
								self.buffer = '';
								self.element.style.overflowX = 'auto';
								self.element.style.padding = '5px';
								self.element.innerHTML = '_';
							}
						});},
						get print () {return __get__ (this, function (self) {
							var sep = ' ';
							var end = '\n';
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											case 'sep': var sep = __allkwargs0__ [__attrib0__]; break;
											case 'end': var end = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
								var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
							}
							else {
								var args = tuple ();
							}
							if (self.element) {
								self.buffer = '{}{}{}'.format (self.buffer, sep.join (function () {
									var __accu0__ = [];
									var __iterable0__ = args;
									for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
										var arg = __iterable0__ [__index0__];
										__accu0__.append (str (arg));
									}
									return __accu0__;
								} ()), end).__getslice__ (-(4096), null, 1);
								self.element.innerHTML = self.buffer.py_replace ('\n', '<br>');
								self.element.scrollTop = self.element.scrollHeight;
							}
							else {
								console.log (sep.join (function () {
									var __accu0__ = [];
									var __iterable0__ = args;
									for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
										var arg = __iterable0__ [__index0__];
										__accu0__.append (str (arg));
									}
									return __accu0__;
								} ()));
							}
						});},
						get input () {return __get__ (this, function (self, question) {
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].__class__ == __kwargdict__) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'self': var self = __allkwargs0__ [__attrib0__]; break;
											case 'question': var question = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
							}
							else {
							}
							self.print ('{}_'.format (question), __kwargdict__ ({end: ''}));
							try {
								var answer = window.prompt (question);
							}
							catch (__except0__) {
								console.log ('Error: Blocking input not yet implemented outside browser');
							}
							self.buffer = self.buffer.__getslice__ (0, -(1), 1);
							self.print (answer);
							return answer;
						});}
					});
					var __terminal__ = __Terminal__ ();
					__pragma__ ('<all>')
						__all__.AssertionError = AssertionError;
						__all__.Exception = Exception;
						__all__.StopIteration = StopIteration;
						__all__.ValueError = ValueError;
						__all__.__Terminal__ = __Terminal__;
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

	// Initialize non-nested modules __base__ and __standard__ and make its names available directly and via __all__
	// It can't do that itself, because it is a regular Python module
	// The compiler recognizes its their namesand generates them inline rather than nesting them
	// In this way it isn't needed to import them everywhere
	 	
	// __base__
	
	__nest__ (__all__, '', __init__ (__all__.org.transcrypt.__base__));
	var __envir__ = __all__.__envir__;

	// __standard__
	
	__nest__ (__all__, '', __init__ (__all__.org.transcrypt.__standard__));
	
	var Exception = __all__.Exception;
	var StopIteration = __all__.StopIteration;
	var ValueError = __all__.ValueError;
	var AssertionError = __all__.AssertionError;
	
	var __sort__ = __all__.__sort__;
	var sorted = __all__.sorted;
	
	var map = __all__.map;
	var filter = __all__.filter;
	
	
	__all__.print = __all__.__terminal__.print;
	__all__.input = __all__.__terminal__.input;
	
	var print = __all__.print;
	var input = __all__.input;

	// Complete __envir__, that was created in __base__, for non-stub mode
	__envir__.executor_name = __envir__.transpiler_name;
	
	// Make make __main__ available in browser
	var __main__ = {__file__: ''};
	__all__.main = __main__;
	
	// Define current exception, there's at most one exception in the air at any time
	var __except__ = null;
	__all__.__except__ = __except__;
		
	// Define recognizable dictionary for **kwargs parameter
	var __kwargdict__ = function (anObject) {
		anObject.__class__ = __kwargdict__;	// This class needs no __name__
		anObject.constructor = Object;
		return anObject;
	}
	__all__.___kwargdict__ = __kwargdict__;
	
	// Property installer function, no member since that would bloat classes
	var property = function (getter, setter) {	// Returns a property descriptor rather than a property
		if (!setter) {	// ??? Make setter optional instead of dummy?
			setter = function () {};
		}
		return {get: function () {return getter (this)}, set: function (value) {setter (this, value)}, enumerable: true};
	}
	__all__.property = property;
	
	// Assert function, call to it only generated when compiling with --dassert option
	function assert (condition, message) {
		if (!condition) {
			if (message != undefined) {
				throw AssertionError (message);
			}
			else {
				throw AssertionError ();
			}
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
	}
	__all__.__merge__ = __merge__;
	
	/* Not needed anymore?
	// Make console.log understand apply
	console.log.apply = function () {
		print ([] .slice.apply (arguments) .slice (1));
	};
	*/

	// Manipulating attributes by name
	
	var dir = function (obj) {
		var aList = [];
		for (var aKey in obj) {
			aList.push (aKey);
		}
		aList.sort ();
		return aList;
	}
	
	var setattr = function (obj, name, value) {
		obj [name] = value;
	};
		
	__all__.setattr = setattr;
	
	var getattr = function (obj, name) {
		return obj [name];
	};
	
	__all__.getattr= getattr
	
	var hasattr = function (obj, name) {
		return name in obj;
	};
	__all__.hasattr = hasattr;
	
	var delattr = function (obj, name) {
		delete obj [name];
	};
	__all__.delattr = (delattr);
	
	// The __in__ function, used to mimic Python's 'in' operator
	// In addition to CPython's semantics, the 'in' operator is also allowed to work on objects, avoiding a counterintuitive separation between Python dicts and JavaScript objects
	// In general many Transcrypt compound types feature a deliberate blend of Python and JavaScript facilities, facilitating efficient integration with JavaScript libraries
	// If only Python objects and Python dicts are dealt with in a certain context, the more pythonic 'hasattr' is preferred for the objects as opposed to 'in' for the dicts
	var __in__ = function (element, container) {
		if (type (container) == dict) {
			return container.keys () .indexOf (element) > -1;                                   // The keys of parameter 'element' are in an array
		}
		else {
			return container.indexOf ? container.indexOf (element) > -1 : element in container; // Parameter 'element' itself is an array, string or object
		}
	}
	__all__.__in__ = __in__;
	
	// Find out if an attribute is special
	var __specialattrib__ = function (attrib) {
		return (attrib.startswith ('__') && attrib.endswith ('__')) || attrib == 'constructor' || attrib.startswith ('py_');
	}
	__all__.__specialattrib__ = __specialattrib__;
		
	// Len function for any object
	var len = function (anObject) {
		if (anObject) {
			var l = anObject.length;
			if (l == undefined) {
				var result = 0;
				for (var attrib in anObject) {
					if (!__specialattrib__ (attrib)) {
						result++;
					}
				}
				return result;
			}
			else {
				return l;
			}
		}
		else {
			return 0;
		}
	}
	__all__.len = len;
	

	// General conversions
	
	function __ (any) {				// Truthyness, __ ([1, 2, 3]) returns [1, 2, 3], needed for nonempty selection: l = list1 or list2]
		return (['boolean', 'number'] .indexOf (typeof any) >= 0 || any instanceof Function || len (any)) ? any : false;
		// JavaScript functions have a length attribute, denoting the number of parameters
		// Python objects are JavaScript functions, but their length doesn't matter, only their existence
		// By the term 'any instanceof Function' we make sure that Python objects aren't rejected when their length equals zero
	}
	__all__.__ = __;
	
	var bool = function (any) {		// Always truly returns a bool, rather than something truthy or falsy
		return !!__ (any);
	}
	bool.__name__ = 'bool'			// So it can be used as a type with a name
	__all__.bool = bool;
	
	var float = function (any) {
		if (isNaN (any)) {
			throw ('ValueError');	// !!! Turn into real value error
		}
		else {
			return +any;
		}
	}
	float.__name__ = 'float'
	__all__.float = float;
	
	var int = function (any) {
		return float (any) | 0
	}
	int.__name__ = 'int';
	__all__.int = int;
	
	var type = function (anObject) {
		try {
			var result = anObject.__class__;
			return result;
		}
		catch (exception) {
			var aType = typeof anObject;
			if (aType == 'boolean') {
				return bool;
			}
			else if (aType == 'number') {
				if (anObject % 1 == 0) {
					return int;
				}
				else {
					return float;
				}				
			}
			else {
				return aType;
			}
		}
	}
	__all__.type = type;
	
	var isinstance = function (anObject, classinfo) {
		function isA (queryClass) {
			if (queryClass == classinfo) {
				return true;
			}
			for (var index = 0; index < queryClass.__bases__.length; index++) {
				if (isA (queryClass.__bases__ [index], classinfo)) {
					return true;
				}
			}
			return false;
		}
		try {
			return '__class__' in anObject ? isA (anObject.__class__) : anObject instanceof classinfo;
		}
		catch (exception) {
			console.log (exception);
			console.dir (anObject);
		}
	};
	__all__.isinstance = isinstance;
	
	// Repr function uses __repr__ method, then __str__ then toString
	var repr = function (anObject) {
		try {
			return anObject.__repr__ ();
		}
		catch (exception) {
			try {
				return anObject.__str__ ();
			}
			catch (exception) {	// It was a dict in Python, so an Object in JavaScript
				try {
					if (anObject.constructor == Object) {
						var result = '{';
						var comma = false;
						for (var attrib in anObject) {
							if (!__specialattrib__ (attrib)) {
								if (attrib.isnumeric ()) {
									var attribRepr = attrib;				// If key can be interpreted as numerical, we make it numerical 
								}											// So we accept that '1' is misrepresented as 1
								else {
									var attribRepr = '\'' + attrib + '\'';	// Alpha key in dict
								}
								
								if (comma) {
									result += ', ';
								}
								else {
									comma = true;
								}
								try {
									result += attribRepr + ': ' + anObject [attrib] .__repr__ ();
								}
								catch (exception) {
									result += attribRepr + ': ' + anObject [attrib] .toString ();
								}
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
					console.log ('ERROR: Could not evaluate repr (<object of type ' + typeof anObject + '>)');
					return '???';
				}
			}
		}
	}
	__all__.repr = repr;
	
	// Char from Unicode or ASCII
	var chr = function (charCode) {
		return String.fromCharCode (charCode);
	}
	__all__.chr = chr;

	// Unicode or ASCII from char
	var ord = function (aChar) {
		return aChar.charCodeAt (0);
	}
	__all__.org = ord;
	
	// Maximum of n numbers
	var max = Math.max;
	__all__.max = max;
	
	// Minimum of n numbers
	var min = Math.min;
	__all__.min = min;
	
	// Absolute value
	var abs = Math.abs;
	__all__.abs = abs;
	
	// Bankers rounding
	var round = function (number, ndigits) {
		if (ndigits) {
			var scale = Math.pow (10, ndigits);
			number *= scale;
		}
			
		var rounded = Math.round (number);
		if (rounded - number == 0.5 && rounded % 2) {	// Has rounded up to odd, should have rounded down to even
			rounded -= 1;
		}
			
		if (ndigits) {
			rounded /= scale;
		}
		
		return rounded
 	}
	__all__.round = round;
		
	// Iterator protocol functions
	
	function wrap_py_next () {		// Add as 'next' method to make Python iterator JavaScript compatible
		var result = this.__next__ ();
		return {value: result, done: result == undefined};		
	}
	
	function wrap_js_next () {		// Add as '__next__' method to make JavaScript iterator Python compatible
		var result = this.next ();
		if (result.done) {
			throw StopIteration ();
		}
		else {
			return result.value;
		}
	}
	
	function py_iter (iterable) {	// Produces universal iterator with Python '__next__' as well as JavaScript 'next'
		if ('__iter__' in iterable) {	// It's a Python iterable (incl. JavaScript Arrays and strings)
			var iterator = iterable.__iter__ ();
			iterator.next = wrap_py_next;
			return iterator;
		}
		else if ('selector' in iterable) { // Assume it's a JQuery iterator
			var iterator = list (iterable) .__iter__ ();
			iterator.next = wrap_py_next;
			return iterator;
		}
		else if ('next' in iterable) {	// It's a JavaScript generator
			// It should have an iterator field, but doesn't in Chrome
			// So we just return the generator itself, which is both an iterable and an iterator
			iterable.__next__ = wrap_js_next;
			return iterable;
		}
		else {
			return null;
		}
	}
	__all__.py_iter = py_iter;
	
	function py_next (iterator) {				// Called only in a Python context, could receive Python or JavaScript iterator
		try {									// Primarily assume Python iterator, for max speed
			var result = iterator.__next__ ();
		}
		catch (exception) {						// JavaScript iterators are the exception here
			var result = iterator.next ();
			if (result.done) {
				throw StopIteration ();
			}
			else {
				return result.value;
			}
		}	
		if (result == undefined) {
			throw StopIteration ();
		}
		return result;
	}
	__all__.py_next = py_next;
	
	function __SeqIterator__ (iterable) {
		this.iterable = iterable;
		this.index = 0;
	}
	
	__all__.__SeqIterator__ = __SeqIterator__;
	
	__SeqIterator__.prototype.__iter__ = function () {
		return this;
	}
	
	__SeqIterator__.prototype.__next__ = function () {
		return this.iterable [this.index++];
	}
	
	__SeqIterator__.prototype.next = wrap_py_next;
	
	function __KeyIterator__ (iterable) {
		this.iterable = iterable;
		this.index = 0;
	}

	__all__.__KeyIterator__ = __KeyIterator__;
	
	__KeyIterator__.prototype.__iter__ = function () {
		return this;
	}
	
	__KeyIterator__.prototype.__next__ = function () {
		return this.iterable.keys () [this.index++];
	}
			
	__KeyIterator__.prototype.next = wrap_py_next;
	
	// Reversed function for arrays
	var py_reversed = function (iterable) {
		iterable = iterable.slice ();
		iterable.reverse ();
		return iterable;
	}
	__all__.py_reversed = py_reversed;
	
	// Zip method for arrays
	var zip = function () {
		var args = [] .slice.call (arguments);
		var shortest = args.length == 0 ? [] : args.reduce (	// Find shortest array in arguments
			function (array0, array1) {
				return array0.length < array1.length ? array0 : array1;
			}
		);
		return shortest.map (					// Map each element of shortest array
			function (current, index) {			// To the result of this function
				return args.map (				// Map each array in arguments
					function (current) {		// To the result of this function
						return current [index]; // Namely it's index't entry
					}
				);
			}
		);
	}
	__all__.zip = zip;
	
	// Range method, returning an array
	function range (start, stop, step) {
		if (stop == undefined) {
			// one param defined
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
	
	// Any, all and sum
	
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
	
	// Enumerate method, returning a zipped list
	function enumerate (iterable) {
		return zip (range (len (iterable)), iterable);
	}
	__all__.enumerate = enumerate;
		
	// Shallow and deepcopy
	
	function copy (anObject) {
		if (anObject == null || typeof anObject == "object") {
			return anObject;
		}
		else {
			var result = {}
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
			var result = {}
			for (var attrib in obj) {
				if (anObject.hasOwnProperty (attrib)) {
					result [attrib] = deepcopy (anObject [attrib]);
				}
			}
			return result;
		}
	}
	__all__.deepcopy = deepcopy;
		
	// List extensions to Array
	
	function list (iterable) {										// All such creators should be callable without new
		var instance = iterable ? [] .slice.apply (iterable) : [];	// Spread iterable, n.b. array.slice (), so array before dot
		// Sort is the normal JavaScript sort, Python sort is a non-member function
		return instance;
	}
	__all__.list = list;
	Array.prototype.__class__ = list;	// All arrays are lists (not only if constructed by the list ctor), unless constructed otherwise
	list.__name__ = 'list';
	
	/*
	Array.from = function (iterator) { // !!! remove
		result = [];
		for (item of iterator) {
			result.push (item);
		}
		return result;
	}
	*/
	
	Array.prototype.__iter__ = function () {
		return new __SeqIterator__ (this);
	}
	
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
		
		var result = list ([]);
		for (var index = start; index < stop; index += step) {
			result.push (this [index]);
		}
		
		return result;
	}
		
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
			
		if (step == null) {	// Assign to 'ordinary' slice, replace subsequence
			Array.prototype.splice.apply (this, [start, stop - start] .concat (source)) 
		}
		else {				// Assign to extended slice, replace designated items one by one
			var sourceIndex = 0;
			for (var targetIndex = start; targetIndex < stop; targetIndex += step) {
				this [targetIndex] = source [sourceIndex++];
			}
		}
	}
	
	Array.prototype.__repr__ = function () {
		if (this.__class__ == set && !this.length) {
			return 'set()';
		}
		
		var result = !this.__class__ || this.__class__ == list ? '[' : this.__class__ == tuple ? '(' : '{';
		
		for (var index = 0; index < this.length; index++) {
			if (index) {
				result += ', ';
			}
			try {
				result += this [index] .__repr__ ();
			}
			catch (exception) {
				result += this [index] .toString ();
			}
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

	Array.prototype.clear = function () {
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
			throw ('KeyError');
		}
		this.splice (index, 1);
	};

	Array.prototype.index = function (element) {
		return this.indexOf (element)
	};
	
	Array.prototype.py_pop = function (index) {
		if (index == undefined) {
			return this.pop ()	// Remove last element
		}
		else {
			return this.splice (index, 1) [0];
		}
	};	
	
	Array.prototype.py_sort = function () {
		__sort__.apply  (null, [this].concat ([] .slice.apply (arguments)));	// Can't work directly with arguments
		// Python params: (iterable, key = None, reverse = False)
		// py_sort is called with the Transcrypt kwargs mechanism, and just passes the params on to __sort__
		// __sort__ is def'ed with the Transcrypt kwargs mechanism
	};
	
	Array.prototype.__add__ = function (aList) {
		return list (this.concat (aList))
	}
	
	Array.prototype.__mul__ = function (scalar) {
		var result = this;
		for (var i = 1; i < scalar; i++) {
			result = result.concat (this);
		}
		return result;
	}
	
	Array.prototype.__rmul__ = Array.prototype.__mul__;
		
	// Tuple extensions to Array
	
	function tuple (iterable) {
		var instance = iterable ? [] .slice.apply (iterable) : [];
		instance.__class__ = tuple;	// Not all arrays are tuples
		return instance;
	}
	__all__.tuple = tuple;
	tuple.__name__ = 'tuple';
	
	// Set extensions to Array
	// N.B. Since sets are unordered, set operations will occasionally alter the 'this' array by sorting it
		
	function set (iterable) {
		var instance = [];
		if (iterable) {
			for (var index = 0; index < iterable.length; index++) {
				instance.add (iterable [index]);
			}
			
			
		}
		instance.__class__ = set;	// Not all arrays are sets
		return instance;
	}
	__all__.set = set;
	set.__name__ = 'set';
	
	Array.prototype.__bindexOf__ = function (element) {	// Used to turn O (n^2) into O (n log n)
	// Since sorting is lex, compare has to be lex. This also allows for mixed lists
	
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
	}
	
	Array.prototype.add = function (element) {		
		if (this.indexOf (element) == -1) {	// Avoid duplicates in set
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
		return set (other.slice ()) .issuperset (this);	// Sort copy of 'other', not 'other' itself, since it may be an ordered sequence
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
	
	Array.prototype.update = function () {	// O (n)
		var updated = [] .concat.apply (this.slice (), arguments) .sort ();		
		this.clear ();
		for (var i = 0; i < updated.length; i++) {
			if (updated [i] != updated [i - 1]) {
				this.push (updated [i]);
			}
		}
	};
	
	Array.prototype.__eq__ = function (other) {	// Also used for list
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
	
	Array.prototype.__ne__ = function (other) {	// Also used for list
		return !this.__eq__ (other);
	}
		
	Array.prototype.__le__ = function (other) {
		return this.issubset (other);
	}
		
	Array.prototype.__ge__ = function (other) {
		return this.issuperset (other);
	}
		
	Array.prototype.__lt__ = function (other) {
		return this.issubset (other) && !this.issuperset (other);
	}
		
	Array.prototype.__gt__ = function (other) {
		return this.issuperset (other) && !this.issubset (other);
	}
	
	// Dict extensions to object
	
	function __keyIterator__ () {
		return new __KeyIterator__ (this);
	}
	
	function __keys__ () {
		var keys = []
		for (var attrib in this) {
			if (!__specialattrib__ (attrib)) {
				keys.push (attrib);
			}     
		}
		return keys;
	}
		
	function __items__ () {
		var items = []
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
		}
		return aDefault;
	}	
	
	function __update__(aDict) {
		for (var aKey in aDict) {
			this [aKey] = aDict [aKey];
		}
	}
	
	function dict (objectOrPairs) {
		if (!objectOrPairs || objectOrPairs instanceof Array) {	// It's undefined or an array of pairs
			var instance = {};
			if (objectOrPairs) {
				for (var index = 0; index < objectOrPairs.length; index++) {
					var pair = objectOrPairs [index];
					instance [pair [0]] = pair [1];
				}
			}
		}
		else {													// It's a JavaScript object literal
			var instance = objectOrPairs;
		}
			
		// Trancrypt interprets e.g. {aKey: 'aValue'} as a Python dict literal rather than a JavaScript object literal
		// So dict literals rather than bare Object literals will be passed to JavaScript libraries
		// Some JavaScript libraries call all enumerable callable properties of an object that's passed to them
		// So the properties of a dict should be non-enumerable
		Object.defineProperty (instance, '__class__', {value: dict, enumerable: false, writable: true});
		Object.defineProperty (instance, 'keys', {value: __keys__, enumerable: false});
		Object.defineProperty (instance, '__iter__', {value: __keyIterator__, enumerable: false});
		Object.defineProperty (instance, 'items', {value: __items__, enumerable: false});		
		Object.defineProperty (instance, 'del', {value: __del__, enumerable: false});
		Object.defineProperty (instance, 'clear', {value: __clear__, enumerable: false});
		Object.defineProperty (instance, 'setdefault', {value: __setdefault__, enumerable: false});
		Object.defineProperty (instance, 'py_pop', {value: __pop__, enumerable: false});
		Object.defineProperty (instance, 'update', {value: __update__, enumerable: false});
		return instance;
	}
	__all__.dict = dict;
	dict.__name__ = 'dict';
	
	// String extensions
	
	function str (stringable) {
		try {
			return stringable.__str__ ();
		}
		catch (exception) {
			return new String (stringable);
		}
	}
	__all__.str = str;	
	
	String.prototype.__class__ = str;	// All strings are str
	str.__name__ = 'str';
	
	String.prototype.__iter__ = function () {
		return new __SeqIterator__ (this);
	}
		
	String.prototype.__repr__ = function () {
		return (this.indexOf ('\'') == -1 ? '\'' + this + '\'' : '"' + this + '"') .replace ('\t', '\\t') .replace ('\n', '\\n');
	};
	
	String.prototype.__str__ = function () {
		return this;
	};
	
	String.prototype.capitalize = function () {
		return this.charAt (0).toUpperCase () + this.slice (1);
	};
	
	String.prototype.endswith = function (suffix) {
		return suffix == '' || this.slice (-suffix.length) == suffix;
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
	}
	
	// Since it's worthwhile for the 'format' function to be able to deal with *args, it is defined as a property
	// __get__ will produce a bound function if there's something before the dot
	// Since a call using *args is compiled to e.g. <object>.<function>.apply (null, args), the function has to be bound already
	// Otherwise it will never be, because of the null argument
	// Using 'this' rather than 'null' contradicts the requirement to be able to pass bound functions around
	// The object 'before the dot' won't be available at call time in that case, unless implicitly via the function bound to it
	// While for Python methods this mechanism is generated by the compiler, for JavaScript methods it has to be provided manually
	// Call memoizing is unattractive here, since every string would then have to hold a reference to a bound format method
	Object.defineProperty (String.prototype, 'format', {
		get: function () {return __get__ (this, function (self) {
			var args = tuple ([] .slice.apply (arguments).slice (1));			
			var autoIndex = 0;
			return self.replace (/\{(\w*)\}/g, function (match, key) { 
				if (key == '') {
					key = autoIndex++;
				}
				if (key == +key) {	// So key is numerical
					return args [key] == undefined ? match : args [key];
				}
				else {				// Key is a string
					for (var index = 0; index < args.length; index++) {
						// Find first 'dict' that has that key and the right field
						if (typeof args [index] == 'object' && args [index][key] != undefined) {
							return args [index][key];	// Return that field field
						}
					}
					return match;
				}
			});
		});},
		enumerable: true
	});
	
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
	
	String.prototype.rsplit = function (sep, maxsplit) {	// Combination of general whitespace sep and positive maxsplit neither supported nor checked, expensive and rare
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
	
	String.prototype.py_split = function (sep, maxsplit) {	// Combination of general whitespace sep and positive maxsplit neither supported nor checked, expensive and rare
		if (sep == undefined || sep == null) {
			sep = /\s+/
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
		return this.indexOf (prefix) == 0;
	};
	
	String.prototype.strip = function () {
		return this.trim ();
	};
		
	String.prototype.upper = function () {
		return this.toUpperCase ();
	};
	
	String.prototype.__mul__ = function (scalar) {
		var result = this;
		for (var i = 1; i < scalar; i++) {
			result = result + this;
		}
		return result;
	}
	
	String.prototype.__rmul__ = String.prototype.__mul__;
		
	// General operator overloading, only the ones that make most sense in matrix and complex operations
	
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
	
	var __div__ = function (a, b) {
		if (typeof a == 'object' && '__div__' in a) {
			return a.__div__ (b);
		}
		else if (typeof b == 'object' && '__rdiv__' in b) {
			return b.__rdiv__ (a);
		}
		else {
			return a / b;
		}
	};  
	__all__.__div__ = __div__;
	
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
	
	var __eq__ = function (a, b) {
		if (typeof a == 'object' && '__eq__' in a) {
			return a.__eq__ (b);
		}
		else {
			return a == b
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
			return a < b
		}
	};
	__all__.__lt__ = __lt__;
		
	var __le__ = function (a, b) {
		if (typeof a == 'object' && '__le__' in a) {
			return a.__le__ (b);
		}
		else {
			return a <= b
		}
	};
	__all__.__le__ = __le__;
		
	var __gt__ = function (a, b) {
		if (typeof a == 'object' && '__gt__' in a) {
			return a.__gt__ (b);
		}
		else {
			return a > b
		}
	};
	__all__.__gt__ = __gt__;
		
	var __ge__ = function (a, b) {
		if (typeof a == 'object' && '__ge__' in a) {
			return a.__ge__ (b);
		}
		else {
			return a >= b
		}
	};
	__all__.__ge__ = __ge__;
		
	var __getitem__ = function (container, key) {							// Slice c.q. index, direct generated call to runtime switch
		if (typeof container == 'object' && '__getitem__' in container) {
			return container.__getitem__ (key);								// Overloaded on container
		}
		else {
			return container [key];											// Container must support bare JavaScript brackets
		}
	};
	__all__.__getitem__ = __getitem__;

	var __setitem__ = function (container, key, value) {					// Slice c.q. index, direct generated call to runtime switch
		if (typeof container == 'object' && '__setitem__' in container) {
			container.__setitem__ (key, value);								// Overloaded on container
		}
		else {
			container [key] = value;										// Container must support bare JavaScript brackets
		}
	};
	__all__.__setitem__ = __setitem__;

	var __getslice__ = function (container, lower, upper, step) {			// Slice only, no index, direct generated call to runtime switch
		if (typeof container == 'object' && '__getitem__' in container) {
			return container.__getitem__ ([lower, upper, step]);			// Container supports overloaded slicing c.q. indexing
		}
		else {
			return container.__getslice__ (lower, upper, step);				// Container only supports slicing injected natively in prototype
		}
	};
	__all__.__getslice__ = __getslice__;

	var __setslice__ = function (container, lower, upper, step, value) {	// Slice, no index, direct generated call to runtime switch
		if (typeof container == 'object' && '__setitem__' in container) {
			container.__setitem__ ([lower, upper, step], value);			// Container supports overloaded slicing c.q. indexing
		}
		else {
			container.__setslice__ (lower, upper, step, value);				// Container only supports slicing injected natively in prototype
		}
	};
	__all__.__setslice__ = __setslice__;

	var __call__ = function (/* <callee>, <params>* */) {
		var args = [] .slice.apply (arguments)
		if (typeof args [0] == 'object' && '__call__' in args [0]) {
			return args [0] .__call__ .apply (null,  args.slice (1));
		}
		else {
			return args [0] .apply (null, args.slice (1));
		}		
	};
	__all__.__call__ = __call__;

function pytigon () {

	__nest__ (
		__all__,
		'page', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var Page = __class__ ('Page', [object], {
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
					var can_popup = __init__ (__world__.tools).can_popup;
					var corect_href = __init__ (__world__.tools).corect_href;
					var ajax_load = __init__ (__world__.tools).ajax_load;
					var ajax_get = __init__ (__world__.tools).ajax_get;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_submit = __init__ (__world__.tools).ajax_submit;
					var handle_class_click = __init__ (__world__.tools).handle_class_click;
					var mount_html = __init__ (__world__.tools).mount_html;
					var datatable_refresh = __init__ (__world__.tbl).datatable_refresh;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var refresh_fragment = function (data_item_to_refresh, fun, only_table) {
						if (typeof fun == 'undefined' || (fun != null && fun .__class__ == __kwargdict__)) {;
							var fun = null;
						};
						if (typeof only_table == 'undefined' || (only_table != null && only_table .__class__ == __kwargdict__)) {;
							var only_table = false;
						};
						var refr_block = data_item_to_refresh.closest ('.refr_object');
						if (refr_block.hasClass ('refr_target')) {
							var target = refr_block;
						}
						else {
							var target = refr_block.find ('.refr_target');
						}
						if (only_table) {
							var datatable = target.find ('table[name=tabsort].datatable');
							if (datatable.length > 0) {
								datatable_refresh (datatable);
								if (fun) {
									fun ();
								}
								return true;
							}
							return false;
						}
						var src = refr_block.find ('.refr_source');
						if (src.length > 0) {
							var href = src.attr ('href');
							if (src.prop ('tagName') == 'FORM') {
								var _refr2 = function (data) {
									mount_html (target, data);
									fragment_init (target);
									if (fun) {
										fun ();
									}
								};
								ajax_post (corect_href (href), src.serialize (), _refr2);
							}
							else {
								var _on_load = function (responseText) {
									// pass;
								};
								ajax_load (target, corect_href (href), _on_load);
							}
						}
						return true;
					};
					var on_popup_inline = function (elem) {
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery (elem).closest ('table').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<tr class='refr_source inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'><td colspan='20'>") + INLINE_TABLE_HTML) + '</td></tr>');
						new_fragment.insertAfter (jQuery (elem).closest ('tr'));
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
					var on_popup_in_form = function (elem) {
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (window.WAIT_ICON) {
							window.WAIT_ICON.start ();
						}
						jQuery (elem).closest ('div.Dialog').find ('.inline_dialog').remove ();
						window.COUNTER = window.COUNTER + 1;
						var id = window.COUNTER;
						var href2 = corect_href (jQuery (elem).attr ('href'));
						var new_fragment = jQuery (((((("<div class='refr_source inline_dialog hide' id='IDIAL_" + id) + "' href='") + href2) + "'>") + INLINE_TABLE_HTML) + '</div>');
						new_fragment.insertAfter (jQuery (elem).closest ('div.form-group'));
						var elem2 = new_fragment.find ('.refr_target');
						var _on_load = function (responseText, status, response) {
							jQuery ('#IDIAL_' + id).hide ();
							jQuery ('#IDIAL_' + id).removeClass ('hide');
							jQuery ('#IDIAL_' + id).show ('slow');
							if (status != 'error') {
								_dialog_loaded (false, elem2);
								var table_type = get_table_type (elem2);
								var tbl = elem2.find ('.tabsort');
								if (tbl.length > 0) {
									init_table (tbl, table_type);
								}
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
					var on_popup_edit_new = function (elem) {
						jQuery (elem).attr ('data-style', 'zoom-out');
						jQuery (elem).attr ('data-spinner-color', '#FF0000');
						window.WAIT_ICON = Ladda.create (elem);
						if (can_popup () && !(jQuery (elem).hasClass ('inline')) && !(jQuery (elem).attr ('name') && __in__ ('_inline', jQuery (elem).attr ('name')))) {
							var elem2 = jQuery ('div.dialog-data');
							elem2.closest ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var _on_load = function (responseText, status, response) {
								_dialog_loaded (true, elem2);
								on_dialog_load ();
							};
							ajax_load (elem2, jQuery (elem).attr ('href'), _on_load);
						}
						else {
							if (window.WAIT_ICON) {
								window.WAIT_ICON.start ();
							}
							if (jQuery (elem).hasClass ('new-row')) {
								var elem2 = jQuery (("<div class='refr_source inline_dialog tr hide'>" + INLINE_DIALOG_UPDATE_HTML) + '</div>');
								elem2.insertAfter (jQuery (elem).closest ('div.tr'));
							}
							else {
								var test = jQuery (elem).closest ('form');
								if (test.length > 0) {
									var elem2 = jQuery (("<div class='refr_source inline_dialog hide'>" + INLINE_DIALOG_UPDATE_HTML) + '</div>');
									elem2.insertAfter (jQuery (elem).closest ('div.form-group'));
								}
								else {
									var elem2 = jQuery (("<tr class='inline_dialog hide'><td colspan='20'>" + INLINE_DIALOG_UPDATE_HTML) + '</td></tr>');
									elem2.insertAfter (jQuery (elem).closest ('tr'));
								}
							}
							mount_html (elem2.find ('.modal-title'), jQuery (elem).attr ('title'));
							elem2.find ('.refr_object').attr ('related-object', jQuery (elem).uid ());
							var elem3 = elem2.find ('div.dialog-data-inner');
							var _on_load2 = function (responseText, status, response) {
								elem2.hide ();
								elem2.removeClass ('hide');
								elem2.show ('slow');
								if (status != 'error') {
									_dialog_loaded (false, elem3);
									var table_type = get_table_type (elem3);
									init_table (elem3, table_type);
									on_dialog_load ();
								}
								if (window.WAIT_ICON) {
									window.WAIT_ICON.stop ();
									window.WAIT_ICON = null;
								}
							};
							ajax_load (elem3, jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_popup_info = function (elem) {
						if (can_popup ()) {
							var _on_load = function (responseText, status, response) {
								jQuery ('div.dialog-form-info').modal ();
							};
							ajax_load (jQuery ('div.dialog-data-info'), jQuery (elem).attr ('href'), _on_load);
						}
						else {
							jQuery ('.inline_dialog').remove ();
							jQuery (("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_INFO_HTML) + '</td></tr>').insertAfter (jQuery (elem).parents ('tr'));
							var _on_load2 = function (responseText, status, response) {
								// pass;
							};
							ajax_load (jQuery ('div.dialog-data-inner'), jQuery (elem).attr ('href'), _on_load2);
						}
						return false;
					};
					var on_popup_delete = function (elem) {
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
							var elem2 = jQuery (("<tr class='inline_dialog'><td colspan='20'>" + INLINE_DIALOG_DELETE_HTML) + '</td></tr>');
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
						fragment_init (elem);
						if (is_modal) {
							jQuery ('div.dialog-form').fadeTo ('fast', 1);
							if (jQuery ('div.dialog-form').find ('div.form2columns').length > 0) {
								jQuery ('div.dialog-form').find ('.modal-dialog').addClass ('modal-lg');
							}
							else {
								jQuery ('div.dialog-form').find ('.modal-dialog').removeClass ('modal-lg');
							}
							jQuery ('div.dialog-form').modal ();
							jQuery ('div.dialog-form').drags (dict ({'handle': '.modal-header'}));
						}
					};
					var _refresh_win = function (responseText, ok_button) {
						var popup_activator = jQuery ('#' + jQuery (ok_button).closest ('.refr_object').attr ('related-object'));
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							if (!(can_popup ())) {
								if (jQuery ('div.dialog-form').hasClass ('in')) {
									var dialog = 'div.dialog-form';
								}
								else {
									if (jQuery ('div.dialog-form-delete').hasClass ('in')) {
										var dialog = 'div.dialog-form-delete';
									}
									else {
										var dialog = 'div.dialog-form-info';
									}
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
								if (!(refresh_fragment (popup_activator, null, true))) {
									return refresh_fragment (popup_activator, null, true);
								}
							}
						}
						else {
							if (!(can_popup ())) {
								mount_html (jQuery ('div.dialog-data'), responseText);
							}
							else {
								mount_html (ok_button.closest ('.refr_target'), responseText);
							}
						}
					};
					var _refresh_win_and_ret = function (responseText, ok_button) {
						if (responseText && __in__ ('RETURN_OK', responseText)) {
							var related_object = jQuery (ok_button).closest ('.refr_object').attr ('related-object');
							var popup_activator = jQuery ('#' + related_object);
							if (jQuery (ok_button).closest ('.refr_object').hasClass ('in')) {
								jQuery ('div.dialog-form').modal ('hide');
							}
							else {
								jQuery (ok_button).closest ('.refr_object').remove ();
							}
							if (popup_activator && popup_activator.data ('edit_ret_function')) {
								window.RET_CONTROL = popup_activator.data ('ret_control');
								window.EDIT_RET_FUNCTION = popup_activator.data ('edit_ret_function');
								var q = jQuery (responseText);
								eval (q [1].text);
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
					var on_edit_ok = function (form) {
						var _fun = function (data) {
							_refresh_win_after_ok (data, form);
						};
						ajax_submit (form, _fun);
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
						jQuery (elem).closest ('.inline_dialog').remove ();
					};
					window.on_cancel_inline = on_cancel_inline;
					var ret_ok = function (id, title) {
						window.RET_CONTROL.select2 ('data', dict ([[id, id], [text, title]])).trigger ('change');
						window.RET_CONTROL.val (id.toString ());
						window.RET_CONTROL [0].defaultValue = id.toString ();
					};
					var on_get_tbl_value = function (elem) {
						on_popup_in_form (elem);
					};
					var on_new_tbl_value = function (elem) {
						window.EDIT_RET_FUNCTION = _refresh_win_and_ret;
						window.RET_CONTROL = jQuery (elem).closest ('.input-group').find ('.django-select2');
						jQuery (elem).data ('edit_ret_function', window.EDIT_RET_FUNCTION);
						jQuery (elem).data ('ret_control', window.RET_CONTROL);
						return on_popup_edit_new (elem);
					};
					var on_get_row = function (elem) {
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
					var fragment_init = function (elem) {
						if (typeof elem == 'undefined' || (elem != null && elem .__class__ == __kwargdict__)) {;
							var elem = null;
						};
						if (elem) {
							var elem2 = elem;
						}
						else {
							var elem2 = window.ACTIVE_PAGE.page;
						}
						handle_class_click (elem, 'get_tbl_value', on_get_tbl_value);
						handle_class_click (elem, 'new_tbl_value', on_new_tbl_value);
						handle_class_click (elem, 'get_row', on_get_row);
						var d = elem2.find ('.dateinput');
						d.wrap ("<div class='input-group date'></div>");
						d.after ("<span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span>");
						d.parent ().datetimepicker (dict ({'format': 'YYYY-MM-DD', 'locale': 'pl', 'showTodayButton': true}));
						var d = elem2.find ('.datetimeinput');
						d.wrap ("<div class='input-group date datetime'></div>");
						d.after ("<span class='input-group-addon'><span class='glyphicon glyphicon-time'></span></span>");
						d.parent ().datetimepicker (dict ({'format': 'YYYY-MM-DD hh:mm', 'locale': 'pl', 'showTodayButton': true}));
						elem2.find ('.win-content').bind ('resize', datatable_onresize);
						jQuery ('.selectpicker').selectpicker ();
						if (window.BASE_FRAGMENT_INIT) {
							window.BASE_FRAGMENT_INIT ();
						}
						datatable_onresize ();
					};
					__pragma__ ('<use>' +
						'tbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__._dialog_loaded = _dialog_loaded;
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
						__all__.fragment_init = fragment_init;
						__all__.handle_class_click = handle_class_click;
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
						__all__.refresh_fragment = refresh_fragment;
						__all__.ret_ok = ret_ok;
					__pragma__ ('</all>')
				}
			}
		}
	);
	__nest__ (
		__all__,
		'scrolltbl', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var stick_resize = function () {
						var tbl = window.ACTIVE_PAGE.page.find ('.tbl_scroll');
						if (tbl.length > 0) {
							var dy_table = tbl.offset ().top;
							var __left0__ = jQuery (window).height ();
							var dy_win = __left0__;
							var dy_win = __left0__;
							var dy = dy_win - dy_table;
							if (dy < 100) {
								var dy = 100;
							}
							tbl.height (dy - 35);
						}
					};
					var resize_win = function () {
						stick_resize ();
						var tab2 = list ([]);
						var tab_width = window.ACTIVE_PAGE.page.find ("table[name='tabsort']").width ();
						window.ACTIVE_PAGE.page.find ('.tbl_header').width (tab_width);
						var _local_fun = function () {
							tab2.push (jQuery (this).width ());
						};
						window.ACTIVE_PAGE.page.find ("table[name='tabsort'] tr:first td").each (_local_fun);
						var tab2 = tab2.reverse ();
						var _local_fun2 = function () {
							jQuery (this).width (tab2.py_pop ());
						};
						window.ACTIVE_PAGE.page.find ('.tbl_header th').each (_local_fun2);
					};
					var stick_header = function () {
						var tab = list ([]);
						var tab2 = list ([]);
						var _local_fun = function () {
							tab.push (jQuery (this).width ());
						};
						window.ACTIVE_PAGE.page.find ('table.tabsort th').each (_local_fun);
						var table = jQuery ('<table class="tabsort tbl_header" style="overflow-x: hidden;"></table>');
						table.append (window.ACTIVE_PAGE.page.find ('table.tabsort thead'));
						window.ACTIVE_PAGE.page.find ('.tbl_scroll').before (table);
						var _local_fun2 = function () {
							tab2.push (jQuery (this).width ());
						};
						window.ACTIVE_PAGE.page.find ('.tbl_header th').each (_local_fun2);
						var tab2 = tab2.reverse ();
						var _local_fun3 = function () {
							var x = tab2.py_pop ();
							if (x > jQuery (this).width ()) {
								jQuery (this).css ('min-width', x);
							}
						};
						window.ACTIVE_PAGE.page.find ("table[name='tabsort'] tr:first td").each (_local_fun3);
						var tab = tab.reverse ();
						var _local_fun4 = function () {
							jQuery (this).width (tab.py_pop ());
						};
						window.ACTIVE_PAGE.page.find ('.tbl_header th').each (_local_fun4);
						jQuery (window).resize (resize_win);
						resize_win ();
					};
					__pragma__ ('<all>')
						__all__.resize_win = resize_win;
						__all__.stick_header = stick_header;
						__all__.stick_resize = stick_resize;
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
					var Page = __init__ (__world__.page).Page;
					var TabMenuItem = __init__ (__world__.tabmenuitem).TabMenuItem;
					var datatable_onresize = __init__ (__world__.tbl).datatable_onresize;
					var history_push_state = __init__ (__world__.tools).history_push_state;
					var mount_html = __init__ (__world__.tools).mount_html;
					var TabMenu = __class__ ('TabMenu', [object], {
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
							if (typeof push_state == 'undefined' || (push_state != null && push_state .__class__ == __kwargdict__)) {;
								var push_state = true;
							};
							var menu_item = self.titles [title];
							jQuery (sprintf ('#li_%s a', menu_item.id)).tab ('show');
							if (push_state && window.PUSH_STATE) {
								history_push_state (menu_item.title, menu_item.url);
							}
							datatable_onresize ();
						});},
						get new_page () {return __get__ (this, function (self, title, data, href, component_init, page_init) {
							var _id = 'tab' + self.id;
							var title2 = jQuery.trim (title);
							var menu_item = TabMenuItem (_id, title2, href, data);
							self.titles [title2] = menu_item;
							jQuery ('#tabs2').append (vsprintf ("<li id='li_%s'><a href='#%s' data-toggle='tab'>%s &nbsp &nbsp</a> <button id = 'button_%s' class='close btn btn-raised btn-danger btn-xs' title='remove page' type='button'><span class='fa fa-times'></span></button></li>", list ([_id, _id, title2, _id])));
							jQuery ('#tabs2_content').append (sprintf ("<div class='tab-pane' id='%s'></div>", _id));
							window.ACTIVE_PAGE = Page (_id, jQuery ('#' + _id));
							self.active_item = menu_item;
							mount_html (jQuery ('#' + _id), data);
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
							jQuery ('#tabs2 a:last').on ('shown.bs.tab', _on_show_tab);
							jQuery ('#tabs2 a:last').tab ('show');
							page_init (_id, false);
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
							var _local_fun = function (index, value) {
								if (value && value.id == id) {
									self.titles [index] = null;
								}
							};
							jQuery.each (self.titles, _local_fun);
							jQuery (sprintf ('#li_%s', id)).remove ();
							jQuery (sprintf ('#%s', id)).remove ();
							jQuery ('#tabs2 a:last').tab ('show');
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
					var TabMenuItem = __class__ ('TabMenuItem', [object], {
						get __init__ () {return __get__ (this, function (self, id, title, url, data) {
							if (typeof data == 'undefined' || (data != null && data .__class__ == __kwargdict__)) {;
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
					var stick_header = __init__ (__world__.scrolltbl).stick_header;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var ajax_post = __init__ (__world__.tools).ajax_post;
					var datetable_set_height = function () {
						if (jQuery (this).hasClass ('table_get')) {
							return ;
						}
						if (!(jQuery (this).is (':visible'))) {
							return ;
						}
						var elem = jQuery (this).closest ('.tabsort_panel');
						var dy_table = elem.height ();
						var dy_win = jQuery (window).height ();
						var dy_body1 = 0;
						var _local_fun = function () {
							dy_body1 += jQuery (this).height ();
						};
						jQuery ('.win-header').each (_local_fun);
						var dy_body2 = jQuery ('.win-content').height ();
						var dy_body = dy_body1 + dy_body2;
						var dy = dy_table + (dy_win - dy_body);
						if (dy < 200) {
							var dy = 200;
						}
						jQuery (this).bootstrapTable ('resetView', dict ({'height': dy - 10}));
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
						if (table_type == 'scrolled') {
							stick_header ();
						}
						if (table_type == 'datatable') {
							var onLoadSuccess = function (data) {
								prepare_datatable (table);
								datatable_onresize ();
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
						}
					};
					var datatable_onresize = function () {
						jQuery ('.datatable:not(.table_get)').each (datetable_set_height);
					};
					__pragma__ ('<use>' +
						'scrolltbl' +
						'tools' +
					'</use>')
					__pragma__ ('<all>')
						__all__._rowStyle = _rowStyle;
						__all__.ajax_post = ajax_post;
						__all__.datatable_ajax = datatable_ajax;
						__all__.datatable_onresize = datatable_onresize;
						__all__.datatable_refresh = datatable_refresh;
						__all__.datetable_set_height = datetable_set_height;
						__all__.init_table = init_table;
						__all__.prepare_datatable = prepare_datatable;
						__all__.stick_header = stick_header;
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
					var LOADED_FILES = dict ({});
					var evalJSFromHtml = function (html) {
						var newElement = document.createElement ('div');
						newElement.innerHTML = html;
						var scripts = newElement.getElementsByTagName ('script');
						var eval_fun = function (id, value) {
							eval (value.innerHTML);
						};
						jQuery.each (scripts, eval_fun);
					};
					var mount_html = function (elem, html_txt) {
						if (window.COMPONENT_INIT) {
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
							}
						}
						else {
							elem.html (html_txt);
						}
					};
					var download_binary_file = function (buf, content_disposition) {
						var l = buf.length;
						var buffer = new ArrayBuffer (l);
						var view = new Uint8Array (buffer);
						for (var i = 0; i < l; i++) {
							view [i] = buf.charCodeAt (i);
						}
						var mimetype = 'text/html';
						if (__in__ ('odf', content_disposition) || __in__ ('ods', content_disposition)) {
							var mimetype = 'application/vnd.oasis.opendocument.formula';
						}
						else {
							if (__in__ ('pdf', content_disposition)) {
								var mimetype = 'application/pdf';
							}
							else {
								if (__in__ ('zip', content_disposition)) {
									var mimetype = 'application/x-compressed';
								}
								else {
									if (__in__ ('xls', content_disposition)) {
										var mimetype = 'application/excel';
									}
								}
							}
						}
						var blob = new Blob (list ([view]), dict ({'type': mimetype}));
						var blobURL = window.URL.createObjectURL (blob);
						window.open (blobURL);
					};
					var ajax_get = function (url, complete) {
						var req = new XMLHttpRequest ();
						var _onload = function () {
							var disp = req.getResponseHeader ('Content-Disposition');
							if (disp && __in__ ('attachment', disp)) {
								download_binary_file (req.response, disp);
								complete (null);
							}
							else {
								complete (req.responseText);
							}
						};
						req.onload = _onload;
						req.open ('GET', url, true);
						req.send ();
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
					var _req_post = function (req, url, data, complete) {
						var _onload = function () {
							var disp = req.getResponseHeader ('Content-Disposition');
							if (disp && __in__ ('attachment', disp)) {
								download_binary_file (req.response, disp);
								complete (null);
							}
							else {
								complete (req.responseText);
							}
						};
						req.onload = _onload;
						req.open ('POST', url, true);
						req.setRequestHeader ('X-CSRFToken', Cookies.get ('csrftoken'));
						if (data.length) {
							req.setRequestHeader ('Content-type', 'application/x-www-form-urlencoded');
							req.setRequestHeader ('Content-length', data.length);
							req.setRequestHeader ('Connection', 'close');
						}
						req.send (data);
					};
					var ajax_post = function (url, data, complete) {
						var req = new XMLHttpRequest ();
						_req_post (req, url, data, complete);
					};
					window.ajax_post = ajax_post;
					var ajax_submit = function (form, complete, data_filter) {
						if (typeof data_filter == 'undefined' || (data_filter != null && data_filter .__class__ == __kwargdict__)) {;
							var data_filter = null;
						};
						var req = new XMLHttpRequest ();
						if (form.find ("[type='file']").length > 0) {
							form.attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
							var data = new FormData (form [0]);
							if (data_filter) {
								var data = data_filter (data);
							}
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
						_req_post (req, corect_href (form.attr ('action')), data, complete);
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
							else {
								return 'scrolled';
							}
						}
						else {
							return '';
						}
					};
					var can_popup = function () {
						if (jQuery ('div.dialog-form').hasClass ('in') || jQuery ('div.dialog-form-delete').hasClass ('in') || jQuery ('div.dialog-form-info').hasClass ('in')) {
							return false;
						}
						else {
							return true;
						}
					};
					var corect_href = function (href) {
						if (__in__ ('only_content', href)) {
							return href;
						}
						else {
							if (__in__ ('?', href)) {
								return href + '&only_content=1';
							}
							else {
								return href + '?only_content=1';
							}
						}
					};
					var handle_class_click = function (fragment_obj, obj_class, fun) {
						var _on_click = function (e) {
							var src_obj = jQuery (this);
							e.preventDefault ();
							fun (this);
							return false;
						};
						fragment_obj.on ('click', '.' + obj_class, _on_click);
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
								for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
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
						for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
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
						if (typeof data == 'undefined' || (data != null && data .__class__ == __kwargdict__)) {;
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
					__pragma__ ('<all>')
						__all__.LOADED_FILES = LOADED_FILES;
						__all__._req_post = _req_post;
						__all__.ajax_get = ajax_get;
						__all__.ajax_load = ajax_load;
						__all__.ajax_post = ajax_post;
						__all__.ajax_submit = ajax_submit;
						__all__.can_popup = can_popup;
						__all__.corect_href = corect_href;
						__all__.download_binary_file = download_binary_file;
						__all__.evalJSFromHtml = evalJSFromHtml;
						__all__.get_page = get_page;
						__all__.get_table_type = get_table_type;
						__all__.handle_class_click = handle_class_click;
						__all__.history_push_state = history_push_state;
						__all__.load_css = load_css;
						__all__.load_js = load_js;
						__all__.load_many_js = load_many_js;
						__all__.mount_html = mount_html;
						__all__.on_load_js = on_load_js;
					__pragma__ ('</all>')
				}
			}
		}
	);
	(function () {
		var __symbols__ = ['__esv5__'];
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
		var fragment_init = __init__ (__world__.popup).fragment_init;
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
		var init_pagintor = function (pg) {
			var x = load_js;
			if (pg.length > 0) {
				var paginate = true;
				var totalPages = pg.attr ('totalPages');
				var page_number = pg.attr ('start_page');
				var _on_page_click = function (event, page) {
					var form = pg.closest ('.refr_object').find ('form.refr_source');
					if (form) {
						var _on_new_page = function (data) {
							mount_html (pg.closest ('.content').find ('.tabsort tbody'), jQuery (jQuery.parseHTML (data)).find ('.tabsort tbody').html ());
							fragment_init (pg.closest ('.content').find ('.tabsort tbody'));
							if (window.WAIT_ICON2) {
								jQuery ('#loading-indicator').hide ();
								window.WAIT_ICON2 = false;
							}
						};
						var url = pg.attr ('href').py_replace ('[[page]]', page) + '&only_content=1';
						form.attr ('action', url);
						form.attr ('href', url);
						var active_button = pg.find ('.page active');
						window.WAIT_ICON2 = true;
						jQuery ('#loading-indicator').show ();
						ajax_post (url, form.serialize (), _on_new_page);
					}
				};
				var options = dict ({'totalPages': +(totalPages), 'startPage': +(page_number), 'visiblePages': 3, 'first': '<<', 'prev': '<', 'next': '>', 'last': '>>', 'onPageClick': _on_page_click});
				pg.twbsPagination (options);
				if (+(page_number) != 1) {
					var form = pg.closest ('.refr_object').find ('form.refr_source');
					var url = pg.attr ('href').py_replace ('[[page]]', page_number) + '&only_content=1';
					form.attr ('action', url);
					form.attr ('href', url);
				}
			}
			else {
				var paginate = false;
			}
			return paginate;
		};
		var page_init = function (id, first_time) {
			if (typeof first_time == 'undefined' || (first_time != null && first_time .__class__ == __kwargdict__)) {;
				var first_time = true;
			};
			var table_type = get_table_type (jQuery ('#' + id));
			if (table_type != 'datatable') {
				if (window.ACTIVE_PAGE) {
					var pg = window.ACTIVE_PAGE.page.find ('.pagination');
					var paginate = init_pagintor (pg);
				}
			}
			init_table (jQuery (('#' + id) + ' .tabsort'), table_type);
			if (first_time) {
				var elem2 = jQuery ('body');
			}
			var _on_click = function (e) {
				var target = jQuery (e.currentTarget).attr ('target');
				var src_obj = jQuery (this);
				if (target == '_blank') {
					return ;
				}
				var __iterable0__ = list (['get_tbl_value', 'new_tbl_value', 'get_row']);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var pos = __iterable0__ [__index0__];
					if (jQuery (this).hasClass (pos)) {
						return true;
					}
				}
				var __iterable0__ = list ([tuple (['popup', on_popup_edit_new]), tuple (['popup_inline', on_popup_inline]), tuple (['popup_info', on_popup_info]), tuple (['popup_delete', on_popup_delete])]);
				for (var __index0__ = 0; __index0__ < __iterable0__.length; __index0__++) {
					var pos = __iterable0__ [__index0__];
					if (jQuery (this).hasClass (pos [0])) {
						e.preventDefault ();
						pos [1] (this);
						return true;
					}
				}
				var href = jQuery (this).attr ('href');
				if (href && __in__ ('#', href)) {
					return true;
				}
				e.preventDefault ();
				if (__in__ (jQuery (e.currentTarget).attr ('target'), tuple (['_top', '_top2']))) {
					var title = jQuery (e.currentTarget).attr ('title');
					if (!(title)) {
						if (len (href) > 16) {
							var title = '...' + href.__getslice__ (-(13), null, 1);
						}
						else {
							var title = href;
						}
					}
					return _on_menu_href (this, title);
				}
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
							mount_html (window.ACTIVE_PAGE.page, data);
							window.ACTIVE_PAGE.set_href (href);
							page_init (window.ACTIVE_PAGE.id, false);
						}
						else {
							mount_html (jQuery ('#body_body'), data);
							page_init ('body_body', false);
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
			jQuery ('#' + id).on ('click', 'a', _on_click);
			var _on_submit = function (e) {
				if (jQuery (this).attr ('target') == '_blank') {
					jQuery (this).attr ('enctype', 'multipart/form-data').attr ('encoding', 'multipart/form-data');
					return true;
				}
				if (jQuery (this).attr ('target') == 'refresh_obj') {
					if (refresh_fragment (jQuery (this), null, true)) {
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
					jQuery (this).attr ('action', corect_href (href));
				}
				var _on_submit2 = function (data) {
					mount_html (window.ACTIVE_PAGE.page, data);
					page_init (id, false);
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
			window.ACTIVE_PAGE.page.find ('form').submit (_on_submit);
			fragment_init (window.ACTIVE_PAGE.page);
		};
		var app_init = function (application_template, menu_id, lang, base_path, base_fragment_init, component_init) {
			window.APPLICATION_TEMPLATE = application_template;
			window.MENU = null;
			window.PUSH_STATE = true;
			window.BASE_PATH = null;
			window.BASE_PATH = base_path;
			window.WAIT_ICON = null;
			window.WAIT_ICON2 = false;
			window.MENU_ID = 0;
			window.BASE_FRAGMENT_INIT = base_fragment_init;
			window.COUNTER = 1;
			window.EDIT_RET_FUNCTION = null;
			window.RET_CONTROL = null;
			window.COMPONENT_INIT = component_init;
			window.LANG = lang;
			if (can_popup ()) {
				var _local_fun = function () {
					jQuery ('#tabs').tabdrop ();
					jQuery ('#tabs2').tabdrop ();
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
					jQuery (elem.prop ('hash')).perfectScrollbar ();
					var _on_menu_click = function (e) {
						if (window.APPLICATION_TEMPLATE != 'traditional') {
							e.preventDefault ();
							_on_menu_href (this);
						}
					};
					jQuery ('body').on ('click', 'a.menu-href', _on_menu_click);
					var _on_submit = function (e) {
						e.preventDefault ();
						on_edit_ok (jQuery (this));
					};
					jQuery ('body').on ('submit', 'form.DialogForm', _on_submit);
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
						jQuery (jQuery (this).prop ('hash')).perfectScrollbar ();
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
					jQuery (window).resize (datatable_onresize);
				};
				jQuery (_local_fun);
			}
		};
		var _on_menu_href = function (elem, title) {
			if (typeof title == 'undefined' || (title != null && title .__class__ == __kwargdict__)) {;
				var title = null;
			};
			if (window.APPLICATION_TEMPLATE != 'traditional') {
				if (!(title)) {
					var title = jQuery.trim (jQuery (elem).text ());
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
					var href = jQuery (elem).attr ('href');
					var href2 = corect_href (href);
					var _on_new_win = function (data) {
						if (window.APPLICATION_TEMPLATE == 'modern') {
							var id = menu.new_page (title, data, href2, window.COMPONENT_INIT, page_init);
						}
						else {
							mount_html (jQuery ('#body_body'), data);
							window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
							window.ACTIVE_PAGE.set_href (href2);
							page_init ('body_body', false);
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
				mount_html (jQuery (this).find ('div.dialog-data'), "<div class='alert alert-info' role='alert'>Sending data - please wait</div>");
			};
			jQuery ('div.dialog-form').on ('hide.bs.modal', _on_hide);
			var _local_fun = function () {
				console.log ('collapsed');
			};
			jQuery ('.navbar-ex1-collapse').on ('hidden.bs.collapse', _local_fun);
			if (window.APPLICATION_TEMPLATE == 'traditional') {
				window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
				page_init ('body_body');
			}
			else {
				if (window.APPLICATION_TEMPLATE == 'modern') {
					var txt = jQuery ('.page').text ();
					var txt2 = jQuery.trim (txt);
					if (txt2) {
						var txt = jQuery.trim (jQuery ('.page') [0].outerHTML);
						jQuery ('.page').remove ();
						var menu = get_menu ();
						menu.new_page (jQuery ('title').text (), txt, window.location.href, window.COMPONENT_INIT, page_init);
					}
				}
				else {
					window.ACTIVE_PAGE = Page (0, jQuery ('#body_body'));
					page_init ('body_body');
				}
			}
		};
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
			else {
				if (window.APPLICATION_TEMPLATE == 'modern') {
					// pass;
				}
				else {
					mount_html (jQuery ('#body_body'), '');
					window.ACTIVE_PAGE = null;
					if (window.APPLICATION_TEMPLATE == 'standard') {
						jQuery ('a.menu-href').removeClass ('btn-warning');
					}
				}
			}
		};
		window.addEventListener ('popstate', _on_popstate, false);
		__pragma__ ('<use>' +
			'page' +
			'popup' +
			'tabmenu' +
			'tabmenuitem' +
			'tbl' +
			'tools' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Page = Page;
			__all__.TabMenuItem = TabMenuItem;
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
			__all__.fragment_init = fragment_init;
			__all__.get_menu = get_menu;
			__all__.get_table_type = get_table_type;
			__all__.handle_class_click = handle_class_click;
			__all__.history_push_state = history_push_state;
			__all__.init_pagintor = init_pagintor;
			__all__.init_table = init_table;
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
			__all__.on_new_tbl_value = on_new_tbl_value;
			__all__.on_popup_delete = on_popup_delete;
			__all__.on_popup_edit_new = on_popup_edit_new;
			__all__.on_popup_info = on_popup_info;
			__all__.on_popup_inline = on_popup_inline;
			__all__.page_init = page_init;
			__all__.refresh_fragment = refresh_fragment;
			__all__.ret_ok = ret_ok;
		__pragma__ ('</all>')
	}) ();
	return __all__;
}
window ['pytigon'] = pytigon ();
