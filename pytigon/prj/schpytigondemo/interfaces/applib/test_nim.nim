import py_ext
import std/json

type
  Person = object
    age: int
    name: string

proc json_test(arg: JsonNode): JsonNode =
  var hisName = "John"
  let herAge = 31
  echo "===================="
  echo arg
  echo "===================="
  var p = %* [ Person(age: 38, name: "Torbjørn"), Person(age: herAge, name: hisName) ]
  return p

py_ext.register_python_fun(json_test, "json_test")


proc int_test(arg: int): int = 
  return arg + 1

py_ext.register_python_fun(int_test, "int_test")


proc float_test(arg: float): float = 
  echo arg
  return arg + 1.0

py_ext.register_python_fun(float_test, "float_test")


proc string_test(arg: string): string = 
  return arg & " world!"

py_ext.register_python_fun(string_test, "string_test")


proc string_int_test(arg: string): int = 
  echo "Hello from void_test: " & arg
  return 1
  
py_ext.register_python_fun(string_int_test, "string_int_test")


proc void_test(): int = 
  echo "Hello from void_test"
  return 1

py_ext.register_python_fun(void_test, "void_test")


proc json_test2(arg: JsonNode): JsonNode =
  echo "===================="
  echo arg
  echo "===================="
  var p = %* {"OK": true,}
  return p

py_ext.register_python_fun(json_test2, "json_test2")
